__author__ = 'kevin'

import psycopg2

from attacksurfacemeter.formatters.database_formatter import DatabaseFormatter

# TODO: refactor magic strings and numbers.


class PgsqlFormatter(DatabaseFormatter):

    attack_surface_insert_stmt = '''INSERT INTO attack_surfaces(source, nodes_count, edges_count, entry_points_count,
        exit_points_count, attack_surface_nodes_count, entry_points_clustering, exit_points_clustering,
        execution_paths_count, execution_paths_average, execution_paths_median, median_closeness, average_closeness,
        median_betweenness, average_betweenness, median_degree_centrality, average_degree_centrality,
        median_in_degree_centrality, average_in_degree_centrality, median_out_degree_centrality,
        average_out_degree_centrality, median_degree, average_degree, median_in_degree, average_in_degree,
        median_out_degree, average_out_degree)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id'''
    
    node_insert_stmt = '''INSERT INTO nodes(attack_surface_id, function_name, function_signature, closeness, 
        betweenness, degree_centrality, in_degree_centrality, out_degree_centrality, degree, in_degree, out_degree,
        descendant_entry_points_ratio, descendant_exit_points_ratio, ancestor_entry_points_ratio,
        ancestor_exit_points_ratio, descendant_entry_points_count, descendant_exit_points_count,
        ancestor_entry_points_count, ancestor_exit_points_count, is_entry_point, is_exit_point, is_in_attack_surface,
        entry_point_reachability, shallow_entry_point_reachability_depth_1, shallow_entry_point_reachability_depth_2,
        exit_point_reachability, page_rank, entry_page_rank, exit_page_rank)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    node_select_id_stmt = '''SELECT id FROM nodes
                             WHERE attack_surface_id = %s
                             AND function_name = %s
                             AND function_signature = %s'''

    edge_insert_stmt = '''INSERT INTO edges(caller_node_id, callee_node_id)
                          VALUES (%s, %s)'''

    descendant_entry_points_insert_stmt = '''INSERT INTO descendant_entry_points(node_id, descendant_node_id)
                                             VALUES (%s, %s)'''

    descendant_exit_points_insert_stmt = '''INSERT INTO descendant_exit_points(node_id, descendant_node_id)
                                            VALUES (%s, %s)'''

    ancestor_entry_points_insert_stmt = '''INSERT INTO ancestor_entry_points(node_id, ancestor_node_id)
                                            VALUES (%s, %s)'''

    ancestor_exit_points_insert_stmt = '''INSERT INTO ancestor_exit_points(node_id, ancestor_node_id)
                                          VALUES (%s, %s)'''

    def __init__(self, call_graph, connection_string):
        super(PgsqlFormatter, self).__init__(call_graph)
        self.connection_string = connection_string

    def get_connection(self):
        return psycopg2.connect(self.connection_string)

    def get_database_init_script(self):
        return "database.create.pgsql.sql"

    def get_last_inserted_row_id(self, cursor):
        return cursor.fetchone()[0]