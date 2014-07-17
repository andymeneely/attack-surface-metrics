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
    formatter.write_output()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyzes a software's source code and reports various metrics related to it's attack surface.")

    parser.add_argument("source_dir", help="Root directory of the source code to analyze.")
    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics.")
    # parser.add_argument("-o", "--output", help="Output file.", default="output.metrics")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")

    return parser.parse_args()


if __name__ == '__main__':
    main()