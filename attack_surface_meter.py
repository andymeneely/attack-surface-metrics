__author__ = 'kevin'

import argparse

from attacksurfacemeter import CallGraph
from formatters import TxtFormatter, XmlFormatter, JsonFormatter, HtmlFormatter


def main():

    formatters = {
        'txt': TxtFormatter,
        'xml': XmlFormatter,
        'json': JsonFormatter,
        'html': HtmlFormatter
    }

    args = parse_args()

    call_graph = CallGraph(args.source_dir, args.reverse)

    formatter = formatters[args.format](call_graph)

    if args.summary:
        print(formatter.write_summary())
    else:
        print(formatter.write_output())


def parse_args():
    """
        Provides a command line interface for the attack surface meter.

        Defines all the positional and optional arguments along with their respective valid values
        for the command line interface and returns all the received arguments as an object.

        Returns:
            An object that contains all the provided command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes a software's source code and reports various metrics related to it's attack surface.")

    parser.add_argument("source_dir",
                        help="Root directory of the source code to analyze or the text file that "
                             "contains the raw call graph information.")
    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")
    parser.add_argument("-s", "--summary", action="store_true",
                        help="Print only a summary of the report.")

    return parser.parse_args()


if __name__ == '__main__':
    main()