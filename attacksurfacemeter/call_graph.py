import os
import statistics as stat

import networkx as nx

from attacksurfacemeter import utilities
from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments


class CallGraph():

    """Represents the Call Graph of a software system.

    Encapsulates a graph data structure where each node is a method or function
    call and an edge between nodes represents a caller - callee relationship.
    """

    def __init__(self, source, graph, load_errors=None, fragmentize=False):
        """CallGraph constructor.

        The call graph is split into strongly connected component subgraphs
        (referred to as fragments). The largest fragment is used as the call
        graph of the system.

        Parameters
        ----------
        source : str
            The source of the call graph that is represented by the CallGraph
            object. source is typically the absolute path of the file
            containing the call graph. On occasion, source may be the absolute
            path to the directory containing the source code of a system the
            call graph for which is to be generated.
        graph : networkx.DiGraph
            Internal representation of the graph data structure.

        Returns
        -------
        callgraph : CallGraph
            An instance of CallGraph.
        """
        self.source = source
        self.call_graph = graph
        self.load_errors = load_errors
        self.num_fragments = None
        self.monolithicity = None

        self._init()

        if fragmentize:
            fragments = utilities.get_fragments(graph)
            fragment = utilities.get_largest_fragment(fragments)

            self.num_fragments = len(fragments)
            self.monolithicity = len(fragment.nodes()) / len(graph.nodes())
            self.call_graph = fragment

    def _init(self):
        """Initialize private instance variables."""
        self._entry_points = None
        self._exit_points = None

        self._degree = None

    @classmethod
    def from_loader(cls, loader, fragmentize=False):
        """Construct a CallGraph using the given loader.

        Parameters
        ----------
        loader : BaseLoader or its derivative
            Loader used to load the call graph.

        Returns
        -------
        call_graph : CallGraph
            An instance of CallGraph representing a call graph loaded by the
            specified loader.
        """
        graph = loader.load_call_graph()
        load_errors = loader.errors

        return cls(loader.source, graph, load_errors, fragmentize)

    @classmethod
    def from_merge(cls, cflow_call_graph, gprof_call_graph, fragmentize=False):
        """Construct a CallGraph by merging cflow and gprof call graphs.

        Parameters
        ----------

        cflow_call_graph : CallGraph
            An instance of CallGraph representing a call graph generated using
            GNU cflow and loaded using CflowLoader.
        gprof_call_graph : CallGraph
            An instance of CallGraph representing a call graph generated using
            GNU gprof and loaded using GprofLoader.

        Returns
        -------
        call_graph : CallGraph
            An instance of CallGraph representing a call graph obtained by
            merging call graphs loaded by CflowLoader and GprofLoader.
        """
        source = "cflow: {0} - gprof: {1}".format(
            cflow_call_graph.source, gprof_call_graph.source
        )
        utilities.fix(cflow_call_graph, using=gprof_call_graph)

        graph = nx.DiGraph()

        # WARNING: The merge order CANNOT change. The value of the 'tested'
        #   attribute of the graph nodes works on the assumption that nodes
        #   from cflow are merged in first. Similarly, the weights of edges in
        #   gprof are lower than those in cflow and the merged graph is
        #   expected to have the edge weights match those from gprof.

        # Load nodes including any attributes that may be associated with them
        graph.add_nodes_from(cflow_call_graph.nodes)
        graph.add_nodes_from(gprof_call_graph.nodes)

        # Load edges including any attributes that may be associated with them
        graph.add_edges_from(cflow_call_graph.edges)
        graph.add_edges_from(gprof_call_graph.edges)

        load_errors = (
            cflow_call_graph.load_errors + gprof_call_graph.load_errors
        )

        return cls(source, graph, load_errors, fragmentize)

    @property
    def entry_points(self):
        """Return the list of entry points in the call graph.

        Parameters
        ----------
        None

        Returns
        -------
        entry_points : list
            A list of Call objects, each representing an entry point.
        """
        if self._entry_points is None:
            self._entry_points = list(
                nx.get_node_attributes(self.call_graph, 'entry').keys()
            )

        return self._entry_points

    @property
    def exit_points(self):
        """Return the list of exit points in the call graph.

        Parameters
        ----------
        None

        Returns
        -------
        exit_points : list
            A list of Call objects, each representing an exit point.
        """
        if self._exit_points is None:
            self._exit_points = list(
                nx.get_node_attributes(self.call_graph, 'exit').keys()
            )

        return self._exit_points

    @property
    def nodes(self):
        """Return the list of nodes present in the call graph.

        Parameters
        ----------
        None

        Returns
        -------
        nodes : list
            A list of two-tuples, (node, attributes), where node is an instance
            of Call representing a function/method in the call graph and
            attributes is a dictionary of attributes associated with the node.
        """
        return self.call_graph.nodes(data=True)

    @property
    def edges(self):
        """Return the list of edges present in the call graph.

        Parameters
        ----------
        None

        Returns
        -------
        edges : list
            A list of three-tuples, (source, destination, attributes), where
            source and destination are instances of Call representing the
            vertices of a directed edge from source to destination and
            attributes is a dictionary of attributes associated with the node.
        """
        return self.call_graph.edges(data=True)

    def get_degree(self, call=None):
        """Return the degree of a specific call.

        Parameters
        ----------
        call : Call, optional
            An instance of Call the degree of which will be calculated.

        Returns
        -------
        degree : int or dict
            The degree of call (if provided) or a dictionary keyed by call with
            degree as the value.
        """
        if self._degree is None:
            self._degree = self.call_graph.degree()

        if call:
            return self._degree[call]
        return self._degree

    def get_ancestors(self, call):
        """Return the list of ancestors of a specific call.

        The list of ancestors represent all functions/methods that invoke the
        given call.

        Parameters
        ----------
        call : Call
            An instance of Call the ancestors of which should be returned.

        Returns
        -------
        ancestors : list
            A list of Call objects, each of which represent the ancestor of the
            given call.
        """
        return list(nx.ancestors(self.call_graph, call))

    def get_descendants(self, call):
        """Return the list of descendants of a specific call.

        The list of descendants represent all functions/methods that the given
        call invokes.

        Parameters
        ----------
        call : Call
            An instance of Call the descendants of which should be returned.

        Returns
        -------
        descendants : list
            A list of Call objects, each of which represent the descendant of
            the given call.
        """
        return list(nx.descendants(self.call_graph, call))

    def get_entry_point_reachability(self, call):
        """Return the percentage of system accessible from an entry point.

        Parameters
        ----------
        call : Call
            An instance of Call representing an entry point.

        Returns
        -------
        reachability : float
            The calculated percentage.
        """
        if call not in self.entry_points:
            raise Exception('{0} must be an entry point.'.format(call))

        return len(self.get_descendants(call)) / len(self.nodes)

    def get_exit_point_reachability(self, call):
        """Return the percentage of system that accesses an exit point.

        Parameters
        ----------
        call : Call
            An instance of Call representing an exit point.

        Returns
        -------
        reachability : float
            The calculated percentage.
        """
        if call not in self.exit_points:
            raise Exception('{0} must be an exit point.'.format(call))

        return len(self.get_ancestors(call)) / len(self.nodes)

    def get_entry_surface_metrics(self, call):
        """Return entry surface metrics collected for a particular function.

        In addition to the metrics, a list of Call objects representing the
        entry points that the given function calls is also returned.

        Parameters
        ----------
        call : Call
            An object representing a function call in the call graph.

        Returns
        -------
        metrics : dictionary
            A dictionary with keys: points, proximity, and surface_coupling.
        """
        metrics = dict()
        points = list()
        proximity = list()
        surface_coupling = None

        if call in self.entry_points:
            proximity.append(0)
        else:
            for en in self.entry_points:
                if nx.has_path(self.call_graph, source=en, target=call):
                    points.append(en)
                    proximity.append(nx.shortest_path_length(
                        self.call_graph, source=en, target=call
                    ))

        metrics['points'] = points if points else None
        metrics['proximity'] = stat.mean(proximity) if proximity else None
        metrics['surface_coupling'] = len(points) if points else None

        return metrics

    def get_exit_surface_metrics(self, call):
        """Return exit surface metrics collected for a particular function.

        In addition to the metrics, a list of Call objects representing the
        exit points that the given function calls is also returned.

        Parameters
        ----------
        call : Call
            An object representing a function call in the call graph.

        Returns
        -------
        metrics : dictionary
            A dictionary with keys: points, proximity, and surface_coupling.
        """
        metrics = dict()
        points = list()
        proximity = list()
        surface_coupling = None

        if call in self.exit_points:
            proximity.append(0)
        else:
            for ex in self.exit_points:
                if nx.has_path(self.call_graph, source=call, target=ex):
                    points.append(ex)
                    proximity.append(nx.shortest_path_length(
                        self.call_graph, source=call, target=ex
                    ))

        metrics['points'] = points if points else None
        metrics['proximity'] = stat.mean(proximity) if proximity else None
        metrics['surface_coupling'] = len(points) if points else None

        return metrics

    def get_page_rank(self, call=None, primary=10000, secondary=1):
        """Compute the page rank of nodes in the call graph.

        Parameters
        ----------
        call : Call, optional
            An instance of Call the page rank for which will be returned.
        primary : int, optional
            A non-zero personalization value for a node that is an entry point
            or an exit point.
        secondary : int, optional
            A non-zero personalization value for a node that is not an entry
            point or an exit point.

        Returns
        -------
        page_rank : dict or float
            If call is specified, the page rank corresponding to call is
            returned else a dictionary containing the page rank of all nodes in
            the call graph is returned with the node being the key and the
            page rank being the value.
        """
        personalization = {
            n: primary
            if n in self.entry_points or n in self.exit_points
            else secondary
            for (n, _) in self.nodes
        }

        page_rank = nx.pagerank(
            self.call_graph,
            weight='weight',
            personalization=personalization
        )

        if call is not None:
            return page_rank[call]
        return page_rank

    def assign_page_rank(self, primary=10000, secondary=1, name='page_rank'):
        """Assign the page rank as an attribute of the node.

        Parameters
        ----------
        primary : int, optional
            A non-zero personalization value for a node that is an entry point
            or an exit point.
        secondary : int, optional
            A non-zero personalization value for a node that is not an entry
            point or an exit point.
        name : str, optional
            The name of the attribute that the page rank should be assigned to.

        Returns
        -------
        None
        """
        nx.set_node_attributes(
            self.call_graph,
            name,
            self.get_page_rank(primary=primary, secondary=secondary)
        )
