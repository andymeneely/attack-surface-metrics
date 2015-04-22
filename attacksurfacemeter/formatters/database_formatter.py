__author__ = 'kevin'

import os.path

from attacksurfacemeter.formatters.base_formatter import BaseFormatter

# TODO: refactor magic strings and numbers.


class DatabaseFormatter(BaseFormatter):

    attack_surface_insert_stmt = ""
    node_insert_stmt = ""
    node_select_id_stmt = ""
    edge_insert_stmt = ""
    descendant_entry_points_insert_stmt = ""
    descendant_exit_points_insert_stmt = ""
    ancestor_entry_points_insert_stmt = ""
    ancestor_exit_points_insert_stmt = ""

    def __init__(self, call_graph):
        super(DatabaseFormatter, self).__init__(call_graph)

    def init_database(self):
        db = self.get_connection()
        cursor = db.cursor()

        create_database = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.get_database_init_script())

        with open(create_database, "r") as create_database:
            create_table_commands = create_database.read().split("// separator")

            for create_table_command in create_table_commands:
                cursor.execute(create_table_command)

        db.commit()
        cursor.close()
        db.close()

    def get_connection(self):
        return None

    def get_database_init_script(self):
        return ""

    def get_last_inserted_row_id(self, cursor):
        return 0

    def write_summary(self):
        raise NotImplementedError("Operation not supported. Use write_output instead.")

    def write_output(self):
        db = self.get_connection()
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

        new_attack_surface_id = self.get_last_inserted_row_id(cursor)

        nodes_to_insert = []

        for c in self.nodes:
            nodes_to_insert.append(
                (new_attack_surface_id,
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
                 self.call_graph.is_entry_point(c),
                 self.call_graph.is_exit_point(c),
                 c in self.call_graph.attack_surface_graph_nodes,
                 self.call_graph.get_entry_point_reachability(c),
                 self.call_graph.get_shallow_entry_point_reachability(c),
                 self.call_graph.get_shallow_entry_point_reachability(c, depth=2),
                 self.call_graph.get_exit_point_reachability(c),
                 self.call_graph.get_page_rank(c),
                 self.call_graph.get_entry_page_rank(c),
                 self.call_graph.get_exit_page_rank(c))
            )

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
        raise NotImplementedError("Operation not supported.")

    @property
    def summary_template_file(self):
        raise NotImplementedError("Operation not supported.")