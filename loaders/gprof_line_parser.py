__author__ = 'kevin'

import re


class GprofLineParser():
    """"""
    _instance = None

    @staticmethod
    def get_instance():
        if GprofLineParser._instance is None:
            GprofLineParser._instance = GprofLineParser()

        return GprofLineParser._instance

    def __init__(self):
        self._function_name = ""
        self._function_signature = ""

    def load(self, gprof_line):
        match = re.search(r"(\[\d+\])( +)((\d+\.\d+)( +)){3}(\d*\+*\d*)( +)([\w.]+)( +)(.*)", gprof_line)

        if not match:
            match = re.search(r"(\[\d+)( +)((\d+\.\d+)( +)){3}(\d*)( +)([\w.]+)( +)(.*)", gprof_line)

        if match:
            self._function_name = match.group(8)
            self._function_signature = GprofLineParser._get_file_name(match.group(10))
        else:
            match = re.search(r"( +)((\d+\.\d+)( +)){2}(\d+/\d+)( +)([\w.]+)( +)(.*)", gprof_line)

            if match:
                self._function_name = match.group(7)
                self._function_signature = GprofLineParser._get_file_name(match.group(9))
            else:
                match = re.search(r"( +)(\d+)( +)(\w+)( +)(.*)", gprof_line)

                if match:
                    try:
                        self._function_name = match.group(4)
                        self._function_signature = GprofLineParser._get_file_name(match.group(6))
                    except:
                        raise ValueError("Can not parse a call from the received text.")
                else:
                    raise ValueError("Can not parse a call from the received text.")

    @staticmethod
    def _get_file_name(text_fragment):
        """
            Obtains the name of the file where the function represented is defined.

            Args:
               text_fragment: A String containing a fragment from a line of gprof's output.

            Returns:
                A String containing the name of the file where the function detailed in the fragment is defined.
        """
        regex = r"(\w+\.c)|(\w+\.asm)"

        match = re.search(regex, text_fragment)

        if match:
            return re.search(regex, text_fragment).group(0)
        else:
            return ""

    def get_function_name(self, gprof_line=None):
        self._load_if_new(gprof_line)
        return self._function_name

    def get_function_signature(self, gprof_line=None):
        self._load_if_new(gprof_line)
        return self._function_signature

    def _load_if_new(self, gprof_line):
        if gprof_line is not None:
            self.load(gprof_line)