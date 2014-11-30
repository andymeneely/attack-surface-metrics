__author__ = 'kevin'

import argparse
import subprocess
import os
import re


def main():
    args = parse_args()

    os.chdir(args.repo_root)

    # git checkout <COMMIT SHA1>
    subprocess.call(['git', 'checkout', args.commit])

    # git show --pretty="format:" --name-only <COMMIT SHA1>
    proc = subprocess.Popen(['git',
                             'show',
                             '--pretty=format:',
                             '--name-only',
                             args.commit],
                            stdout=subprocess.PIPE)

    changed_files = proc.stdout.read().decode(encoding='UTF-8')
    changed_files = changed_files.strip().split('\n')

    modified_functions = set()

    for changed_file in changed_files:
        #git show <COMMIT SHA1> -- <FILE NAME>
        proc = subprocess.Popen(['git',
                                 'show',
                                 args.commit,
                                 '--',
                                 changed_file],
                                stdout=subprocess.PIPE)

        changed_file_diff = proc.stdout.read().decode(encoding='UTF-8')

        diff_lines = changed_file_diff.splitlines()
        reached_diff = False



        for diff_line in diff_lines:
            if not reached_diff:
                if diff_line.startswith('@@'):
                    reached_diff = True
                    idx = 0

                    # @@ -12,35 +12,4 @@ void greet(int);
                    # @@ from-file-line-numbers to-file-line-numbers @@
                    # @@ start,count start,count @@
                    # >>> re.search(reg_ex, text).group(4)
                    # '+12,4'
                    # >>> re.search(reg_ex, text).group(5)
                    # '12'
                    # >>> re.search(reg_ex, text).group(6)
                    # '4'
                    match = re.search(r"(@@ )([-]\d+,\d+)( )([+](\d+),(\d+))( @@)(.*)", diff_line)
                    diff_start_line = int(match.group(5))
                    # diff_count_line = int(match.group(6))

            else:
                if diff_line.startswith('+') or diff_line.startswith('-'):
                    function_for_line = find_function(diff_start_line + idx, changed_file)

                    if function_for_line:
                        modified_functions.add(function_for_line)

                idx += 1

    for function_name in modified_functions:
        print(function_name)

    subprocess.call(['git', 'checkout', 'origin/master'])


def find_function(line_number, file):

    function_for_line = None

    # ctags -x --c-kinds=f <FILE NAME>
    # http://ctags.sourceforge.net/ctags.html
    ctags = subprocess.Popen(["ctags",
                              "-x",
                              "--c-kinds=f",
                              file],
                             stdout=subprocess.PIPE)

    ctags_output = ctags.stdout.read().decode(encoding='UTF-8').splitlines()

    # line = 'GreeterSayHi     function     48 tests/helloworld/src/helloworld.c void GreeterSayHi()'
    functions_in_file = [{'name': line.split()[0], 'line_number': int(line.split()[2])} for line in ctags_output]
    functions_in_file = [f for f in functions_in_file if f['line_number'] <= line_number]

    if functions_in_file:
        functions_in_file.sort(key=lambda func: func['line_number'])
        function_for_line = functions_in_file[-1]['name']

    return function_for_line


def parse_args():

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-c", "--commit", help="")
    parser.add_argument("-d", "--diff", help="")
    parser.add_argument("-rr", "--repo_root", help="")

    return parser.parse_args()


if __name__ == "__main__":
    main()