import copy
import networkx as nx
import warnings

from attacksurfacemeter.call import Call


def fix(call_graph, using):
    """Fix a call graph using information from another, reference call graph.

    Function attempts to a fix a call graph using a reference call graph
    which is assumed to be more comprehensive than the one being fixed.
    The notion of fixing a call graph entails identifying a node without
    function_signature and replacing it with an identical node from the
    reference call graph that has a function_signature.

    A call graph is required to be fixed to ensure compatibility of
    equivalent nodes so that later when merging the two call graphs' sets
    of edges, networkx doesn't think the cflow and gprof calls are
    different only because one of them doesn't have a function_signature
    associated to it.

    Parameters
    ----------
    call_graph : CallGraph
        An instance of CallGraph that represents a call graph to be fixed.
    using : CallGraph
        An instance of CallGraph that represents a call graph assumed to
        be more comprehensive than call graph required to be fixed. In other
        words, the using call graph is a reference call graph.

    Notes
    -----

    networkx internally uses a dictionary as the data structure to store
    nodes. Modifying an attribute that is used in the computation of the
    object's hash will invalidate the hash leaving the graph in an
    inconsistent state. Hence, fixing nodes involves replacing existing
    nodes with their fixed equivalents.

    More details at http://networkx.lanl.gov/tutorial/tutorial.html
    """
    nodes_to_replace = []

    for node in [n for (n, _) in call_graph.nodes if not n.function_signature]:
        reference_nodes = [
            n for (n, _) in using.nodes
            if n.function_name == node.function_name
        ]

        if len(reference_nodes) == 1:
            new_node = Call(
                node.function_name,
                reference_nodes[0].function_signature,
                node.environment
            )
            nodes_to_replace.append((node, new_node))

    for (before, after) in nodes_to_replace:
        call_graph.call_graph.add_node(
            after,
            call_graph.call_graph.node[before]
        )

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


def get_fragments(graph):
    """Return a list of strongly connected components of a graph.

    Parameters
    ----------
    graph : NetworkX DiGraph
        A strongly connected instance of NetworkX DiGraph object.

    Returns
    -------
    fragments : list
        A list of strongly connected instances of NetworkX DiGraph each of
        which represents a component in the graph.
    """
    if not isinstance(graph, nx.DiGraph):
        raise Exception(
            'get_fragments operation not defined for undirected graphs.'
        )

    return list(nx.strongly_connected_component_subgraphs(graph))


def get_largest_fragment(fragments):
    """Return the largest connected component in a list of components.

    Parameters
    ----------
    fragments : list
        A list of strongly connected instances of NetworkX DiGraph each of
        which represents a component in the graph.

    Returns
    -------
    fragment : NetworkX DiGraph
        A strongly connected instance of NetworkX DiGraph that represents the
        largest component in the graph.
    """
    fragments.sort(key=lambda f: len(f.nodes()), reverse=True)
    return fragments[0]


def get_node_attrs(source, caller, callee, defenses, vulnerabilities):
    """Return node attributes.

    Parameters
    ----------

    Returns
    -------
    attributes : tuple
        A tuple of two dictionary elements: caller_attrs and callee_attrs. The
        callee_attrs may be None if the callee is a standard library function.
        Each dictionary may contain the following keys:

        Common Keys:

        tested: True if the node is tested, False otherwise.
        defense: Set if the node represents a function which is a designed
            defense in the system.
        vulnerable: Set if the node represents a vulnerable function in the
            system.

        Caller-specific Keys:

        dangerous: Set if the callee is a dangerous system function.
        entry: Set if the callee is an standard input function.
        exit: Set if the callee is a standard output function.
    """
    caller_attrs = dict()
    callee_attrs = None

    if caller in defenses:
        caller_attrs['defense'] = None
    if caller in vulnerabilities:
        caller_attrs['vulnerable'] = None
    if callee is not None:
        if 'gprof' in source:
            caller_attrs['tested'] = None
        if callee.in_stdlib():
            if callee.is_dangerous():
                caller_attrs['dangerous'] = None
            if callee.is_input():
                caller_attrs['entry'] = None
            if callee.is_output():
                caller_attrs['exit'] = None
        else:
            callee_attrs = dict()

            callee_attrs['frequency'] = 1
            if 'gprof' in source:
                callee_attrs['tested'] = None
            if callee in defenses:
                callee_attrs['defense'] = None
            if callee in vulnerabilities:
                callee_attrs['vulnerable'] = None

    attributes = (caller_attrs, callee_attrs)

    return attributes


def deprecation(function):
    """Mark a function as deprecated.

    Parameters
    ----------
    function : object
        A function object to be marked as deprecated.

    Returns
    -------
    function : object
        A function object that wraps the function being decorated.
    """
    def wrapper(*args, **kwargs):
        warnings.warn(
            '{0} will soon be deprecated'.format(function.__name__),
            DeprecationWarning,
            stacklevel=2
        )
        return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    wrapper.__dict__ = function.__dict__
    return wrapper
