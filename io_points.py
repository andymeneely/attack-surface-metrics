__author__ = 'kevin'

import sys
from subprocess import check_output
import os

indent = "    "
file_patterns = ["*.c", "*.h"]
cflow_exec = "cflow"

input_functions = ['canonicalize_file_name', 'catgets', 'confstr', 'ctermid', 'ctermid', 'cuserid', 'dgettext',
                   'dngettext', 'fgetc', 'fgetc_unlocked', 'fgets', 'fgets_unlocked', 'fpathconf', 'fread',
                   'fread_unlocked', 'fscanf', 'getc', 'getchar', 'getchar_unlocked', 'getc_unlocked',
                   'get_current_dir_name', 'getcwd', 'getdelim', '__getdelim', 'getdelim', 'getdents', 'getenv',
                   'gethostbyaddr', 'gethostbyname', 'gethostbyname2', 'gethostent', 'gethostid', 'getline', 'getline',
                   'getlogin', 'getlogin_r', 'getmsg', 'getopt', '_getopt_internal', 'getopt_long', 'getopt_long_only',
                   'getpass', 'getpmsg', 'gets', 'gettext', 'getw', 'getwd', 'ngettext', 'pathconf', 'pread', 'pread64',
                   'ptsname', 'ptsname_r', 'read', 'readdir', 'readlink', 'readv', 'realpath', 'recv', 'recv_from',
                   'recvmesg', 'scanf', '__secure_getenv', 'signal', 'sysconf', 'ttyname', 'ttyname_r', 'vfscanf',
                   'vscanf']

output_functions = ['dprintf', 'fprintf', 'fputc', 'fputchar_unlocked', 'fputc_unlocked', 'fputs', 'fputs_unlocked',
                    'fwrite', 'fwrite_unlocked', 'perror', 'printf', 'psignal', 'putc', 'putchar', 'putc_unlocked',
                    'putenv', 'putmsg', 'putpmsg', 'puts', 'putw', 'pwrite', 'pwrite64', 'send', 'sendmsg', 'sendto',
                    'setenv', 'sethostid', 'setlogin', 'ungetc', 'vdprintf', 'vfprintf', 'vsyslog', 'write', 'writev']


def get_cflow_args(root):

    dirs_found = []

    for path, dirs, files in os.walk(os.path.abspath(root)):
        for dir in dirs:
            for pattern in file_patterns:
                dirs_found.append(os.path.join(path, dir, pattern))

    return dirs_found


def build_cflow_command(source_dir):
    cflow_args = get_cflow_args(source_dir)
    command = "cd {0}; ".format(source_dir) + cflow_exec + ' ' + ' '.join(cflow_args) + ";"
    return command


def is_input_function(call):

    is_input = False

    if call['call'].endswith("()"):  # i.e. if is_leaf
        is_input = call['call'][:-2] in input_functions

    return is_input


def is_output_function(call):
    is_output = False

    if call['call'].endswith("()"):  # i.e. if is_leaf
        is_output = call['call'][:-2] in output_functions

    return is_output


class FunctionCall():
    def __init__(self, call, level):
        self.call = call
        self.level = level


def main(args):
    source_dir = args[1]

    cmd_cflow = build_cflow_command(source_dir)
    cflow_output = check_output(cmd_cflow, shell=True).decode("utf-8")

    entry_points = []
    exit_points = []

    main_call = cflow_output.splitlines()[0]
    main_level = 0

    parent = []
    parent.append({'call': main_call, 'level': main_level})
    previous = {'call': main_call, 'level': main_level}

    for i, line in enumerate(cflow_output.splitlines()):
        if i != 0:
            split = line.split(indent)
            current = {'call': split[-1], 'level': len(split) - 1}

            if current['level'] > previous['level']:
                parent.append(previous)
            elif current['level'] < previous['level']:
                for i in range(current['level'] - previous['level']):
                    parent.pop()

            if is_input_function(current):
                entry_points.append(parent[-1])

            if is_output_function(current):
                exit_points.append(parent[-1])

            previous = current

    print(entry_points)
    print(exit_points)

if __name__ == '__main__':
    main(sys.argv)