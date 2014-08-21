__author__ = 'kevin'

import argparse

from attacksurfacemeter import CallGraph
from attacksurfacemeter import CflowLoader
from attacksurfacemeter import GprofLoader
from formatters import TxtFormatter, XmlFormatter, JsonFormatter, HtmlFormatter


def main():

    formatters = {
        'txt': TxtFormatter,
        'xml': XmlFormatter,
        'json': JsonFormatter,
        'html': HtmlFormatter
    }

    loaders = {
        'cflow': CflowLoader,
        'gprof': GprofLoader
    }

    args = parse_args()

    loader = loaders[args.tool](args.source, args.reverse)

    call_graph = CallGraph(loader)

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

    parser.add_argument("source",
                        help="Can be either the root directory of the source code to analyze or the text file that "
                             "contains the raw call graph information.")
    parser.add_argument("-t", "--tool", choices=["cflow", "gprof"], default="cflow",
                        help="The call graph generation software to use.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")
    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics report.")
    parser.add_argument("-s", "--summary", action="store_true",
                        help="Print only a summary of the report.")

    return parser.parse_args()


if __name__ == '__main__':
    main()