__author__ = 'kevin'

import argparse
import sqlite3

from loaders.javacg_loader import JavaCGLoader


def main():

    args = parse_args()

    loader = JavaCGLoader(args.javacgfile)
    call_graph = loader.load_call_graph()

    edges_to_insert = [(e[0].identity, e[1].identity, args.application) for e in call_graph.edges()]

    with sqlite3.connect('extras/android.cg.db') as db:
        # db.row_factory = sqlite3.Row

        db.executemany('INSERT INTO edges (caller, callee, app) VALUES (?, ?, ?)', edges_to_insert)


def parse_args():
    """
        Provides a command line interface.

        Defines all the positional and optional arguments along with their respective valid values
        for the command line interface and returns all the received arguments as an object.

        Returns:
            An object that contains all the provided command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes a software's source code and reports various metrics related to it's attack surface.")

    parser.add_argument("-jf", "--javacgfile",
                        help="The file containing java-callgraph's output")

    parser.add_argument("-app", "--application",
                        help="The name of the application from which this callgraph was generated")

    return parser.parse_args()


if __name__ == '__main__':
    main()
