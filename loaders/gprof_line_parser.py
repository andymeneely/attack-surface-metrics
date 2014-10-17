__author__ = 'kevin'

import re

from loaders import BaseLineParser


class GprofLineParser(BaseLineParser):
    """"""
    def __init__(self):
        super(GprofLineParser, self).__init__()

    @staticmethod
    def get_instance():
        return GprofLineParser._lazy_load_instance(GprofLineParser)

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