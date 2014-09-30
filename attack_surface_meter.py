__author__ = 'kevin'

import argparse

from attacksurfacemeter import CallGraph
from loaders import CflowLoader, GprofLoader
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

    if args.tool == "all":
        # TODO: Maybe it would be useful to have some sort of factory method here because
        # of different constructor signatures for different loaders. I.e. gprof doesn't
        # support a reverse option so its not necessary to send it as a parameter.
        cflow_loader = loaders['cflow'](args.cflowfile, args.reverse)
        gprof_loader = loaders['gprof'](args.gproffile, args.reverse)

        call_graph = CallGraph.from_merge(CallGraph.from_loader(cflow_loader),
                                          CallGraph.from_loader(gprof_loader))
    else:
        if_not_none = lambda arg: arg if arg is not None else args.source

        input_file = {
            'cflow': if_not_none(args.cflowfile),  # args.cflowfile if args.cflowfile is not None else args.source,
            'gprof': if_not_none(args.gproffile)  # args.gproffile if args.gproffile is not None else args.source,
        }

        loader = loaders[args.tool](input_file[args.tool], args.reverse)

        call_graph = CallGraph.from_loader(loader)

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

    parser.add_argument("-src", "--source",
                        help="Can be either the root directory of the source code to analyze or the text file that "
                             "contains the raw call graph information. Use this when specifying only one call graph "
                             "generation tool with the -t (--tool) option.")
    parser.add_argument("-cf", "--cflowfile",
                        help="The file containing cflow's output.")
    parser.add_argument("-gf", "--gproffile",
                        help="The file containing gprof's output")
    parser.add_argument("-t", "--tool", choices=["cflow", "gprof", "all"], default="cflow",
                        help="The call graph generation software to use. Choose both to use both tools.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")
    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics report.")
    parser.add_argument("-s", "--summary", action="store_true",
                        help="Print only a summary of the report.")

    return parser.parse_args()


if __name__ == '__main__':
    main()