__author__ = 'kevin'

import re

from attacksurfacemeter.call import Call


class GprofCall(Call):
    """
        Represents a function/method call in a source code.

        Encapsulates parsing logic for gprof's output.
        For each new line of output, an instance of this class is created.
    """
    def __init__(self, line):
        """
            Call constructor.

            Receives a line of gprof's output and parses it for some key information such as
            function name and the point where it's defined.

            Args:
                line: A String containing one single line of raw information output from gprof.

            Returns:
                A new instance of Call.

            Sample lines:
                                0.00    0.00  131072/147456      get_bits (get_bits.h:262 @ 6d16df) [269306]
                [4]      0.0    0.00    0.00  147456         read_tree (bink.c:245 @ 7003f0) [4]

            Some identified special cases:
                [28]     0.0    0.00    0.00      58+8       avg_cavs_qpel8or16_v1_3dnow (cavsdsp_mmx.c:429 @ 9afb10) [28]'
                [18977   0.0    0.00    0.00                 ff_choose_timebase (mux.c:106 @ 54fd80) [189777]
        """
        self.raw_line = line
        match = re.search(r"(\[\d+\])( +)((\d+\.\d+)( +)){3}(\d*\+*\d*)( +)([\w.]+)( +)(.*)", line)

        if not match:
            match = re.search(r"(\[\d+)( +)((\d+\.\d+)( +)){3}(\d*)( +)([\w.]+)( +)(.*)", line)

        if match:
            self._function_name = match.group(8)
            self._function_signature = self.get_file_name(match.group(10))
        else:
            match = re.search(r"( +)((\d+\.\d+)( +)){2}(\d+/\d+)( +)([\w.]+)( +)(.*)", line)

            if match:
                self._function_name = match.group(7)
                self._function_signature = self.get_file_name(match.group(9))
            else:
                match = re.search(r"( +)(\d+)( +)(\w+)( +)(.*)", line)

                if match:
                    try:
                        self._function_name = match.group(4)
                        self._function_signature = self.get_file_name(match.group(6))
                    except:
                        raise ValueError("Can not parse a call from the received text.")
                else:
                    raise ValueError("Can not parse a call from the received text.")

    def get_file_name(self, text_fragment):
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

    @property
    def function_name(self):
        """
            Returns the name of the function call represented by this Call.

            Returns:
                A String containing the name of the function call represented by this object.
        """
        return self._function_name

    @property
    def function_signature(self):
        """
            Returns the signature and file location of the function call represented by this object.

            Returns:
                A String containing the function signature and file location of the call represented by this object
        """
        return self._function_signature