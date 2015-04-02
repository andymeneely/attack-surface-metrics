__author__ = 'kevin'

import sqlite3

from attacksurfacemeter.formatters.database_formatter import DatabaseFormatter

# TODO: refactor magic strings and numbers.


class SqliteFormatter(DatabaseFormatter):

    attack_surface_insert_stmt = '''INSERT INTO attack_surfaces(source, nodes_count, edges_count, entry_points_count,
        exit_points_count, attack_surface_nodes_count, entry_points_clustering, exit_points_clustering,
        execution_paths_count, execution_paths_average, execution_paths_median, median_closeness, average_closeness,
        median_betweenness, average_betweenness, median_degree_centrality, average_degree_centrality,
        median_in_degree_centrality, average_in_degree_centrality, median_out_degree_centrality,
        average_out_degree_centrality, median_degree, average_degree, median_in_degree, average_in_degree,
        median_out_degree, average_out_degree)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    
    node_insert_stmt = '''INSERT INTO nodes(attack_surface_id, function_name, function_signature, closeness, 
        betweenness, degree_centrality, in_degree_centrality, out_degree_centrality, degree, in_degree, out_degree,
        descendant_entry_points_ratio, descendant_exit_points_ratio, ancestor_entry_points_ratio,
        ancestor_exit_points_ratio, descendant_entry_points_count, descendant_exit_points_count,
        ancestor_entry_points_count, ancestor_exit_points_count, is_entry_point, is_exit_point, is_in_attack_surface,
        entry_point_reachability, shallow_entry_point_reachability_depth_1, shallow_entry_point_reachability_depth_2,
        exit_point_reachability, page_rank, entry_page_rank, exit_page_rank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    node_select_id_stmt = '''SELECT id FROM nodes
                             WHERE attack_surface_id = ?
                             AND function_name = ?
                             AND function_signature = ?'''

    edge_insert_stmt = '''INSERT INTO edges(caller_node_id, callee_node_id)
                          VALUES (?, ?)'''

    descendant_entry_points_insert_stmt = '''INSERT INTO descendant_entry_points(node_id, descendant_node_id)
                                             VALUES (?, ?)'''

    descendant_exit_points_insert_stmt = '''INSERT INTO descendant_exit_points(node_id, descendant_node_id)
                                            VALUES (?, ?)'''

    ancestor_entry_points_insert_stmt = '''INSERT INTO ancestor_entry_points(node_id, ancestor_node_id)
                                            VALUES (?, ?)'''

    ancestor_exit_points_insert_stmt = '''INSERT INTO ancestor_exit_points(node_id, ancestor_node_id)
                                          VALUES (?, ?)'''

    def __init__(self, call_graph, database_file):
        super(SqliteFormatter, self).__init__(call_graph)
        self.database_file = database_file

    def get_connection(self):
        return sqlite3.connect(self.database_file)

    def get_database_init_script(self):
        return "database.create.sqlite.sql"

    def get_last_inserted_row_id(self, cursor):
        return cursor.lastrowid