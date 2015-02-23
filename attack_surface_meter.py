__author__ = 'kevin'

import argparse

from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader
from loaders.gprof_loader import GprofLoader
from loaders.javacg_loader import JavaCGLoader
from formatters.txt_formatter import TxtFormatter
from formatters.xml_formatter import XmlFormatter
from formatters.json_formatter import JsonFormatter
from formatters.html_formatter import HtmlFormatter

# TODO: This way of setting up the call graph and metrics calculations is becoming
# too complex. Better find another way to set all of this up. Creating classes for
# managing the set up of each "class chain" seems like a good idea.
def main():

    formatters = {
        'txt': TxtFormatter,
        'xml': XmlFormatter,
        'json': JsonFormatter,
        'html': HtmlFormatter
    }

    loaders = {
        'cflow': CflowLoader,
        'gprof': GprofLoader,
        'javacg': JavaCGLoader
    }

    args = parse_args()

    if args.tool == "all":
        # TODO: Maybe it would be useful to have some sort of factory method here because
        # of different constructor signatures for different loaders. I.e. gprof doesn't
        # support a reverse option so its not necessary to send it as a parameter.
        cflow_loader = loaders['cflow'](args.cflowfile, args.reverse)
        gprof_loader = loaders['gprof'](args.gproffile, args.reverse)

        call_graph = CallGraph.from_merge(CallGraph.from_loader(cflow_loader),
                                          CallGraph.from_loader(gprof_loader))
    else:
        if_not_none = lambda file: file if file is not None else args.source

        input_file = {
            'cflow': if_not_none(args.cflowfile),
            'gprof': if_not_none(args.gproffile),
            'javacg': if_not_none(args.javacgfile)
        }

        if args.tool == "javacg":
            loader = loaders[args.tool](input_file[args.tool], args.apppackages)
        else:
            loader = loaders[args.tool](input_file[args.tool], args.reverse)

        call_graph = CallGraph.from_loader(loader)

    formatter = formatters[args.format](call_graph)

    if args.summary:
        print(formatter.write_summary())
    else:
        print(formatter.write_output())

    if args.show_errors:
        for m in call_graph.errors:
            print(m)


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

    parser.add_argument("-src", "--source",
                        help="Can be either the root directory of the source code to analyze or the text file that "
                             "contains the raw call graph information. Use this when specifying only one call graph "
                             "generation tool with the -t (--tool) option.")
    parser.add_argument("-cf", "--cflowfile",
                        help="The file containing cflow's output.")
    parser.add_argument("-gf", "--gproffile",
                        help="The file containing gprof's output")
    parser.add_argument("-jf", "--javacgfile",
                        help="The file containing java-callgraph's output")

    # TODO: Change this "all" option so that it reflects what it actually is: using both cflow and gprof files.
    parser.add_argument("-t", "--tool", choices=["cflow", "gprof", "all", "javacg"], default="cflow",
                        help="The call graph generation software to use. Choose both to use both tools.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")
    parser.add_argument("-ap", "--apppackages", metavar='P', nargs="*",
                        help="When using java-callgraph for call graph generation of android apps, "
                             "specify the fully qualified package name of the method calls that will"
                             "be included in the call graph. This is generally the name of the java package"
                             "inside which the app's classes are defined.")

    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics report.")
    parser.add_argument("-s", "--summary", action="store_true",
                        help="Print only a summary of the report.")
    parser.add_argument("-e", "--show_errors", action="store_true",
                        help="Print all parsing error messages at the end of the report")

    return parser.parse_args()


if __name__ == '__main__':
    main()
