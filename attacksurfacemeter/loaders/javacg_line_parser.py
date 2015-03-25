__author__ = 'kevin'

from attacksurfacemeter.loaders.base_line_parser import BaseLineParser


class JavaCGLineParser(BaseLineParser):
    """"""
    _instance = None

    @staticmethod
    def get_instance(cflow_line=None):
        if JavaCGLineParser._instance is None:
            JavaCGLineParser._instance = JavaCGLineParser()

        JavaCGLineParser._instance.load(cflow_line)

        return JavaCGLineParser._instance

    def __init__(self):
        super(JavaCGLineParser, self).__init__()

        self._class_name = ""
        self._package_name = ""

    def load(self, javacg_line):
        self.__init__()

        if javacg_line.startswith("M:"):
            javacg_line = javacg_line[2:].strip()  # Remove the trailing "M:"
        else: # if javacg_line.startswith("(M)") or "(I)" or "(O)" or "(S)"
            javacg_line = javacg_line[3:].strip()  # Remove the trailing "(*)"

        self._function_name = javacg_line[javacg_line.index(":") + 1:]
        self._function_signature = javacg_line[:javacg_line.index(":")]

        self._class_name = self._function_signature

        if "." in self._class_name:
            self._package_name = ".".join(self._class_name.split(".")[:-1])
        else:
            self._package_name = self._class_name

    def get_class(self):
        return self._class_name

    def get_package(self):
        return self._package_name