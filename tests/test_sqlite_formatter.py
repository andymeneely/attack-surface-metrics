__author__ = 'kevin'

import unittest
import os
import sqlite3

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.formatters.sqlite_formatter import SqliteFormatter

@unittest.skip('Temporarily skipped.')
class SqliteFormatterTestCase(unittest.TestCase):

    temp_database_file = "temp.db"

    def setUp(self):
        self.call_graph = CallGraph.from_loader(
            CflowLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     "helloworld/cflow.callgraph.txt")))

        self.formatter = SqliteFormatter(self.call_graph, self.temp_database_file)

        self.test_oracle_database_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/attack_surface.cg.db")

    def tearDown(self):
        os.remove(self.temp_database_file)

    def test_init_database(self):
        # Arrange
        db = sqlite3.connect(self.test_oracle_database_file)
        c = db.cursor()
        c.execute("SELECT tbl_name, sql FROM sqlite_master;")
        expected_content = c.fetchall()
        c.close()
        db.close()

        # Act
        self.formatter.init_database()
        db = sqlite3.connect(self.temp_database_file)
        c = db.cursor()
        c.execute("SELECT tbl_name, sql FROM sqlite_master;")
        created_tables = c.fetchall()
        c.close()
        db.close()

        # Assert
        self.assertEqual(expected_content, created_tables)

    def test_write_output(self):
        # Arrange
        attack_surface_select_stmt = '''SELECT id, nodes_count, edges_count, entry_points_count, exit_points_count, 
                                        attack_surface_nodes_count, entry_points_clustering, exit_points_clustering,
                                        execution_paths_count, execution_paths_average, execution_paths_median,
                                        median_closeness, average_closeness, median_betweenness, average_betweenness,
                                        median_degree_centrality, average_degree_centrality, median_in_degree_centrality,
                                        average_in_degree_centrality, median_out_degree_centrality,
                                        average_out_degree_centrality, median_degree, average_degree,
                                        median_in_degree, average_in_degree, median_out_degree, average_out_degree
                                        FROM attack_surfaces;'''

        node_select_stmt = '''SELECT attack_surface_id, function_name, function_signature, closeness, betweenness,
                              degree_centrality, in_degree_centrality, out_degree_centrality, degree, in_degree, 
                              out_degree, descendant_entry_points_ratio, descendant_exit_points_ratio, 
                              ancestor_entry_points_ratio, ancestor_exit_points_ratio, descendant_entry_points_count, 
                              descendant_exit_points_count, ancestor_entry_points_count, ancestor_exit_points_count, 
                              is_entry_point, is_exit_point, is_in_attack_surface, entry_point_reachability, 
                              shallow_entry_point_reachability_depth_1, shallow_entry_point_reachability_depth_2, 
                              exit_point_reachability, page_rank, entry_page_rank, exit_page_rank 
                              FROM nodes;'''
        
        edge_select_stmt = '''SELECT caller_node.function_name, caller_node.function_signature, 
                              callee_node.function_name, callee_node.function_signature 
                              FROM edges as e 
                              INNER JOIN nodes as caller_node ON e.caller_node_id = caller_node.id 
                              INNER JOIN nodes as callee_node ON e.callee_node_id = callee_node.id;'''
        
        descendant_entry_points_select_stmt = '''SELECT node.function_name, node.function_signature, 
                                                 descendant.function_name, descendant.function_signature 
                                                 FROM descendant_entry_points as dep 
                                                 INNER JOIN nodes as node ON dep.node_id = node.id 
                                                 INNER JOIN nodes as descendant ON dep.node_id = descendant.id;'''
        
        descendant_exit_points_select_stmt = '''SELECT node.function_name, node.function_signature, 
                                                descendant.function_name, descendant.function_signature
                                                FROM descendant_exit_points as dep
                                                INNER JOIN nodes as node ON dep.node_id = node.id
                                                INNER JOIN nodes as descendant ON dep.node_id = descendant.id;'''
        
        ancestor_entry_points_select_stmt = '''SELECT node.function_name, node.function_signature,
                                               ancestor.function_name, ancestor.function_signature
                                               FROM ancestor_entry_points as aep
                                               INNER JOIN nodes as node ON aep.node_id = node.id
                                               INNER JOIN nodes as ancestor ON aep.node_id = ancestor.id;'''
        
        ancestor_exit_points_select_stmt = '''SELECT node.function_name, node.function_signature,
                                              ancestor.function_name, ancestor.function_signature
                                              FROM ancestor_exit_points as aep
                                              INNER JOIN nodes as node ON aep.node_id = node.id
                                              INNER JOIN nodes as ancestor ON aep.node_id = ancestor.id;'''

        db = sqlite3.connect(self.test_oracle_database_file)
        c = db.cursor()
        
        c.execute(attack_surface_select_stmt)
        expected_attack_surfaces = c.fetchall()

        c.execute(node_select_stmt)
        expected_nodes = c.fetchall()

        c.execute(edge_select_stmt)
        expected_edges = c.fetchall()

        c.execute(descendant_entry_points_select_stmt)
        expected_descendant_entry_points = c.fetchall()

        c.execute(descendant_exit_points_select_stmt)
        expected_descendant_exit_points = c.fetchall()

        c.execute(ancestor_entry_points_select_stmt)
        expected_ancestor_entry_points = c.fetchall()

        c.execute(ancestor_exit_points_select_stmt)
        expected_ancestor_exit_points = c.fetchall()

        c.close()
        db.close()

        # Act
        self.formatter.init_database()
        self.formatter.write_output()

        db = sqlite3.connect(self.temp_database_file)
        c = db.cursor()

        c.execute(attack_surface_select_stmt)
        created_attack_surfaces = c.fetchall()

        c.execute(node_select_stmt)
        created_nodes = c.fetchall()

        c.execute(edge_select_stmt)
        created_edges = c.fetchall()

        c.execute(descendant_entry_points_select_stmt)
        created_descendant_entry_points = c.fetchall()

        c.execute(descendant_exit_points_select_stmt)
        created_descendant_exit_points = c.fetchall()

        c.execute(ancestor_entry_points_select_stmt)
        created_ancestor_entry_points = c.fetchall()

        c.execute(ancestor_exit_points_select_stmt)
        created_ancestor_exit_points = c.fetchall()

        c.close()
        db.close()

        # Assert
        self.assertEqual(expected_attack_surfaces, created_attack_surfaces)

        # Assert all of the non page rank fields.
        self.assertEquals(sorted([n[:-3] for n in expected_nodes]), sorted([n[:-3] for n in created_nodes]))

        # Assert the page rank fields. They are slightly different each time they are calculated.
        # Hence the Almost Equal assertion
        expected_nodes = sorted(expected_nodes)
        created_nodes = sorted(created_nodes)

        for i in range(0, len(expected_nodes)):
            self.assertAlmostEquals(expected_nodes[i][-3], created_nodes[i][-3])
            self.assertAlmostEquals(expected_nodes[i][-2], created_nodes[i][-2])
            self.assertAlmostEquals(expected_nodes[i][-1], created_nodes[i][-1])

        # Assert everything else
        self.assertEquals(sorted(expected_edges), sorted(created_edges))
        self.assertEquals(sorted(expected_descendant_entry_points), sorted(created_descendant_entry_points))
        self.assertEquals(sorted(expected_descendant_exit_points), sorted(created_descendant_exit_points))
        self.assertEquals(sorted(expected_ancestor_entry_points), sorted(created_ancestor_entry_points))
        self.assertEquals(sorted(expected_ancestor_exit_points), sorted(created_ancestor_exit_points))


if __name__ == '__main__':
    unittest.main()
