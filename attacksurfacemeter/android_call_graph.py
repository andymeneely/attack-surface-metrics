__author__ = 'kevin'

# import statistics as stat
import networkx as nx
import os

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.javacg_loader import JavaCGLoader


class AndroidCallGraph(CallGraph):
    """
        Represents the Call Graph of a software system.

        Encapsulates a graph data structure where each node is a method/function call.

        Attributes:
            source: String that contains where the source code that this Call Graph represents comes from.
            call_graph: networkx.DiGraph. Internal representation of the graph data structure.
    """

    _android_override_input_methods = []
    _android_override_output_methods = []
    _android_black_list_packages = []
    _android_black_list_edges = []

    def __init__(self, source, graph, generation_errors=None):
        """
            CallGraph constructor

            Instantiates a new CallGraph object and generates a networkx.DiGraph representing the Call Graph of
            a program.

            Args:
                source: String that contains where the source code that this Call Graph represents comes from.
                graph: networkx.DiGraph. Internal representation of the graph data structure.

            Returns:
                A new instance of type CallGraph.
        """
        self.source = source
        self.call_graph = graph
        self.errors = generation_errors

        self._entry_points = set()
        self._exit_points = set()

        self._execution_paths = list()

    @staticmethod
    def _load_function_list(function_list_file):
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', function_list_file)

        with open(file_name) as f:
            functions = f.read().splitlines()

        return functions

    @staticmethod
    def _get_android_override_input_methods():
        if not AndroidCallGraph._android_override_input_methods:
            AndroidCallGraph._android_override_input_methods = AndroidCallGraph._load_function_list("android_override_input_methods")

        return AndroidCallGraph._android_override_input_methods

    @staticmethod
    def _get_android_override_output_methods():
        if not AndroidCallGraph._android_override_output_methods:
            AndroidCallGraph._android_override_output_methods = AndroidCallGraph._load_function_list("android_override_output_methods")

        return AndroidCallGraph._android_override_output_methods

    @staticmethod
    def _get_android_edge_black_list():
        if not AndroidCallGraph._android_black_list_edges:
            file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "android_edge_black_list_extended")
            black_list_call_graph = AndroidCallGraph.from_loader(JavaCGLoader(file_name))
            AndroidCallGraph._android_black_list_edges = black_list_call_graph.edges

        return AndroidCallGraph._android_black_list_edges

    @staticmethod
    def _load_android_package_black_list():
        if not AndroidCallGraph._android_black_list_packages:
            AndroidCallGraph._android_black_list_packages = AndroidCallGraph._load_function_list("android_package_black_list")

        return AndroidCallGraph._android_black_list_packages

    def calculate_entry_and_exit_points(self):
        self._calculate_entry_and_exit_points()

        override_input_methods = [m.split('.')[-1] for m in AndroidCallGraph._get_android_override_input_methods()]
        entry_points_to_add = {n: n for n in self.call_graph.nodes() if n.function_name in override_input_methods}

        self._entry_points = AndroidCallGraph._merge_dicts(self._entry_points, entry_points_to_add)

        override_output_methods = [m.split('.')[-1] for m in AndroidCallGraph._get_android_override_output_methods()]
        exit_points_to_add = {n: n for n in self.call_graph.nodes() if n.function_name in override_output_methods}

        self._exit_points = AndroidCallGraph._merge_dicts(self._exit_points, exit_points_to_add)

    @staticmethod
    def _merge_dicts(x, y):
        """
            Given two dicts, merge them into a new dict as a shallow copy.
        """
        z = x.copy()
        z.update(y)
        return z

    def calculate_attack_surface_nodes(self):
        # Sub-graphing only those nodes connected to the attack surface
        attack_surface_nodes = set()

        for en in self.entry_points:
            attack_surface_nodes.add(en)
            for des in self.get_descendants(en):
                attack_surface_nodes.add(des)

        for ex in self.exit_points:
            attack_surface_nodes.add(ex)
            for anc in self.get_ancestors(ex):
                attack_surface_nodes.add(anc)

        self.attack_surface_graph = nx.subgraph(self.call_graph, attack_surface_nodes)

    def collapse_android_black_listed_edges(self):
        """
            Collapses all black listed edges into package nodes. It is important to call this meethod
            before any further manipulation (via the collapse_android_black_listed_packages method)
            because this way we make sure that all black listed edges get collapsed and we don't end up
            collapsing. Also, this way we ignore any input/output method that appears in the black listed
            nodes so that they don't appear in the metrics.
        """
        get_hash = lambda edge_to_hash: str(hash(edge_to_hash[0])) + str(hash(edge_to_hash[1]))

        black_listed_edges = AndroidCallGraph._get_android_edge_black_list()

        black_listed_edges = {get_hash(e): True for e in black_listed_edges}

        nodes_to_remove = set()
        edges_to_remove = []
        edges_to_add = []

        black_list_nodes = dict()

        for edge in self.call_graph.edges():
            caller, callee = edge

            caller_id = hash(caller)
            callee_id = hash(callee)
            edge_id = get_hash(edge)

            edge_is_in_black_list = edge_id in black_listed_edges

            if edge_is_in_black_list:

                edges_to_remove.append(edge)

                caller_package_node = Call(caller.package_name, "package_node", Environments.ANDROID)
                callee_package_node = Call(callee.package_name, "package_node", Environments.ANDROID)

                edges_to_add.append((caller_package_node, callee_package_node))

                # A node can only be removed if all its edges are in the black list.
                # After the collapse process, nodes whose edges are all in the black
                # list would be totally disconnected and substituted by their respective
                # package node. We need to remove those.

                if caller_id not in black_list_nodes:
                    black_list_nodes[caller_id] = {
                        'node': caller,
                        'all_edges_black_list': True
                    }

                if callee_id not in black_list_nodes:
                    black_list_nodes[callee_id] = {
                        'node': callee,
                        'all_edges_black_list': True
                    }

            if caller_id in black_list_nodes:
                if not edge_is_in_black_list:
                    black_list_nodes[caller_id]['all_edges_black_list'] = False

            if callee_id in black_list_nodes:
                if not edge_is_in_black_list:
                    black_list_nodes[callee_id]['all_edges_black_list'] = False

        for node_id, black_list_node in black_list_nodes.items():
            if black_list_node['all_edges_black_list']:
                nodes_to_remove.add(black_list_node['node'])

        self.call_graph.remove_edges_from(edges_to_remove)
        self.call_graph.remove_nodes_from(nodes_to_remove)

        self.call_graph.add_edges_from(edges_to_add)

        # Use this if planing to create a gml to open with gephi
        # for e in edges_to_add:
        #     edge_data = self.call_graph.get_edge_data(*e)
        #
        #     if not edge_data:
        #         self.call_graph.add_edge(*e, weight=1)
        #     else:
        #         self.call_graph.add_edge(*e, weight=edge_data["weight"] + 1)

    def collapse_android_black_listed_packages(self):

        black_listed_packages = AndroidCallGraph._load_android_package_black_list()

        nodes_to_remove = set()
        edges_to_remove = []

        edges_to_add = []

        for edge in self.call_graph.edges():
            caller, callee = edge

            if not (caller.is_input_function() or caller.is_output_function() or
                    callee.is_input_function() or callee.is_output_function()):

                if caller.package_name in black_listed_packages and callee.package_name in black_listed_packages:

                    edges_to_remove.append(edge)
                    nodes_to_remove.add(caller)
                    nodes_to_remove.add(callee)

                    edges_to_add.append((caller.package_name, callee.package_name))

                elif caller.package_name in black_listed_packages:

                    edges_to_remove.append(edge)
                    nodes_to_remove.add(caller)

                    edges_to_add.append((caller.package_name, callee))

                elif callee.package_name in black_listed_packages:

                    edges_to_remove.append(edge)
                    nodes_to_remove.add(callee)

                    edges_to_add.append((caller, callee.package_name))

        self.call_graph.remove_edges_from(edges_to_remove)
        self.call_graph.remove_nodes_from(nodes_to_remove)

        for e in edges_to_add:
            edge_data = self.call_graph.get_edge_data(*e)

            if not edge_data:
                self.call_graph.add_edge(*e, weight=1)
            else:
                self.call_graph.add_edge(*e, weight=edge_data["weight"] + 1)