__author__ = 'kevin'

import psycopg2
import os.path

from attacksurfacemeter.formatters.base_formatter import BaseFormatter

# TODO: refactor magic strings and numbers.

class PgsqlFormatter(BaseFormatter):

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

    def init_database(self):
        db = psycopg2.connect(self.connection_string)
        cursor = db.cursor()

        create_database = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database.create.pgsql.sql")

        with open(create_database, "r") as create_database:
            create_table_commands = create_database.read().split("// separator")

            for create_table_command in create_table_commands:
                cursor.execute(create_table_command)

        db.commit()
        cursor.close()
        db.close()

    def write_summary(self):
        raise NotImplementedError("Operation not supported. Use write_output instead.")

    def write_output(self):
        db = psycopg2.connect(self.connection_string)
        cursor = db.cursor()

        attack_surface_to_insert = (self.source, 
                                    self.nodes_count, 
                                    self.edges_count, 
                                    self.entry_points_count,
                                    self.exit_points_count, 
                                    len(self.call_graph.attack_surface_graph_nodes),
                                    self.entry_points_clustering, 
                                    self.exit_points_clustering, 
                                    self.execution_paths_count,
                                    self.average_execution_path_length, 
                                    self.median_execution_path_length,
                                    self.median_closeness, 
                                    self.average_closeness, 
                                    self.median_betweenness,
                                    self.average_betweenness, 
                                    self.median_degree_centrality, 
                                    self.average_degree_centrality,
                                    self.median_in_degree_centrality, 
                                    self.average_in_degree_centrality,
                                    self.median_out_degree_centrality, 
                                    self.average_out_degree_centrality, 
                                    self.median_degree,
                                    self.average_degree, 
                                    self.median_in_degree, 
                                    self.average_in_degree, 
                                    self.median_out_degree,
                                    self.average_out_degree)

        cursor.execute(self.attack_surface_insert_stmt, attack_surface_to_insert)

        new_attack_surface_id = cursor.fetchone()[0]

        nodes_to_insert = [(new_attack_surface_id,
                            c.function_name,
                            c.function_signature,
                            self.get_closeness(c),
                            self.get_betweenness(c),
                            self.get_degree_centrality(c),
                            self.get_in_degree_centrality(c),
                            self.get_out_degree_centrality(c),
                            self.get_degree(c),
                            self.get_in_degree(c),
                            self.get_out_degree(c),
                            self.get_descendants_entry_point_ratio(c),
                            self.get_descendants_exit_point_ratio(c),
                            self.get_ancestors_entry_point_ratio(c),
                            self.get_ancestors_exit_point_ratio(c),
                            self.get_descendant_entry_points_count(c),
                            self.get_descendant_exit_points_count(c),
                            self.get_ancestor_entry_points_count(c),
                            self.get_ancestor_exit_points_count(c),
                            c in self.entry_points,
                            c in self.exit_points,
                            c in self.call_graph.attack_surface_graph_nodes,
                            self.call_graph.get_entry_point_reachability(c),
                            self.call_graph.get_shallow_entry_point_reachability(c),
                            self.call_graph.get_shallow_entry_point_reachability(c, depth=2),
                            self.call_graph.get_exit_point_reachability(c),
                            self.call_graph.get_page_rank(c),
                            self.call_graph.get_entry_page_rank(c),
                            self.call_graph.get_exit_page_rank(c))
                           for c in self.nodes]

        cursor.executemany(self.node_insert_stmt, nodes_to_insert)

        edges_to_insert = []

        for edge in self.edges:
            cursor.execute(self.node_select_id_stmt,
                           (new_attack_surface_id, edge[0].function_name, edge[0].function_signature))
            caller_id = cursor.fetchone()[0]

            cursor.execute(self.node_select_id_stmt,
                           (new_attack_surface_id, edge[1].function_name, edge[1].function_signature))
            callee_id = cursor.fetchone()[0]

            edges_to_insert.append((caller_id, callee_id))

        cursor.executemany(self.edge_insert_stmt, edges_to_insert)

        for call in self.nodes:
            cursor.execute(self.node_select_id_stmt,
                           (new_attack_surface_id, call.function_name, call.function_signature))
            node_id = cursor.fetchone()[0]

            self._insert_relations(new_attack_surface_id, node_id,
                                   self.get_descendant_entry_points(call),
                                   self.descendant_entry_points_insert_stmt,
                                   cursor)

            self._insert_relations(new_attack_surface_id, node_id,
                                   self.get_descendant_exit_points(call),
                                   self.descendant_exit_points_insert_stmt,
                                   cursor)

            self._insert_relations(new_attack_surface_id, node_id,
                                   self.get_ancestor_entry_points(call),
                                   self.ancestor_entry_points_insert_stmt,
                                   cursor)

            self._insert_relations(new_attack_surface_id, node_id,
                                   self.get_ancestor_exit_points(call),
                                   self.ancestor_exit_points_insert_stmt,
                                   cursor)

        db.commit()
        cursor.close()
        db.close()

    def _insert_relations(self, attack_surface_id, node_id, relations, relation_insert_stmt, cursor):
        relations_to_insert = []

        for relation in relations:
            cursor.execute(self.node_select_id_stmt,
                           (attack_surface_id, relation.function_name, relation.function_signature))

            relation_node_id = cursor.fetchone()[0]

            relations_to_insert.append((node_id, relation_node_id))

        cursor.executemany(relation_insert_stmt, relations_to_insert)

    @property
    def template_file(self):
        return ""

    @property
    def summary_template_file(self):
        return ""