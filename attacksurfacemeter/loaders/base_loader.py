from attacksurfacemeter.granularity import Granularity


class BaseLoader(object):
    def __init__(self, source, is_reverse=False, defenses=None,
                 vulnerabilities=None):
        """Constructor for BaseLoader.

        BaseLoader is an abstract base class for to be derived and implemented
        by different call graph loaders. E.g. CflowLoader, GprofLoader etc.

        Parameters
        ----------
        source : str
            The absolute path to a text file containing the call graph or the
            absolute path to a directory containing the source files for which
            a call graph must be generated.
        reverse : bool
            True if the call graph should be parsed with the assumption that it
            was created using the reverse algorithm (if available) in the tool,
            False otherwise.
        defenses : list, optional
            A list of Call objects, each representing a designed defense in the
            system.
        vulnerabilities : list, optional
            A list of Call objects, each representing a vulnerable function in
            the system.
        """
        self.source = source
        self.is_reverse = is_reverse
        self.defenses = defenses if defenses is not None else list()
        self.vulnerabilities = (
            vulnerabilities if vulnerabilities is not None else list()
        )
        self._errors = list()

    def load_call_graph(self, granularity=Granularity.FILE):
        raise NotImplementedError()

    @property
    def errors(self):
        return self._errors
