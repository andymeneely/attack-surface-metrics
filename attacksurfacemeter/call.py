__author__ = 'kevin'

import os

from attacksurfacemeter.loaders.cflow_line_parser import CflowLineParser
from attacksurfacemeter.loaders.gprof_line_parser import GprofLineParser
from attacksurfacemeter.loaders.javacg_line_parser import JavaCGLineParser

from attacksurfacemeter.environments import Environments


class Call():
    """
        Represents a function/method call in a source code.
    
        Provides a basic functionality for derived classes.
    """

    indent = "    "

    _android_input_methods = []
    _android_output_methods = []

    _c_std_lib_functions = []
    _c_input_functions = []
    _c_output_functions = []

    def __init__(self, name, signature, environment):
        """
            Call constructor.
        
            Receives a line of cflow's output and parses it for some key information such as indent level,
            function name, signature and the point where it's defined.

            Args:
                name: A String containing the name of the function this Call represents.
                signature: A piece of information associated with the function this Call represents. In the current
                    implementation it is the name of the file where the function is defined.
                
            Returns:
                A new instance of Call.
        """
        self._function_name = name
        self._function_signature = signature
        self._environment = environment

    @classmethod
    def from_cflow(cls, cflow_line):
        cflow_line_parser = CflowLineParser.get_instance(cflow_line)

        new_instance = cls(cflow_line_parser.get_function_name(),
                           cflow_line_parser.get_function_signature(),
                           Environments.C)
        new_instance.level = cflow_line_parser.get_level()

        return new_instance

    @classmethod
    def from_gprof(cls, gprof_line):
        gprof_line_parser = GprofLineParser.get_instance(gprof_line)

        new_instance = cls(gprof_line_parser.get_function_name(),
                           gprof_line_parser.get_function_signature(),
                           Environments.C)

        return new_instance

    @classmethod
    def from_javacg(cls, javacg_line):
        javacg_line_parser = JavaCGLineParser.get_instance(javacg_line)

        new_instance = cls(javacg_line_parser.get_function_name(),
                           javacg_line_parser.get_function_signature(),
                           Environments.ANDROID)

        new_instance.class_name = javacg_line_parser.get_class()
        new_instance.package_name = javacg_line_parser.get_package()

        return new_instance

    def __str__(self):
        """
            Returns a string representation of the Call.

            Returns:
                A String representation of the Call
        """
        if self._environment == Environments.ANDROID:
            return self.function_signature + "." + self.function_name
        else:
            return self.identity

    def __hash__(self):
        """
            Returns a number that uniquely identifies this instance.
                
            Returns:
                An Int that represents the calculated hash of this instance.
        """
        return hash(self.identity)

    def __eq__(self, other):
        """
            Overrides == operator. Compares this instance of Call with another instance for equality.

            Args:
                other: The other instance of Call to compare this instance to.

            Returns:
                A Boolean that says whether this instance can be considered equal to other.
        """
        # return hash(self) == hash(other)

        return self.identity == other.identity

    def __ne__(self, other):
        """
            Overrides != operator. Compares this instance of Call with another instance for inequality.

            Args:
                other: The other instance of Call to compare this instance to.

            Returns:
                A Boolean that says whether this instance can be considered not equal to other.
        """
        return self.identity != other.identity

    @staticmethod
    def _get_android_input_methods():
        if not Call._android_input_methods:
            Call._android_input_methods = Call._load_function_list("android_input_methods")

        return Call._android_input_methods

    @staticmethod
    def _get_android_output_methods():
        if not Call._android_output_methods:
            Call._android_output_methods = Call._load_function_list("android_output_methods")

        return Call._android_output_methods

    @staticmethod
    def _get_c_input_functions():
        if not Call._c_input_functions:
            Call._c_input_functions = Call._load_function_list("c_input_functions")

        return Call._c_input_functions

    @staticmethod
    def _get_c_output_functions():
        if not Call._c_output_functions:
            Call._c_output_functions = Call._load_function_list("c_output_functions")

        return Call._c_output_functions

    @staticmethod
    def _get_c_std_lib_functions():
        if not Call._c_std_lib_functions:
            Call._c_std_lib_functions = Call._load_function_list("c_std_lib_functions")

        return Call._c_std_lib_functions

    @staticmethod
    def _load_function_list(function_list_file):
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', function_list_file)

        with open(file_name) as f:
            functions = f.read().splitlines()

        return functions

    def is_input_function(self):
        """
            Determines whether the function represented by this object is an input function.

            Returns:
                A Boolean that states whether this object is an input function.
        """
        is_input = False

        if self._environment == Environments.C:
            input_functions = Call._get_c_input_functions()
            is_input = self.function_name in input_functions
        elif self._environment == Environments.ANDROID:
            input_functions = Call._get_android_input_methods()
            is_input = (self.function_signature + "." + self.function_name) in input_functions

        return is_input

    def is_output_function(self):
        """
            Determines whether the function represented by this object is an output function.

            Returns:
                A Boolean that states whether this object is an output function.
        """
        is_output = False

        if self._environment == Environments.C:
            output_functions = Call._get_c_output_functions()
            is_output = self.function_name in output_functions
        elif self._environment == Environments.ANDROID:
            output_functions = Call._get_android_output_methods()
            is_output = (self.function_signature + "." + self.function_name) in output_functions

        return is_output

    def is_standard_library_function(self):
        """
            Determines whether the function represented by this object is a standard library function.

            Returns:
                A Boolean that states whether this object is a standard library function.
        """
        c_standard_library_functions = Call._get_c_std_lib_functions()
        return self.function_name in c_standard_library_functions

    def is_function_name_only(self):
        return False if self._function_signature else True

    @property
    def identity(self):
        """
            Returns a string that uniquely identifies this object.

            Returns:
                A String that contains a unique representation of this object.
        """
        value = self.function_name

        if self.function_signature:
            value += ' ' + self.function_signature

        return value

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
        # TODO: This should be renamed to something like file or file_location or file_name.
        return self._function_signature

    def set_function_signature(self, new_function_signature):
        """
            Sets the function_signature property.

        Args:
            new_function_signature: A string representing the new function signature to set.
        """
        self._function_signature = new_function_signature