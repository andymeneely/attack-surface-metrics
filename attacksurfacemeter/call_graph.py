__author__ = 'kevin'

import statistics as stat
import networkx as nx
import os
# import matplotlib.pyplot as plt

from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments


class CallGraph():
    """
        Represents the Call Graph of a software system.

        Encapsulates a graph data structure where each node is a method/function call.

        Attributes:
            source: String that contains where the source code that this Call Graph represents comes from.
            call_graph: networkx.DiGraph. Internal representation of the graph data structure.
    """

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

        # self._entry_points = set()
        # self._exit_points = set()

        self._execution_paths = list()

        self._calculate_entry_and_exit_points()

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

    def _calculate_entry_and_exit_points(self):
        # Calculating the entry and exit points
        # self._entry_points = self._select_nodes(lambda n: any([s.is_input_function() for s
        #                                                            in self.call_graph.successors(n)]))

        # self._exit_points = self._select_nodes(lambda n: any([s.is_output_function() for s
        #                                                       in self.call_graph.successors(n)]))

        self._entry_points = {n: n for n in self.call_graph.nodes()
                              if any([s.is_input_function() for s in self.call_graph.successors(n)])}

        self._exit_points = {n: n for n in self.call_graph.nodes()
                             if any([s.is_output_function() for s in self.call_graph.successors(n)])}

    @classmethod
    def from_loader(cls, loader):
        """
            Constructs a CallGraph using the given loader.

            Args:
                loader: The BaseLoader derived class used for generation of the call graph.

            Returns:
                A new CallGraph instance containing the data obtained from the loader.
        """
        graph = loader.load_call_graph()
        errors = loader.error_messages

        return cls(loader.source, graph, errors)

    @classmethod
    def from_merge(cls, cflow_call_graph, gprof_call_graph):
        """
            Constructs a CallGraph from a merge of two existing CallGraphs.

            Args:
                cflow_call_graph: A CallGraph instance that represents a call graph generated using output from cflow.
                gprof_call_graph: A CallGraph instance that represents a call graph generated using output from gprof.

            Returns:
                A new CallGraph instance that contains the nodes and edges from both supplied call graphs.
        """
        source = "cflow: {0} - gprof: {1}".format(cflow_call_graph.source, gprof_call_graph.source)

        CallGraph._fix(cflow_call_graph, gprof_call_graph)
        
        graph = nx.DiGraph()

        # WARNING: The merge order CANNOT change. The value of the 'tested' 
        #   attribute of the graph nodes works on the assumption that nodes 
        #   from cflow are merged in first. Similarly, the weights of edges in
        #   gprof are lower than those in cflow and the merged graph is 
        #   expected to have the edge weights match those from gprof.

        # Load nodes including any attributes that may be associated with them
        graph.add_nodes_from(
            [
                (n, cflow_call_graph.call_graph.node[n]) 
                    for n in cflow_call_graph.nodes
            ]
        )
        graph.add_nodes_from(
            [
                (n, gprof_call_graph.call_graph.node[n]) 
                    for n in gprof_call_graph.nodes
            ]
        )

        # Load edges including any attributes that may be associated with them
        graph.add_edges_from([
            (u, v, d) 
                for (u, v, d) in cflow_call_graph.call_graph.edges(data=True)
        ])
        graph.add_edges_from([
            (u, v, d) 
                for (u, v, d) in gprof_call_graph.call_graph.edges(data=True)
        ])

        # Could come in handy!
        # nodes = gprof_call_graph.nodes
        #
        # lib_calls = [n for n in cflow_call_graph.nodes
        #              if n.is_library_call()]  # any([e for e in cflow_call_graph.edges if e[0] == n])
        #              # and n not in gprof_call_graph.nodes] Assume gprof doesn't identify library calls
        #
        # lib_call_edges = [e for e in cflow_call_graph.edges if e[1] in lib_calls]

        return cls(source, graph, cflow_call_graph.errors + gprof_call_graph.errors)

    def _select_nodes(self, predicate):
        """
            Selects the nodes in the graph for which predicate is True.

            Args:
                predicate: Function to use to determine which nodes to return from the entire Call Graph.
                    This function must receive a Call object as a parameter and return a Boolean that says
                    if the node meets the selection criteria.

            Returns:
                A List of all the nodes in the cal graph for which predicate is true.
        """
        return [n for n in self.call_graph.nodes() if predicate(n)]

    @staticmethod
    def _fix(call_graph, reference_call_graph):
        """
            Method attempts to a fix a call graph using a reference call 
            graph which is assumed to be more comprehensive than the one
            being fixed. The notion of fixing a call graph entails 
            identifying a node without function_signature and replacing it 
            with an identical node from the reference call graph that has a 
            function_signature.

            A call graph is required to be fixed to ensure compatibility of 
            equivalent nodes so that later when merging the two call graphs' 
            sets of edges, networkx doesn't think the cflow and gprof calls 
            are different only because one of them doesn't have a 
            function_signature associated to it.

            Implementation detail:
                networkx internally uses a dictionary as the data structure 
                to store nodes. Modifying an attribute that is used in the 
                computation of the object's hash will invalidate the hash 
                leaving the graph in an inconsistent state. Hence, fixing 
                nodes involves replacing existing nodes with their fixed 
                equivalents.
                
                More details at 
                http://networkx.lanl.gov/tutorial/tutorial.html

        Args:
                call_graph: A CallGraph instance that represents a call graph 
                to be fixed.
                reference_call_graph: A CallGraph instance that represents a 
                call graph assumed to be more comprehensive than call_graph.
        """
        nodes_to_replace = []

        for node in [n for n in call_graph.nodes if not n.function_signature]:
            reference_nodes = [n for n in reference_call_graph.nodes 
                if n.function_name == node.function_name]

            if len(reference_nodes) == 1:
                new_node = Call(node.function_name, 
                    reference_nodes[0].function_signature,
                    Environments.C)
                nodes_to_replace.append((node, new_node))

        for (before, after) in nodes_to_replace:
            call_graph.call_graph.add_node(after, 
                call_graph.call_graph.node[before])

            # Edges terminating at the node to be replaced
            for predecessor in call_graph.call_graph.predecessors(before):
                call_graph.call_graph.add_edge(
                    predecessor, after, 
                    call_graph.call_graph.get_edge_data(
                        predecessor, before
                    )
                )

            # Edges originating at the node to be replaced
            for successor in call_graph.call_graph.successors(before):
                call_graph.call_graph.add_edge(
                    after, successor,
                    call_graph.call_graph.get_edge_data(
                        before, successor
                    )
                )

            call_graph.call_graph.remove_node(before)

    def remove_function_name_only_calls(self):
        """
            Removes all the nodes in the call graph that represent calls for which the tools could not find the
            file where they were defined.
        """
        nodes_to_remove = self._select_nodes(lambda n: n.is_function_name_only())
        self.call_graph.remove_nodes_from(nodes_to_remove)
        self.attack_surface_graph.remove_nodes_from(nodes_to_remove)

    def remove_standard_library_calls(self):
        """
            Removes all the nodes in the call graph that represent calls to standard library functions.
        """
        nodes_to_remove = self._select_nodes(lambda n: n.is_standard_library_function() and n.is_function_name_only())
        self.call_graph.remove_nodes_from(nodes_to_remove)
        self.attack_surface_graph.remove_nodes_from(nodes_to_remove)

    @property
    def entry_points(self):
        """
            Returns all the Entry Points present in the Call Graph.
        
            Entry Points are functions that contain calls to input functions in the standard library.
            
            This is the list of the functions that are considered input functions in the C standard library:
            
            canonicalize_file_name, catgets, confstr, ctermid, ctermid, cuserid, dgettext, dngettext, fgetc,
            fgetc_unlocked, fgets, fgets_unlocked, fpathconf, fread, fread_unlocked, fscanf, getc, getchar,
            getchar_unlocked, getc_unlocked, get_current_dir_name, getcwd, getdelim, __getdelim, getdelim, getdents,
            getenv, gethostbyaddr, gethostbyname, gethostbyname2, gethostent, gethostid, getline, getline, getlogin,
            getlogin_r, getmsg, getopt, _getopt_internal, getopt_long, getopt_long_only, getpass, getpmsg, gets,
            gettext, getw, getwd, ngettext, pathconf, pread, pread64, ptsname, ptsname_r, read, readdir, readlink,
            readv, realpath, recv, recv_from, recvmesg, scanf, __secure_getenv, signal, sysconf, ttyname, ttyname_r,
            vfscanf, vscanf
            
        """
        return self._entry_points.values()

    @property
    def exit_points(self):
        """
            Returns all the Exit Points present in the Call Graph.
        
            Exit Points are functions that contain calls to output functions in the standard library.
            
            This is the list of the functions that are considered output functions in the C standard library:
            
            dprintf, fprintf, fputc, fputchar_unlocked, fputc_unlocked, fputs, fputs_unlocked, fwrite, fwrite_unlocked,
            perror, printf, psignal, putc, putchar, putc_unlocked, putenv, putmsg, putpmsg, puts, putw, pwrite,
            pwrite64, send, sendmsg, sendto, setenv, sethostid, setlogin, ungetc, vdprintf, vfprintf, vsyslog, write,
            writev
            
        """
        return self._exit_points.values()

    def is_entry_point(self, call):
        """
            Indicates whether a given call is an entry point

            Args:
                call: The call to test.

            Returns:
                A boolean indicating whether the given entry is an exit Point.
        """
        return call in self._entry_points

    def is_exit_point(self, call):
        """
            Indicates whether a given call is an exit point

            Args:
                call: The call to test.

            Returns:
                A boolean indicating whether the given call is an exit Point.
        """
        return call in self._exit_points

    @property
    def nodes(self):
        """
            Returns all the nodes present in the Call Graph.

            Each node is a Call object with the information of a specific function/method call.
        """
        return self.call_graph.nodes()

    @property
    def attack_surface_graph_nodes(self):
        """
            Returns all the nodes present in the Attack Surface Call Graph.

            Each node is a Call object with the information of a specific function/method call.
        """
        return self.attack_surface_graph.nodes()

    @property
    def edges(self):
        """
            Returns all the edges present in the Call Graph.

            Each edge is a 2-tuple of Call objects where the first member represents the caller and the second
            member represents the callee.
        """
        return self.call_graph.edges()

    # def save_png(self):
    #     """
    #         Creates a graphical representation of the Call Graph and saves it.
    #
    #         The created image file is a png and is saved in the current directory with the name of the folder where
    #         the source code for which the Call Graph was generated is located.
    #     """
    #     nx.draw(self.call_graph)
    #     plt.savefig(os.path.basename(os.path.normpath(self.source_dir)) + ".png")
    #     plt.clf()

    def save_gml(self):
        nx.write_gml(self.call_graph, os.path.basename(os.path.normpath(self.source)) + ".gml")
    
    def shortest_path(self, source, target):
        """
            Computes the shortest path between source and target.

            Args:
                source: The start point of the calculated path.
                
            Returns:
                A List of nodes representing the path from source to target.
                
            Raises:
                networkx.exception.NetworkXNoPath: There is no path between source and target.
                networkx.exception.NetworkXError: source or target or both are not present in the Call Graph.
        """
        return nx.shortest_path(self.call_graph, source, target)

    @property
    def execution_paths(self):
        """
            Returns all the Execution Paths present in the Call Graph.

            An Execution Path is every possible path in the Call Graph that begins in an Entry Point and ends
            in an Exit Point.

            Returns:
                A List where each element is a List of Call objects representing the paths in the Call Graph.
        """
        if not self._execution_paths:
            paths = []

            for entry_point in self.entry_points:
                for exit_point in self.exit_points:
                    if nx.has_path(self.call_graph, entry_point, exit_point):
                        paths.append(nx.shortest_path(self.call_graph, entry_point, exit_point))

            self._execution_paths = paths

        return self._execution_paths

    def get_execution_paths_for(self, call):
        """
            Returns all the Execution Paths in which call appears.

            Args:
                call: A Call object for which Execution Paths want to be found.

            Returns:
                A List where each element is a List of Call objects representing the paths in the Call Graph that
                call is part of.
        """
        return [path for path in self.execution_paths if call in path]

    @property
    def avg_execution_path_length(self):
        """
            Returns the average length of all the Execution Paths in the Call Graph.

            Returns:
                An Float representing the calculated value.
        """
        return stat.mean([len(p) for p in self.execution_paths])

    @property
    def median_execution_path_length(self):
        """
            Returns the median length of all the Execution Paths in the Call Graph.

            Returns:
                An Float representing the calculated value.
        """
        return stat.median([len(p) for p in self.execution_paths])

    def _get_distances(self, distance_calculator, call, paths=None):
        """
            Returns tne distance from call to a given point in the provided or all of the Execution Paths.

            Args:
                distance_calculator: Function that will be used to calculate the distance. The function must recieve
                    a Call instance as a first parameter and an Execution Path (List of Calls) as the second parameter
                    and return an Int that represents the calculated distance.
                call: A Call instance for which the distances will be calculated.
                paths: Optional List of Lists of Call instances that represent the Execution Paths in which call's
                    distance will be calculated. If paths is not provided, the distances will be calculated for all
                    the Execution Paths where call appears. If call is not present in an Execution Path, the distance
                    for that specific path will be None.

            Returns:
                A List of Dictionaries with a 'path' member that contains an Execution Path and a 'distance' member
                that contains the distance calculated for call for the Execution Path contained in the 'path' member.

        """
        distances = list()

        if paths:
            paths_to_search = paths
        else:
            paths_to_search = self.get_execution_paths_for(call)

        for path in paths_to_search:
            try:
                distance_to_point = distance_calculator(call, path)
            except:
                distance_to_point = None

            distances.append({'path': path, 'distance': distance_to_point})

        return distances

    def get_distance_to_entry_point(self, call, paths=None):
        """
            Returns the distance of call to the Entry Point in the provided or all of the Execution Paths.

            Args:
                call: A Call instance for which the distances will be calculated.
                paths: Optional List of Lists of Call instances that represent the Execution Paths in which call's
                    distance to the Entry Point will be calculated. If call is not present in an Execution Path
                    provided in paths, the distance for that specific path will be None. If paths is not provided,
                    the distances will be calculated for all the Execution Paths where call appears.

            Returns:
                A List of Dictionaries with a 'path' member that contains an Execution Path and a 'distance' member
                that contains the distance of call to the Entry Point in the Execution Path contained in the
                'path' member.
        """
        calculator = lambda c, p: p.index(c)
        return self._get_distances(calculator, call, paths)

    def get_distance_to_exit_point(self, call, paths=None):
        """
            Returns the distance of call to the Exit Point in the provided or all of the Execution Paths.

            Args:
                call: A Call instance for which the distances will be calculated.
                paths: Optional List of Lists of Call instances that represent the Execution Paths in which call's
                    distance to the Exit Point will be calculated. If call is not present in an Execution Path
                    provided in paths, the distance for that specific path will be None. If paths is not provided,
                    the distances will be calculated for all the Execution Paths where call appears.

            Returns:
                A List of Dictionaries with a 'path' member that contains an Execution Path and a 'distance' member
                that contains the distance of call to the Exit Point in the Execution Path contained in the
                'path' member.
        """
        calculator = lambda c, p: len(p) - p.index(c) - 1
        return self._get_distances(calculator, call, paths)

    _closeness = dict()

    def get_closeness(self, call=None):
        """
            Calculates the Closeness of call.

            The Closeness of a node represents how close it is to all the other nodes in a graph. It is roughly
            the average of the lengths of all the shortest paths from a specific node to all other nodes.
            Closeness is defined more formally in:

            http://networkx.github.io/documentation/networkx-1.9/reference/generated/
            networkx.algorithms.centrality.closeness_centrality.html

            and

            Freeman, L.C., 1979. Centrality in networks: I. Conceptual clarification. Social Networks 1, 215–239.
            http://leonidzhukov.net/hse/2013/socialnetworks/papers/freeman79-centrality.pdf

            Args:
                call: An optional Call instance for which the Closeness will be calculated. If call is not provided,
                    Closeness will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns a Float that represents the Closeness of call. If not, returns a
                dictionary with every Call in the Call Graph with their respective Closenesses.
        """
        if not self._closeness:
            self._closeness = nx.closeness_centrality(self.call_graph)

        if call:
            return self._closeness[call]
        else:
            return self._closeness

    @property
    def median_closeness(self):
        return stat.median([closeness for k, closeness in self.get_closeness().items()])

    @property
    def average_closeness(self):
        return stat.mean([closeness for k, closeness in self.get_closeness().items()])

    _betweenness = dict()

    def get_betweenness(self, call=None):
        """
            Calculates the Betweenness of call.

            The Betweenness of a node represents how between it is to all the other pairs of nodes in a graph. It is
            roughly the proportion of how many of all the shortest paths between every pair of nodes pass through a
            given node. Betweenness is defined more formally in:

            http://networkx.github.io/documentation/networkx-1.9/reference/generated/
            networkx.algorithms.centrality.betweenness_centrality.html

            and

            Brandes U., 2001, A Faster Algorithm for Betweenness Centrality. Journal of Mathematical Sociology 25(2):163-177.
            http://www.inf.uni-konstanz.de/algo/publications/b-fabc-01.pdf

            Args:
                call: An optional Call instance for which the Betweenness will be calculated. If call is not provided,
                    Betweenness will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns a Float that represents the Betweenness of call. If not, returns a
                dictionary with every Call in the Call Graph with their respective Betweennesses.
        """
        if not self._betweenness:
            self._betweenness = nx.betweenness_centrality(self.call_graph)

        if call:
            return self._betweenness[call]
        else:
            return self._betweenness

    @property
    def median_betweenness(self):
        return stat.median([betweenness for k, betweenness in self.get_betweenness().items()])

    @property
    def average_betweenness(self):
        return stat.mean([betweenness for k, betweenness in self.get_betweenness().items()])

    # Reconsider this. Maybe clustering is not all that useful in terms of call graph.
    def average_clustering(self, nodes):
        """
            Returns the average clustering coefficient of the given nodes.
        
            Args:
                nodes: A List of Calls whose average clustering coefficient will be calculated.
                
            Returns:
                An Int that represents the average clustering coefficient of the given nodes.
        """
        return nx.average_clustering(self.call_graph.to_undirected(), nodes)

    # Reconsider this. Maybe clustering is not all that useful in terms of call graph.
    @property
    def entry_points_clustering(self):
        """
            Returns the average clustering coefficient of the Entry Points.

            Returns:
                An Int that represents the average clustering coefficient of the Entry Points.
        """
        return self.average_clustering(self.entry_points)

    # Reconsider this. Maybe clustering is not all that useful in terms of call graph.
    @property
    def exit_points_clustering(self):
        """
            Returns the average clustering coefficient of the Exit Points.

            Returns:
                An Int that represents the average clustering coefficient of the Exit Points.
        """
        return self.average_clustering(self.exit_points)

    _degree_centrality = dict()

    def get_degree_centrality(self, call=None):
        """
            Returns the degree centrality of a given Call

            The degree centrality is the fraction of other nodes that a specific node is connected to.

            Args:
                call: An optional Call instance for which the degree centrality will be calculated. If call is not
                    provided, degree centrality will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns a Float that represents the degree centrality of call. If not, returns a
                dictionary with every Call in the Call Graph with their respective degree centrality.
        """
        if not self._degree_centrality:
            self._degree_centrality = nx.degree_centrality(self.call_graph)

        if call:
            return self._degree_centrality[call]
        else:
            return self._degree_centrality

    @property
    def median_degree_centrality(self):
        return stat.median([degree_centrality for k, degree_centrality in self.get_degree_centrality().items()])

    @property
    def average_degree_centrality(self):
        return stat.mean([degree_centrality for k, degree_centrality in self.get_degree_centrality().items()])

    _in_degree_centrality = dict()

    def get_in_degree_centrality(self, call=None):
        """
            Returns the in degree centrality of a given Call

            The in degree centrality is the fraction of other nodes that a specific node's incoming edges
            are connected to.

            Args:
                call: An optional Call instance for which the in degree centrality will be calculated. If call is not
                    provided, in degree centrality will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns a Float that represents the in degree centrality of call. If not, returns
                a dictionary with every Call in the Call Graph with their respective in degree centrality.
        """
        if not self._in_degree_centrality:
            self._in_degree_centrality = nx.in_degree_centrality(self.call_graph)

        if call:
            return self._in_degree_centrality[call]
        else:
            return self._in_degree_centrality

    @property
    def median_in_degree_centrality(self):
        return stat.median([in_degree_centrality for k, in_degree_centrality in self.get_in_degree_centrality().items()])

    @property
    def average_in_degree_centrality(self):
        return stat.mean([in_degree_centrality for k, in_degree_centrality in self.get_in_degree_centrality().items()])

    _out_degree_centrality = dict()

    def get_out_degree_centrality(self, call=None):
        """
            Returns the out degree centrality of a given Call

            The out degree centrality is the fraction of other nodes that a specific node's outgoing edges
            are connected to.

            Args:
                call: An optional Call instance for which the out degree centrality will be calculated. If call is not
                    provided, out degree centrality will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns a Float that represents the out degree centrality of call. If not, returns
                a dictionary with every Call in the Call Graph with their respective out degree centrality.
        """
        if not self._out_degree_centrality:
            self._out_degree_centrality = nx.out_degree_centrality(self.call_graph)

        if call:
            return self._out_degree_centrality[call]
        else:
            return self._out_degree_centrality

    @property
    def median_out_degree_centrality(self):
        return stat.median([out_degree_centrality for k, out_degree_centrality in self.get_out_degree_centrality().items()])

    @property
    def average_out_degree_centrality(self):
        return stat.mean([out_degree_centrality for k, out_degree_centrality in self.get_out_degree_centrality().items()])

    _degree = dict()

    def get_degree(self, call=None):
        """
            Returns the degree of a given Call.

            The degree of a node is the number of edges it has.

            Args:
                call: An optional Call instance for which the degree will be calculated. If call is not
                    provided, degree will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns an Int that represents the degree of call. If not, returns
                a dictionary with every Call in the Call Graph with their respective degree.
        """
        if not self._degree:
            self._degree = self.call_graph.degree()

        if call:
            return self._degree[call]
        else:
            return self._degree

    @property
    def median_degree(self):
        return stat.median([degree for k, degree in self.get_degree().items()])

    @property
    def average_degree(self):
        return stat.mean([degree for k, degree in self.get_degree().items()])

    _in_degree = dict()

    def get_in_degree(self, call=None):
        """
            Returns the in degree of a given Call.

            The in degree of a node is the number of incoming edges it has.

            Args:
                call: An optional Call instance for which the in degree will be calculated. If call is not
                    provided, in degree will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns an Int that represents the in degree of call. If not, returns
                a dictionary with every Call in the Call Graph with their respective in degree.
        """
        if not self._in_degree:
            self._in_degree = self.call_graph.in_degree()

        if call:
            return self._in_degree[call]
        else:
            return self._in_degree

    @property
    def median_in_degree(self):
        return stat.median([in_degree for k, in_degree in self.get_in_degree().items()])

    @property
    def average_in_degree(self):
        return stat.mean([in_degree for k, in_degree in self.get_in_degree().items()])

    _out_degree = dict()

    def get_out_degree(self, call=None):
        """
            Returns the out degree of a given Call.

            The out degree of a node is the number of incoming edges it has.

            Args:
                call: An optional Call instance for which the out degree will be calculated. If call is not
                    provided, out degree will be calculated for every Call in the Call Graph.

            Returns:
                If call is provided, returns an Int that represents the out degree of call. If not, returns
                a dictionary with every Call in the Call Graph with their respective out degree.
        """
        if not self._out_degree:
            self._out_degree = self.call_graph.out_degree()

        if call:
            return self._out_degree[call]
        else:
            return self._out_degree

    @property
    def median_out_degree(self):
        return stat.median([out_degree for k, out_degree in self.get_out_degree().items()])

    @property
    def average_out_degree(self):
        return stat.mean([out_degree for k, out_degree in self.get_out_degree().items()])

    # This doesn't make much sense for directed graphs
    # def get_eccentricity(self, call=None):
    #     if call:
    #         return nx.eccentricity(self.call_graph.to_undirected())[call]
    #     else:
    #         return nx.eccentricity(self.call_graph.to_undirected())

    def get_descendants(self, call):
        """
            Returns all the descendants of a given Call.

            The descendants are all the nodes that can be reached from a specific node.

            Args:
                call: A Call instance whose descendants will be returned.

            Returns:
                A List of Call objects that represent all of call's descendants.
        """
        return list(nx.descendants(self.call_graph, call))

    def get_descendants_within(self, call, depth=1):
        """
            Returns all the descendants of a given Call reachable within a specified number
            of hops from Call.

            Args:
                call: A Call instance whose descendants will be returned.
                depth: Number of hops to stop looking for descendants.

            Returns:
                A List of Call objects that represent all of call's descendants reachable
                within a specified depth.
        """
        descendants = set()
        for descendant in nx.single_source_shortest_path(self.call_graph, call, cutoff=depth):
            if descendant.function_name != call.function_name:
                descendants.add(descendant)

        return list(descendants)

    def get_ancestors(self, call):
        """
            Returns all the ancestors of a given Call.

            The ancestors are all the nodes that can reach a specific node.

            Args:
                call: A Call instance whose ancestors will be returned.

            Returns:
                A List of Call objects that represent all of call's ancestors.
        """
        return list(nx.ancestors(self.call_graph, call))

    def _ratio_of_containment(self, contained, container):
        """
            Calculates the ratio of how many elements of contained are present in contained.

            Args:
                contained: List of Call objects that will be tested for presence in container.
                container: List of Call objects that will be tested to contain the elements of contained.

            Returns:
                A Float representing the calculated ratio of contained that are present in container.
        """
        if len(contained) == 0:
            return 0.0

        numerator = len(self._contained_in(contained, container))
        denominator = len(contained)

        return numerator/denominator

    def _contained_in(self, contained, container):
        """
            Returns all the elements of contained that are present in container.
            
            Args:
                contained: List of Call objects that will be tested for presence in container.
                container: List of Call objects that will be tested to contain the elements of contained.

            Returns:
                A List of Call call objects that represent a the subset of contained that is present in container.
        """
        return [c for c in contained if c in container]

    def get_descendant_entry_points(self, call):
        """
            Returns the descendants of call that are Entry Points.

            Args:
                call: A Call object whose descendants are going to be searched for Entry Points.
                
            Returns:
                A List of Call objects that contain all the descendants of call that are Entry Points.
        """
        return self._contained_in(self.get_descendants(call), self.entry_points)

    def get_descendant_exit_points(self, call):
        """
            Returns the descendants of call that are Exit Points.

            Args:
                call: A Call object whose descendants are going to be searched for Exit Points.

            Returns:
                A List of Call objects that contain all the descendants of call that are Exit Points.
        """
        return self._contained_in(self.get_descendants(call), self.exit_points)

    def get_ancestor_entry_points(self, call):
        """
            Returns the ancestors of call that are Entry Points.

            Args:
                call: A Call object whose ancestors are going to be searched for Entry Points.

            Returns:
                A List of Call objects that contain all the ancestors of call that are Entry Points.
        """
        return self._contained_in(self.get_ancestors(call), self.entry_points)

    def get_ancestor_exit_points(self, call):
        """
            Returns the ancestors of call that are Exit Points.

            Args:
                call: A Call object whose ancestors are going to be searched for Exit Points.

            Returns:
                A List of Call objects that contain all the ancestors of call that are Exit Points.
        """
        return self._contained_in(self.get_ancestors(call), self.exit_points)

    def get_descendants_entry_point_ratio(self, call):
        """
            Returns the ratio of descendants of call that are Entry Points.

            Args:
                call: A Call object whose descendants are going to be searched for Entry Points.

            Returns:
                A Float that represents the calculated ratio.
        """
        return self._ratio_of_containment(self.get_descendants(call),
                                          self.entry_points)

    def get_descendants_exit_point_ratio(self, call):
        """
            Returns the ratio of descendants of call that are Exit Points.

            Args:
                call: A Call object whose descendants are going to be searched for Exit Points.

            Returns:
                A Float that represents the calculated ratio.
        """
        return self._ratio_of_containment(self.get_descendants(call),
                                          self.exit_points)

    def get_ancestors_entry_point_ratio(self, call):
        """
            Returns the ratio of ancestors of call that are Entry Points.

            Args:
                call: A Call object whose ancestors are going to be searched for Entry Points.

            Returns:
                A Float that represents the calculated ratio.
        """
        return self._ratio_of_containment(self.get_ancestors(call),
                                          self.entry_points)

    def get_ancestors_exit_point_ratio(self, call):
        """
            Returns the ratio of ancestors of call that are Exit Points.

            Args:
                call: A Call object whose ancestors are going to be searched for Exit Points.

            Returns:
                A Float that represents the calculated ratio.
        """
        return self._ratio_of_containment(self.get_ancestors(call),
                                          self.exit_points)

    # TODO: Converting the graph to undirected is not good for our purposes.
    # Calls to standard libraries are very common and by those, must clusters (components)
    # will be connected.
    def is_connected(self):
        return nx.is_connected(self.call_graph.to_undirected())

    def get_clusters(self):
        return nx.connected_components(self.call_graph.to_undirected())

    def get_entry_point_reachability(self, call):
        """
            Returns the ratio of descendants of a call to the total number of nodes in the call graph.

            Args:
                call: A Call object that represents an Entry Point.

            Returns:
                A Float that represents the calculated ratio.
        """
        return len(self.get_descendants(call)) / len(self.attack_surface_graph_nodes)

    def get_exit_point_reachability(self, call):
        """
            Returns the ratio of ancestors of a call to the total number of nodes in the call graph.

            Args:
                call: A Call object that represents an Exit Point.

            Returns:
                A Float that represents the calculated ratio.
        """
        return len(self.get_ancestors(call)) / len(self.attack_surface_graph_nodes)

    def get_shallow_entry_point_reachability(self, call, depth=1):
        """
            Returns the ratio of descendants of a call that are reachable within a specified depth to
            the total number of nodes in the call graph.

            Args:
                call: A Call object that represents an Entry Point.

            Returns:
                A Float that represents the calculated ratio.
        """

        return len(self.get_descendants_within(call, depth)) / len(self.attack_surface_graph_nodes)

    def get_entry_surface_metrics(self, call):
        """
            Returns a list of Call objects and two function-level metrics associated with the entry surface
                of a software system:
                Proximity - average of the length of shortest paths between all entry points and a specified
                call, if a path exists.
                If there are multiple paths of the same shortest length then all those paths are considered
                proximity is computed.
                Surface Coupling - sum of number of shortest paths from each entry point to a specified call.

            Args:
                call: A Call object that represents a function call in the call graph.

            Returns:
                A dictionary with the keys "points", "proximity", and "surface coupling". Possible values are:
                    0 for proximity and None for surface coupling, if the Call object is an Entry Point.
                    None for both, if there is no path between any of the entry points and the Call object.
                    Otherwise, a decimal (positive integer) value that represents the calculated proximity
                    (surface coupling).
                The dictionary value corresponding to the key "points" is a list of Call objects representing
                    the entry points that the given call gets input from.
        """
        entry_points = proximity_to_entry = surface_coupling_with_entry = None
        if call in self.entry_points:
            proximity_to_entry = 0
        else:
            points = []
            entry_path_lengths = []
            num_paths = 0
            for en in self.entry_points:
                if nx.has_path(self.call_graph, source=en, target=call):
                    points.append(en)
                    for shortest_path in nx.all_shortest_paths(self.call_graph, source=en, target=call):
                        num_paths += 1
                        entry_path_lengths.append(len(shortest_path) - 1) # Path length is one less than the number of nodes

            if entry_path_lengths and num_paths != 0:
                entry_points = points
                proximity_to_entry = stat.mean(entry_path_lengths)
                surface_coupling_with_entry = num_paths

        return {'points': entry_points, 'proximity': proximity_to_entry, 'surface_coupling': surface_coupling_with_entry}

    def get_exit_surface_metrics(self, call):
        """
            Returns a list of Call objects and two function-level metrics associated with the exit surface
                of a software system:
                Proximity - average of the length of shortest paths between a specfied call and all exit points,
                if a path exists.
                If there are multiple paths of the same shortest length then all those paths are considered
                proximity is computed.
                Surface Coupling - sum of number of shortest paths to each exit point from a specified call.

            Args:
                call: A Call object that represents a function call in the call graph.

            Returns:
                A dictionary with the keys "points", "proximity", and "surface coupling". Possible values are:
                    0 for proximity and None for surface coupling, if the Call object is an Exit Point.
                    None for both, if there is no path between the Call object and any of the exit points.
                    Otherwise, a decimal (positive integer) value that represents the calculated proximity
                    (surface coupling).
                The dictionary value corresponding to the key "points" is a list of Call objects representing
                    the exit points that the given call outputs data through.
        """
        exit_points = proximity_to_exit = surface_coupling_with_exit = None
        if call in self.exit_points:
            proximity_to_exit = 0
        else:
            points = []
            exit_path_lengths = []
            num_paths = 0
            for ex in self.exit_points:
                if nx.has_path(self.call_graph, source=call, target=ex):
                    points.append(ex)
                    for shortest_path in nx.all_shortest_paths(self.call_graph, source=call, target=ex):
                        num_paths += 1
                        exit_path_lengths.append(len(shortest_path) - 1) # Path length is one less than the number of nodes

            if exit_path_lengths and num_paths != 0:
                exit_points = points
                proximity_to_exit = stat.mean(exit_path_lengths)
                surface_coupling_with_exit = num_paths

        return {'points': exit_points, 'proximity': proximity_to_exit, 'surface_coupling': surface_coupling_with_exit}

    _entry_page_rank = dict()
    _entry_page_rank_per = dict()

    def get_entry_page_rank(self, call=None, primary=10000, secondary=1):
        """
            Computes the page rank of nodes in the call graph with higher
            preference to entry points.

            Args:
                call: A Call object the page rank for which will be returned.
                    Default is None.
                primary: A non-zero personalization value for a node that
                    is an entry point. Default is 10000.
                secondary: A non-zero personalization value for a node that
                    is not an entry point. Default is 1.

            Returns:
                If call is specified, the page rank corresponding to call is
                returned else a dictionary containing the page rank of all
                nodes in the call graph is returned with the node being the
                key and the page rank being the value.
        """
        if not self._entry_page_rank_per:
            self._entry_page_rank_per = {
                n: primary if n in self.entry_points else secondary
                for n in self.nodes
            }

        # if not call:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)
        # else:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)[call]

        if not self._entry_page_rank:
            self._entry_page_rank = nx.pagerank(self.call_graph, weight='weight', personalization=self._entry_page_rank_per)

        if call:
            return self._entry_page_rank[call]
        else:
            return self._entry_page_rank

    _exit_page_rank = dict()
    _exit_page_rank_per = dict()

    def get_exit_page_rank(self, call=None, primary=10000, secondary=1):
        """
            Computes the page rank of nodes in the call graph with higher
            preference to exit points.

            Args:
                call: A Call object the page rank for which will be returned.
                    Default is None.
                primary: A non-zero personalization value for a node that
                    is an exit point. Default is 10000.
                secondary: A non-zero personalization value for a node that
                    is not an exit point. Default is 1.

            Returns:
                If call is specified, the page rank corresponding to call is
                returned else a dictionary containing the page rank of all
                nodes in the call graph is returned with the node being the
                key and the page rank being the value.
        """
        if not self._exit_page_rank_per:
            self._exit_page_rank_per = {
                n: primary if n in self.exit_points else secondary
                for n in self.nodes
            }

        # if not call:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)
        # else:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)[call]

        if not self._exit_page_rank:
            self._exit_page_rank = nx.pagerank(self.call_graph, weight='weight', personalization=self._exit_page_rank_per)

        if call:
            return self._exit_page_rank[call]
        else:
            return self._exit_page_rank

    _page_rank = dict()
    _page_rank_per = dict()

    def get_page_rank(self, call=None, primary=10000, secondary=1):
        """
            Computes the page rank of nodes in the call graph.

            Args:
                call: A Call object the page rank for which will be returned.
                    Default is None.
                primary: A non-zero personalization value for a node that
                    is an entry point or an exit point. Default is 10000.
                secondary: A non-zero personalization value for a node that
                    is not an entry point or an exit point. Default is 1.

            Returns:
                If call is specified, the page rank corresponding to call is
                returned else a dictionary containing the page rank of all
                nodes in the call graph is returned with the node being the
                key and the page rank being the value.
        """
        if not self._page_rank_per:
            self._page_rank_per = {
                n: primary if n in self.entry_points or n in self.exit_points
                    else secondary
                for n in self.nodes
            }

        # if not call:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)
        # else:
        #     return nx.pagerank(self.call_graph, weight='weight',
        #         personalization=per)[call]

        if not self._page_rank:
            self._page_rank = nx.pagerank(self.call_graph, weight='weight', personalization=self._page_rank_per)

        if call:
            return self._page_rank[call]
        else:
            return self._page_rank

    def assign_page_rank(self, cflow_edge_weight, gprof_edge_weight, 
        primary, secondary, name='page_rank'):
        """
            Assigns the page rank of each node as an attribute of the node.

            Args:
                cflow_edge_weight: The weight of an edge from the cflow call
                    graph.
                gprof_edge_weight: The weight of an edge from the gprof call
                    graph.
                primary: A non-zero personalization value for a node that 
                    is an entry point or an exit point.
                secondary: A non-zero personalization value for a node that 
                    is not an entry point or an exit point.
                name: The name of the attribute that the page rank should be 
                    assigned to. Default is 'page_rank'.
        """
        # Assign weights to edges before computing page rank
        for (u, v, d) in self.call_graph.edges(data=True):
            self.call_graph.edge[u][v]['weight'] = cflow_edge_weight
            if 'gprof' in d:
                self.call_graph.edge[u][v]['weight'] = gprof_edge_weight

        nx.set_node_attributes(self.call_graph, name, 
            self.get_page_rank(primary=primary, secondary=secondary))
