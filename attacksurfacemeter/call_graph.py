__author__ = 'kevin'

import statistics as stat
import networkx as nx
# import matplotlib.pyplot as plt


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

        self._entry_points = set()
        self._exit_points = set()

        self._execution_paths = list()

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
                A new CallGraph instance that contains the nodes and edges from both suppplied call graphs.
        """
        source = "cflow: {0} - gprof: {1}".format(cflow_call_graph.source, gprof_call_graph.source)

        graph = nx.DiGraph()

        # Combine both collections an eliminate duplicates
        # nodes = cflow_call_graph.nodes
        # nodes.extend([n for n in gprof_call_graph.nodes if n not in nodes])

        # CallGraph._populate_graph(graph, nodes, cflow_call_graph.edges)
        # CallGraph._populate_graph(graph, nodes, gprof_call_graph.edges)

        nodes = gprof_call_graph.nodes

        lib_calls = [n for n in cflow_call_graph.nodes
                     if n.is_library_call()]  # any([e for e in cflow_call_graph.edges if e[0] == n])
                     # and n not in gprof_call_graph.nodes] Assume gprof doesn't identify library calls

        nodes.extend(lib_calls)

        lib_call_edges = [e for e in cflow_call_graph.edges if e[1] in lib_calls]

        CallGraph._populate_graph(graph, nodes, gprof_call_graph.edges)
        CallGraph._populate_graph(graph, nodes, lib_call_edges)

        return cls(source, graph)

    @staticmethod
    def _find_edge_in_nodes(edge, nodes):
        """
            Finds the caller and callee of a given call graph edge in a given set of nodes.

            Args:
                edge: A 2-tuple containing a caller and a callee that are going to be searched for. The first element
                    of the tuple is the caller and the second element is the callee.

            Returns:
                caller: A Call object from the given set of nodes that equals to the caller in the given edge.
                callee: A Call object from the given set of nodes that equals to the callee in the given edge.
        """
        caller = [n for n in nodes if edge[0] == n][0]
        callee = [n for n in nodes if edge[1] == n][0]

        # caller = None
        # callee = None
        #
        # for n in nodes:
        #     if caller is None or callee is None:
        #         if n == edge[0]:
        #             caller = n
        #         if n == edge[1]:
        #             callee = n
        #     else:
        #         break

        # nodes_in_edge = [n for n in nodes if n == edge[0] or n == edge[1]]
        #
        # caller = [n for n in nodes_in_edge if edge[0] == n][0]
        # callee = [n for n in nodes_in_edge if edge[1] == n][0]

        return caller, callee

    @staticmethod
    def _populate_graph(graph, nodes, edges):
        """
            Populates an empty graph with the given nodes and edges.

            Args:
                graph: A networkx.DiGraph instance with no nodes.
                nodes: A collection of Call objects that will serve as nodes for the call graph.
                edges: A collection of 2-tuples of Call that will serve as edges for the call graph.
        """
        for e in edges:
            caller, callee = CallGraph._find_edge_in_nodes(e, nodes)
            graph.add_edge(caller, callee)

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
        if not self._entry_points:
            self._entry_points = self._select_nodes(lambda n: any([s.is_input_function() for s
                                                                   in self.call_graph.successors(n)]))
        return self._entry_points

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
        if not self._exit_points:
            self._exit_points = self._select_nodes(lambda n: any([s.is_output_function() for s
                                                                  in self.call_graph.successors(n)]))
        return self._exit_points

    @property
    def nodes(self):
        """
            Returns all the nodes present in the Call Graph.

            Each node is a Call object with the information of a specific function/method call.
        """
        return self.call_graph.nodes()

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
        return nx.closeness_centrality(self.call_graph, call)

    @property
    def median_closeness(self):
        return stat.median([closeness for k, closeness in self.get_closeness().items()])

    @property
    def average_closeness(self):
        return stat.mean([closeness for k, closeness in self.get_closeness().items()])
    
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
        betweennesses = nx.betweenness_centrality(self.call_graph)

        if call:
            return betweennesses[call]
        else:
            return betweennesses

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
        degrees = nx.degree_centrality(self.call_graph)

        if call:
            return degrees[call]
        else:
            return degrees

    @property
    def median_degree_centrality(self):
        return stat.median([degree_centrality for k, degree_centrality in self.get_degree_centrality().items()])

    @property
    def average_degree_centrality(self):
        return stat.mean([degree_centrality for k, degree_centrality in self.get_degree_centrality().items()])

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
        degrees = nx.in_degree_centrality(self.call_graph)

        if call:
            return degrees[call]
        else:
            return degrees

    @property
    def median_in_degree_centrality(self):
        return stat.median([in_degree_centrality for k, in_degree_centrality in self.get_in_degree_centrality().items()])

    @property
    def average_in_degree_centrality(self):
        return stat.mean([in_degree_centrality for k, in_degree_centrality in self.get_in_degree_centrality().items()])

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
        degrees = nx.out_degree_centrality(self.call_graph)

        if call:
            return degrees[call]
        else:
            return degrees

    @property
    def median_out_degree_centrality(self):
        return stat.median([out_degree_centrality for k, out_degree_centrality in self.get_out_degree_centrality().items()])

    @property
    def average_out_degree_centrality(self):
        return stat.mean([out_degree_centrality for k, out_degree_centrality in self.get_out_degree_centrality().items()])
        
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
        if call:
            return self.call_graph.degree([call])[call]
        else:
            return self.call_graph.degree()

    @property
    def median_degree(self):
        return stat.median([degree for k, degree in self.get_degree().items()])

    @property
    def average_degree(self):
        return stat.mean([degree for k, degree in self.get_degree().items()])

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
        if call:
            return self.call_graph.in_degree([call])[call]
        else:
            return self.call_graph.in_degree()

    @property
    def median_in_degree(self):
        return stat.median([in_degree for k, in_degree in self.get_in_degree().items()])

    @property
    def average_in_degree(self):
        return stat.mean([in_degree for k, in_degree in self.get_in_degree().items()])

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
        if call:
            return self.call_graph.out_degree([call])[call]
        else:
            return self.call_graph.out_degree()

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