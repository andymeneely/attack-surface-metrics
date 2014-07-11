__author__ = 'kevin'

import re


class Call():
    """
        Represents a function/method call in a source code.
    
        Encapsulates parsing logic for cflow's output. For each line of cflow's output, an instance of this 
        class is potentially created.
    
        Attributes:
            function_info: A String containing one single line of cflow's output as is.
            level: The level of indentation the line represented by this instance has in cflow's output.
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
        split_line = cflow_line.split(Call.indent)

        self.function_info = split_line[-1].strip()
        self.level = len(split_line) - 1

        self._function_name = None
        self._function_signature = None

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

    @property
    def identity(self):
        """
            Returns a string that uniquely identifies this object.
            
            Returns:
                A String that contains a unique representation of this object.
        """
        value = self.function_name

        if self.function_signature:
            value += self.function_signature

        return value

    @property
    def function_name(self):
        """
            Returns the name of the function call represented by this Call.

            Returns:
                A String containing the name of the function call represented by this object.
        """
        if not self._function_name:
            self._function_name = re.search(r"(\w+\(\))", self.function_info).group(0)

        return self._function_name

    @property
    def function_signature(self):
        """
            Returns the signature and file location of the function call represented by this object.

            Returns:
                A String containing the function signature and file location of the call represented by this object
        """
        if not self._function_signature:
            match = re.search(r"(<.+>)", self.function_info)

            if match:
                self._function_signature = match.group(0)

        return self._function_signature

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
        return self.function_name[:self.function_name.index('(')] in function_set