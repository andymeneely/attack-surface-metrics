__author__ = 'kevin'

import re


class Call():

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
        split_line = cflow_line.split(Call.indent)

        self.function_info = split_line[-1].strip()
        self.level = len(split_line) - 1

        self._function_name = None
        self._function_signature = None

    def __str__(self):
        return self.function_name

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other):
        # return hash(self) == hash(other)
        return self.identity == other.identity

    def __ne__(self, other):
        return self.identity != other.identity

    @property
    def identity(self):
        value = self.function_name

        if self.function_signature:
            value += self.function_signature

        return value

    @property
    def function_name(self):
        if not self._function_name:
            self._function_name = re.search(r"(\w+\(\))", self.function_info).group(0)

        return self._function_name

    @property
    def function_signature(self):
        if not self._function_signature:
            match = re.search(r"(<.+>)", self.function_info)

            if match:
                self._function_signature = match.group(0)

        return self._function_signature

    def is_input_function(self):
        is_input = self._belongs_to(Call.input_functions)
        return is_input

    def is_output_function(self):
        is_output = self._belongs_to(Call.output_functions)
        return is_output

    def _belongs_to(self, function_set):
        return self.function_name[:self.function_name.index('(')] in function_set