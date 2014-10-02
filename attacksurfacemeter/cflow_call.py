__author__ = 'kevin'

import re

from attacksurfacemeter.call import Call


class CflowCall(Call):
    """
        Represents a function/method call in a source code.
    
        Encapsulates parsing logic for cflow's output.
        For each new line of output, an instance of this class is created.

        Attributes:
            function_info: A String containing one single line of raw information output from cflow.
            level: The level of indentation the line represented by this instance has in cflow's output.
                Used to determine the caller/callee relationship between two calls.
    """

    indent = "    "

    def __init__(self, cflow_line):
        """
            Call constructor.
        
            Receives a line of cflow's output and parses it for some key information such as indent level,
            function name, signature and the point where it's defined.
        
            Args:
                cflow_line: A String containing a single line of cflow's output.
                
            Returns:
                A new instance of Call.
        """
        split_line = cflow_line.split(CflowCall.indent)

        self.function_info = split_line[-1].strip()
        self.level = len(split_line) - 1

        self._function_name = None
        self._function_signature = None

    @property
    def function_name(self):
        """
            Returns the name of the function call represented by this Call.

            Returns:
                A String containing the name of the function call represented by this object.
        """
        if not self._function_name:
            self._function_name = re.search(r"(\w+\(\))", self.function_info).group(0)
            self._function_name = self._function_name[:self._function_name.index('(')]

        return self._function_name

    @property
    def function_signature(self):
        """
            Returns the signature and file location of the function call represented by this object.

            Returns:
                A String containing the function signature and file location of the call represented by this object
        """
        if not self._function_signature:
            # match = re.search(r"(<.+>)", self.function_info)
            match = re.search(r"(\w+\.c)", self.function_info)

            if match:
                self._function_signature = match.group(0)

        return self._function_signature

    def is_library_call(self):
        return self._function_signature is None