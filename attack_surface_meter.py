import argparse
import os
import sys

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.granularity import Granularity
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader
from attacksurfacemeter.loaders.multigprof_loader import MultigprofLoader
from attacksurfacemeter.loaders.javacg_loader import JavaCGLoader
from attacksurfacemeter.formatters.txt_formatter import TxtFormatter
from attacksurfacemeter.formatters.xml_formatter import XmlFormatter
from attacksurfacemeter.formatters.html_formatter import HtmlFormatter


FORMATTERS = {
    'txt': TxtFormatter, 'xml': XmlFormatter, 'html': HtmlFormatter
}


def main():
    args = parse_args()

    call_graph = None
    if args.javacg:
        loader = JavaCGLoader(
            args.javacg, args.apppackages
        )
        call_graph = CallGraph.from_loader(loader)
    else:
        cflow_loader = None
        gprof_loader = None
        if args.cflow:
            if not os.path.exists(args.cflow):
                raise Exception('{} not found.'.format(args.cflow))
            else:
                cflow_loader = CflowLoader(args.cflow, reverse=args.reverse)

        if args.gprof:
            if not os.path.exists(args.gprof):
                raise Exception('{} not found.'.format(args.gprof))
            else:
                if os.path.isdir(args.gprof):
                    sources = [
                        os.path.join(args.gprof, filename)
                        for filename in os.listdir(args.gprof)
                        if os.path.isfile(os.path.join(args.gprof, filename))
                    ]
                    gprof_loader = MultigprofLoader(
                        sources, processes=args.processes
                    )
                else:
                    gprof_loader = GprofLoader(
                        args.gprof
                    )

        if cflow_loader and gprof_loader:
            call_graph = CallGraph.from_merge(
                CallGraph.from_loader(
                    cflow_loader, granularity=args.granularity
                ),
                CallGraph.from_loader(
                    gprof_loader, granularity=args.granularity
                )
            )
        elif cflow_loader:
            call_graph = CallGraph.from_loader(
                    cflow_loader, granularity=args.granularity
                )
        elif gprof_loader:
            call_graph = CallGraph.from_loader(
                    gprof_loader, granularity=args.granularity
                )

    if args.output:
        (name, extension) = os.path.splitext(args.output)
        output_format = extension.replace('.', '')
        if output_format not in FORMATTERS:
            output_format = 'txt'
        formatter = FORMATTERS[output_format](call_graph)
        with open(args.output, 'w') as file_:
            if args.verbose:
                file_.write(formatter.write_output())
            else:
                file_.write(formatter.write_summary())
    else:
        formatter = FORMATTERS['txt'](call_graph)
        if args.verbose:
            sys.stdout.write(formatter.write_output())
        else:
            sys.stdout.write(formatter.write_summary())

    if args.showerrors and call_graph.load_errors:
        sys.stdout.write('Parse Errors\n')
        sys.stdout.write('============\n')
        for error in call_graph.load_errors:
            sys.stdout.write(error)


def parse_args():
    '''Parse command line arguments.

    Parameters
    ----------
    None

    Returns
    -------
    args : object
        An object containing the command line arguments are attributes.
    '''
    parser = argparse.ArgumentParser(
        description=(
            'Collect attack surface metrics from the call graph '
            ' representation of a software system.'
        )
    )
    parser.add_argument(
        '-gr', dest='granularity', default=Granularity.FUNC,
        choices=[Granularity.FUNC, Granularity.FILE],
        help=(
            'The granularity at which the call graphs must be processed at.'
        )
    )
    parser.add_argument(
        '-c', dest='cflow',
        help=(
            'Absolute path of the file containing the textual representation '
            'of the call graph generated by GNU cflow or of the directory '
            'containing the source code of the software system to be analyzed.'
        )
    )
    parser.add_argument(
        '--reverse', action='store_true',
        help='cflow call graph was generated with the -r option.'
    )
    parser.add_argument(
        '-g', dest='gprof',
        help=(
            'Absolute path of the file containing the textual representation '
            'of the call graph generated by GNU gprof or of a directory '
            'containing multiple such text files.'
        )
    )
    parser.add_argument(
        '-p', dest='processes', type=int, default=2,
        help=(
            'Number of processes to spawn when loaded multiple gprof call '
            'graph files. Default is 2.'
        )
    )
    parser.add_argument(
        '-j', dest='javacg',
        help=(
            'Absolute path of the file containing the textual representation '
            'of the call graph generated by java-callgraph.'
        )
    )
    parser.add_argument(
        '-a', dest='apppackages', metavar='P', nargs='*',
        help=(
            'When using java-callgraph for call graph generation of android '
            'apps, specify the fully qualified package name of the method '
            'calls that will be included in the call graph. This is generally '
            'the name of the java package inside which the app\'s classes are '
            'defined.'
        )
    )
    parser.add_argument(
        '--output',
        help=(
            'Absolute path of the file to which the output should be written '
            'to. The format of output is inferred from the file extension. '
            'txt, html, and xml are currently supported. In cases when the '
            'output format cannot be inferred, txt is used. When an output '
            'path is not specified, standard output is used.'
        )
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help=(
            'Output itemized report including metric values collected for '
            'each function/file.'
        )
    )
    parser.add_argument(
        '--showerrors', action='store_true',
        help='Display errors encountered when parsing call graph (if any).'
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
