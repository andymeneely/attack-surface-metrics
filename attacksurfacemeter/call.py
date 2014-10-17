__author__ = 'kevin'

import re


class Call():
    """
        Represents a function/method call in a source code.
    
        Provides a basic functionality for derived classes.
    """

    input_functions = ['canonicalize_file_name', 'catgets', 'confstr', 'ctermid', 'ctermid', 'cuserid', 'dgettext',
                       'dngettext', 'fgetc', 'fgetc_unlocked', 'fgets', 'fgets_unlocked', 'fpathconf', 'fread',
                       'fread_unlocked', 'fscanf', 'getc', 'getchar', 'getchar_unlocked', 'getc_unlocked',
                       'get_current_dir_name', 'getcwd', 'getdelim', '__getdelim', 'getdelim', 'getdents', 'getenv',
                       'gethostbyaddr', 'gethostbyname', 'gethostbyname2', 'gethostent', 'gethostid', 'getline',
                       'getline', 'getlogin', 'getlogin_r', 'getmsg', 'getopt', '_getopt_internal', 'getopt_long',
                       'getopt_long_only', 'getpass', 'getpmsg', 'gets', 'gettext', 'getw', 'getwd', 'ngettext',
                       'pathconf', 'pread', 'pread64', 'ptsname', 'ptsname_r', 'read', 'readdir', 'readlink', 'readv',
                       'realpath', 'recv', 'recv_from', 'recvmesg', 'scanf', '__secure_getenv', 'signal', 'sysconf',
                       'ttyname', 'ttyname_r', 'vfscanf', 'vscanf']

    output_functions = ['dprintf', 'fprintf', 'fputc', 'fputchar_unlocked', 'fputc_unlocked', 'fputs', 'fputs_unlocked',
                        'fwrite', 'fwrite_unlocked', 'perror', 'printf', 'psignal', 'putc', 'putchar', 'putc_unlocked',
                        'putenv', 'putmsg', 'putpmsg', 'puts', 'putw', 'pwrite', 'pwrite64', 'send', 'sendmsg',
                        'sendto', 'setenv', 'sethostid', 'setlogin', 'ungetc', 'vdprintf', 'vfprintf', 'vsyslog',
                        'write', 'writev']

    indent = "    "

    def __init__(self, name, signature):
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

    # ini Cflow Stuff

    @classmethod
    def from_cflow(cls, cflow_line, cflow_line_parser):

        # split_line = cflow_line.split(Call.indent)
        #
        # function_info = split_line[-1].strip()
        #
        # # function name
        # function_name = re.search(r"(\w+\(\))", function_info).group(0)
        # function_name = function_name[:function_name.index('(')]
        #
        # # function signature
        # match = re.search(r"(\w+\.c)", function_info)
        # if match:
        #     function_signature = match.group(0)
        #
        # new_instance = cls(function_name, function_signature)
        # new_instance.level = len(split_line) - 1
        # new_instance.function_info = function_info

        cflow_line_parser.load(cflow_line)

        new_instance = cls(cflow_line_parser.get_function_name(), cflow_line_parser.get_function_signature())
        new_instance.level = cflow_line_parser.get_level()
        new_instance.function_info = cflow_line_parser.get_function_info()

        return new_instance

    def is_library_call(self):
        return self._function_signature is None

    # end Cflow Stuff

    # ini Gprof stuff

    @classmethod
    def from_gprof(cls, gprof_line, gprof_line_parser):
        # match = re.search(r"(\[\d+\])( +)((\d+\.\d+)( +)){3}(\d*\+*\d*)( +)([\w.]+)( +)(.*)", gprof_line)
        #
        # if not match:
        #     match = re.search(r"(\[\d+)( +)((\d+\.\d+)( +)){3}(\d*)( +)([\w.]+)( +)(.*)", gprof_line)
        #
        # if match:
        #     _function_name = match.group(8)
        #     _function_signature = Call.get_file_name(match.group(10))
        # else:
        #     match = re.search(r"( +)((\d+\.\d+)( +)){2}(\d+/\d+)( +)([\w.]+)( +)(.*)", gprof_line)
        #
        #     if match:
        #         _function_name = match.group(7)
        #         _function_signature = Call.get_file_name(match.group(9))
        #     else:
        #         match = re.search(r"( +)(\d+)( +)(\w+)( +)(.*)", gprof_line)
        #
        #         if match:
        #             try:
        #                 _function_name = match.group(4)
        #                 _function_signature = Call.get_file_name(match.group(6))
        #             except:
        #                 raise ValueError("Can not parse a call from the received text.")
        #         else:
        #             raise ValueError("Can not parse a call from the received text.")
        #
        # new_instance = Call(_function_name, _function_signature)
        # new_instance.raw_line = gprof_line

        gprof_line_parser.load(gprof_line)

        new_instance = Call(gprof_line_parser.get_function_name(), gprof_line_parser.get_function_signature())
        new_instance.raw_line = gprof_line_parser.get_raw_line()

        return new_instance

    @staticmethod
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

    # end Gprof stuff

    def __str__(self):
        """
            Returns a string representation of the Call.

            Returns:
                A String representation of the Call
        """
        return self.function_name

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

        if self.function_signature and other.function_signature:
            return self.identity == other.identity
        else:
            return self.function_name == other.function_name

    def __ne__(self, other):
        """
            Overrides != operator. Compares this instance of Call with another instance for inequality.

            Args:
                other: The other instance of Call to compare this instance to.

            Returns:
                A Boolean that says whether this instance can be considered not equal to other.
        """
        return self.identity != other.identity

    def is_input_function(self):
        """
            Determines whether the function represented by this object is an input function.

            Returns:
                A Boolean that states whether this object is an input function.
        """
        is_input = self._belongs_to(Call.input_functions)
        return is_input

    def is_output_function(self):
        """
            Determines whether the function represented by this object is an output function.

            Returns:
                A Boolean that states whether this object is an output function.
        """
        is_output = self._belongs_to(Call.output_functions)
        return is_output

    def _belongs_to(self, function_set):
        """
            Determines whether the function represented by this object is contained in a given function set.

            Args:
                function_set: A List of Strings that contain the names of the functions to test if this object is
                    present in.

            Returns:
                A Boolean that states whether the function represented by this object is contained in a given
                function set.
        """
        return self.function_name in function_set

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
        return self._function_signature