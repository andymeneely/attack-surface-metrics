import os

from attacksurfacemeter.environments import Environments
from attacksurfacemeter.granularity import Granularity
from attacksurfacemeter.loaders.cflow_line_parser import CflowLineParser
from attacksurfacemeter.loaders.gprof_line_parser import GprofLineParser
from attacksurfacemeter.loaders.javacg_line_parser import JavaCGLineParser


class Call():

    """Represents a function or method in a system."""

    _android_input_methods = []
    _android_output_methods = []

    _c_std_lib_functions = []
    _c_input_functions = []
    _c_output_functions = []
    _c_dangerous_sys_calls = []

    def __init__(self, name, signature, environment,
                 granularity=Granularity.FUNC):
        """Call constructor.

        Parameters
        ----------
        name : str
            The name of the function represented by the object.
        signature : str
            A piece of information associated with the function represented by
            this object. In the current implementation, it is the name of the
            file where the function is defined.
        environment : str
            The environment of the function. See
            attacksurfacemeter.environments.Environments for available choices.
        granularity : str
            The granularity of the call graph into which the instance of Call
            will be added to. See attacksurfacemeter.granularity.Granularity
            for available choices.

        Returns
        -------
        call : Call
            An instance of Call.
        """
        self._function_name = name
        self._function_signature = signature
        self._environment = environment
        if granularity not in [Granularity.FILE, Granularity.FUNC]:
            raise Exception('Unsupported granularity {}'.format(granularity))
        self._granularity = granularity

    @classmethod
    def from_cflow(cls, cflow_line, granularity=Granularity.FUNC):
        """Instantiate Call by parsing a line from cflow call graph.

        Parameters
        ----------
        cflow_line : str
            A line of string from the cflow call graph.
        granularity : str
            The granularity of the call graph into which the instance of Call
            will be added to. See attacksurfacemeter.granularity.Granularity
            for available choices.

        Returns
        -------
        new_instance : Call
            An instance of Call.
        """
        cflow_line_parser = CflowLineParser.get_instance(cflow_line)

        new_instance = cls(
            cflow_line_parser.get_function_name(),
            cflow_line_parser.get_function_signature(),
            Environments.C,
            granularity
        )
        new_instance.level = cflow_line_parser.get_level()

        return new_instance

    @classmethod
    def from_gprof(cls, gprof_line, granularity=Granularity.FUNC):
        """Instantiate Call by parsing a line from gprof call graph.

        Parameters
        ----------
        gprof_line : str
            A line of string from the gprof call graph.
        granularity : str
            The granularity of the call graph into which the instance of Call
            will be added to. See attacksurfacemeter.granularity.Granularity
            for available choices.

        Returns
        -------
        new_instance : Call
            An instance of Call.
        """
        gprof_line_parser = GprofLineParser.get_instance(gprof_line)

        new_instance = cls(
            gprof_line_parser.get_function_name(),
            gprof_line_parser.get_function_signature(),
            Environments.C,
            granularity
        )

        return new_instance

    @classmethod
    def from_javacg(cls, javacg_line, granularity=Granularity.FUNC):
        """Instantiate Call by parsing a line from Java call graph.

        Parameters
        ----------
        javacg_line : str
            A line of string from the Java call graph.
        granularity : str
            The granularity of the call graph into which the instance of Call
            will be added to. See attacksurfacemeter.granularity.Granularity
            for available choices.

        Returns
        -------
        new_instance : Call
            An instance of Call.
        """
        javacg_line_parser = JavaCGLineParser.get_instance(javacg_line)

        new_instance = cls(
            javacg_line_parser.get_function_name(),
            javacg_line_parser.get_function_signature(),
            Environments.ANDROID,
            granularity
        )

        new_instance.class_name = javacg_line_parser.get_class()
        new_instance.package_name = javacg_line_parser.get_package()

        return new_instance

    def __repr__(self):
        """Return a string representation of the Call.

        Returns
        -------
        call : str
            A String representation of the Call.
        """
        if self._environment == Environments.ANDROID:
            return self._function_signature + '.' + self._function_name
        else:
            return self.identity

    def __str__(self):
        """Return a string representation of the Call.

        Returns
        -------
        call : str
            A String representation of the Call.
        """
        return self.__repr__()

    def __hash__(self):
        """Return a number that uniquely identifies this instance.

        Returns
        -------
        hash : int
            A number that represents the calculated hash of this instance.
        """
        return hash(self.identity)

    def __eq__(self, other):
        """Override == operator to allow comparing two Call instances.

        Parameters
        ----------
        other : Call
            An instance of Call to compare this instance to.

        Returns
        -------
        is_equal : bool
            True if this instance is equal to other, False otherwise.
        """
        return self.identity == other.identity

    def __ne__(self, other):
        """Override != operator to allow comparing two Call instances.

        Parameters
        ----------
        other : Call
            An instance of Call to compare this instance to.

        Returns
        -------
        is_notequal : bool
            True if this instance is not equal to other, False otherwise.
        """
        return self.identity != other.identity

    @staticmethod
    def _get_android_input_methods():
        if not Call._android_input_methods:
            Call._android_input_methods = Call._load_function_list(
                'android_input_methods'
            )

        return Call._android_input_methods

    @staticmethod
    def _get_android_output_methods():
        if not Call._android_output_methods:
            Call._android_output_methods = Call._load_function_list(
                'android_output_methods'
            )

        return Call._android_output_methods

    @staticmethod
    def _get_c_input_functions():
        if not Call._c_input_functions:
            Call._c_input_functions = Call._load_function_list(
                'c_input_functions'
            )

        return Call._c_input_functions

    @staticmethod
    def _get_c_output_functions():
        if not Call._c_output_functions:
            Call._c_output_functions = Call._load_function_list(
                'c_output_functions'
            )

        return Call._c_output_functions

    @staticmethod
    def _get_c_std_lib_functions():
        if not Call._c_std_lib_functions:
            Call._c_std_lib_functions = Call._load_function_list(
                'c_std_lib_functions'
            )

        return Call._c_std_lib_functions

    @staticmethod
    def _get_c_dangerous_sys_calls():
        if not Call._c_dangerous_sys_calls:
            Call._c_dangerous_sys_calls = Call._load_function_list(
                'c_dangerous_sys_calls'
            )

        return Call._c_dangerous_sys_calls

    @staticmethod
    def _load_function_list(function_list_file):
        file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            function_list_file
        )

        with open(file_name) as f:
            functions = f.read().splitlines()

        return functions

    def is_input(self):
        """Return True if the function is standard input, False otherwise.

        The list of standard input functions is taken from Appendix A of
        "Pratyusa, K. Manadhata, and M. Wing Jeannette. "An Attack Surface
        Metric." PhD diss., PhD thesis, Carnegie Mellon University, 2008."

        See file data/c_input_functions for the list of input functions.

        Parameters
        ----------
        None

        Returns
        -------
        is_input : bool
            True if the function is standard input, False otherwise.
        """
        is_input = False

        if self._environment == Environments.C:
            input_functions = Call._get_c_input_functions()
            is_input = (
                not self._function_signature and
                self._function_name in input_functions
            )
        elif self._environment == Environments.ANDROID:
            input_functions = Call._get_android_input_methods()
            is_input = (
                self._function_signature + "." + self._function_name
            ) in input_functions

        return is_input

    def is_output(self):
        """Return True if the function is standard output, False otherwise.

        The list of standard output functions is taken from Appendix A of
        "Pratyusa, K. Manadhata, and M. Wing Jeannette. "An Attack Surface
        Metric." PhD diss., PhD thesis, Carnegie Mellon University, 2008."

        See file data/c_output_functions for the list of output functions.

        Parameters
        ----------
        None

        Returns
        -------
        is_output : bool
            True if function is standard output, False otherwise.
        """
        is_output = False

        if self._environment == Environments.C:
            output_functions = Call._get_c_output_functions()
            is_output = (
                not self._function_signature and
                self._function_name in output_functions
            )
        elif self._environment == Environments.ANDROID:
            output_functions = Call._get_android_output_methods()
            is_output = (
                self._function_signature + "." + self._function_name
            ) in output_functions

        return is_output

    def is_dangerous(self):
        """Return True if the function is a dangerous, False otherwise.

        The list of dangerous system calls is taken from "Bernaschi, M.,
        Gabrielli, E., & Mancini, L. V. (2000, November). Operating system
        enhancements to prevent the misuse of system calls. In Proceedings of
        the 7th ACM conference on Computer and communications security (pp.
        174-183). ACM."

        See file data/c_dangerous_sys_calls for the list of dangerous system
        calls available in the C programming language.

        Parameters
        ----------
        None

        Returns
        -------
        is_dangerous : bool
            True if the function is dangerous, False otherwise.
        """
        c_dangerous_sys_calls = Call._get_c_dangerous_sys_calls()
        is_dangerous = (
            not self._function_signature and
            self._function_name in c_dangerous_sys_calls
        )
        return is_dangerous

    def in_stdlib(self):
        """Return True if the function is part of C library, False otherwise.

        The list of C standard library functions is taken from the list at
        http://www.gnu.org/software/libc/manual/html_node/Function-Index.html

        See file data/c_std_lib_functions for the list of C standard library
        functions.

        Parameters
        ----------
        None

        Returns
        -------
        in_stdlib : bool
            True if function is part of C library, False otherwise.
        """
        c_std_lib_functions = Call._get_c_std_lib_functions()
        in_stdlib = (
            not self._function_signature and
            self._function_name in c_std_lib_functions
        )
        return in_stdlib

    @property
    def identity(self):
        """Return a string that uniquely identifies this object.

        Parameters
        ----------
        None

        Returns
        -------
        identity : str
            The unique representation of this object.
        """
        identity = None
        if self._granularity == Granularity.FUNC:
            identity = self._function_name
            if self._function_signature:
                identity += ' ' + self._function_signature
        elif self._granularity == Granularity.FILE:
            identity = self._function_signature

        return identity

    @property
    def function_name(self):
        """Return the name of the function represented by this Call.

        Parameters
        ----------
        None

        Returns
        -------
        name : str
            The name of the function represented by this object.
        """
        return self._function_name

    @property
    def function_signature(self):
        """Return the signature of the function represented by this object.

        Parameters
        ----------
        None

        Returns
        -------
        signature : str
            The signature of the function represented by this object.
        """
        return self._function_signature

    @property
    def environment(self):
        """Return the environment of the function represented by this object.

        Parameters
        ----------
        None

        Returns
        -------
        environment : str
            The environment of the function represented by this object.
        """
        return self._environment
