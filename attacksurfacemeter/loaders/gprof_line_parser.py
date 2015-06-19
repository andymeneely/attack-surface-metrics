import re

from attacksurfacemeter.loaders.base_line_parser import BaseLineParser

# Regular expression to parse the name field from gprof call graph
RE_NAME = re.compile('^(\w+)(?:(?:\(?.*\)?\s\()([\w\.\-\/]+\.\w+))?')


class GprofLineParser(BaseLineParser):
    """"""
    _instance = None

    @staticmethod
    def get_instance(gprof_line=None):
        if GprofLineParser._instance is None:
            GprofLineParser._instance = GprofLineParser()

        GprofLineParser._instance.load(gprof_line)

        return GprofLineParser._instance

    def __init__(self):
        super(GprofLineParser, self).__init__()

    def load(self, gprof_line):
        self.__init__()

        # The field in the gprof call graph that contains the name of the
        # function and the file containing the function begins at column 46 
        # (deduced from gprof source code)
        name = gprof_line[45:]
        match = RE_NAME.match(name.strip())
        
        if match:
            groups = match.groups(default='')
            self._function_name = groups[0]
            self._function_signature = groups[1]
        else:
            raise ValueError(
                'Unable to parse gprof line - "{0}"'.format(gprof_line)
            )

