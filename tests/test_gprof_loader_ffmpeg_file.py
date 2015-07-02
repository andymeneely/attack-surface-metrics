import os
import unittest

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class GprofLoaderFFmpegFileTestCase(unittest.TestCase):
    def setUp(self):
        self.target = GprofLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'ffmpeg/gprof.callgraph.txt'
            ),
            False
        )

    def test_load_call_graph_errors(self):
        # Act
        graph = self.target.load_call_graph()

        # Assert
        self.assertEqual(1, len(self.target.errors))

    def test_load_call_graph_nodes(self):
        # Arrange
        expected = [
            Call('opt_progress', './ffmpeg_opt.c', Environments.C),
            Call('get_preset_file_2', './ffmpeg_opt.c', Environments.C),
            Call('dump_attachment', './ffmpeg_opt.c', Environments.C),
            Call('open_output_file', './ffmpeg_opt.c', Environments.C),
            Call('init_input', './libavformat/utils.c', Environments.C),
            Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
            Call('ffurl_open', './libavformat/avio.c', Environments.C),
            Call('biquad_s16', './libavfilter/af_biquads.c', Environments.C),
            Call('av_log', './libavutil/log.c', Environments.C)
        ]

        # Act
        graph = self.target.load_call_graph()
        actual = graph.nodes()

        # Assert
        self.assertCountEqual(expected, actual)
        for (_, attrs) in graph.nodes(data=True):
            self.assertTrue('tested' in attrs)
            self.assertTrue('defense' not in attrs)
            self.assertTrue('dangerous' not in attrs)
            self.assertTrue('vulnerable' not in attrs)

    def test_load_call_graph_entry_nodes(self):
        # Arrange
        expected = []

        # Act
        graph = self.target.load_call_graph()

        # Assert
        for (n, attrs) in graph.nodes(data=True):
            if n in expected:
                self.assertTrue('entry' in attrs)
            else:
                self.assertTrue('entry' not in attrs)

    def test_load_call_graph_exit_nodes(self):
        # Arrange
        expected = []

        # Act
        graph = self.target.load_call_graph()

        # Assert
        for (n, attrs) in graph.nodes(data=True):
            if n in expected:
                self.assertTrue('exit' in attrs)
            else:
                self.assertTrue('exit' not in attrs)

    def test_load_call_graph_edges(self):
        # Arrange
        expected = [
            (
                Call('opt_progress', './ffmpeg_opt.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('opt_progress', './ffmpeg_opt.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('get_preset_file_2', './ffmpeg_opt.c', Environments.C)
            ),
            (
                Call('get_preset_file_2', './ffmpeg_opt.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call('dump_attachment', './ffmpeg_opt.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('dump_attachment', './ffmpeg_opt.c', Environments.C)
            ),
            (
                Call('open_output_file', './ffmpeg_opt.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('open_output_file', './ffmpeg_opt.c', Environments.C)
            ),
            (
                Call('init_input', './libavformat/utils.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('init_input', './libavformat/utils.c', Environments.C)
            ),
            (
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C),
                Call('ffurl_open', './libavformat/avio.c', Environments.C)
            ),
            (
                Call('ffurl_open', './libavformat/avio.c', Environments.C),
                Call('avio_open2', './libavformat/aviobuf.c', Environments.C)
            ),
            (
                Call(
                    'biquad_s16', './libavfilter/af_biquads.c', Environments.C
                ),
                Call('av_log', './libavutil/log.c', Environments.C)
            ),
            (
                Call('av_log', './libavutil/log.c', Environments.C),
                Call(
                    'biquad_s16', './libavfilter/af_biquads.c', Environments.C
                )
            ),
        ]

        # Act
        graph = self.target.load_call_graph()
        actual = graph.edges()

        # Assert
        self.assertCountEqual(expected, actual)
        for (_, _, attrs) in graph.edges(data=True):
            self.assertTrue('gprof' in attrs)
            self.assertTrue('cflow' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_load_call_graph_return_edges(self):
        # Act
        graph = self.target.load_call_graph()

        # Assert
        for (u, v) in nx.get_edge_attributes(graph, 'call'):
            self.assertTrue('return' in graph[v][u])

if __name__ == '__main__':
    unittest.main()
