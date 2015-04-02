CREATE TABLE attack_surfaces
(
    id SERIAL PRIMARY KEY NOT NULL,
    source TEXT,

    nodes_count INT,
    edges_count INT,

    entry_points_count INT,
    exit_points_count INT,

    attack_surface_nodes_count INT,

    entry_points_clustering REAL,
    exit_points_clustering REAL,

    execution_paths_count INT,
    execution_paths_average REAL,
    execution_paths_median REAL,

    median_closeness REAL,
    average_closeness REAL,

    median_betweenness REAL,
    average_betweenness REAL,

    median_degree_centrality REAL,
    average_degree_centrality REAL,
    median_in_degree_centrality REAL,
    average_in_degree_centrality REAL,
    median_out_degree_centrality REAL,
    average_out_degree_centrality REAL,

    median_degree REAL,
    average_degree REAL,
    median_in_degree REAL,
    average_in_degree REAL,
    median_out_degree REAL,
    average_out_degree REAL
);
// separator
CREATE TABLE nodes
(
    id SERIAL PRIMARY KEY NOT NULL,
    attack_surface_id INTEGER,
    function_name TEXT,
    function_signature TEXT,

    closeness REAL,
    betweenness REAL,

    degree_centrality REAL,
    in_degree_centrality REAL,
    out_degree_centrality REAL,

    degree INTEGER,
    in_degree INTEGER,
    out_degree INTEGER,

    descendant_entry_points_ratio REAL,
    descendant_exit_points_ratio REAL,
    ancestor_entry_points_ratio REAL,
    ancestor_exit_points_ratio REAL,

    descendant_entry_points_count INTEGER,
    descendant_exit_points_count INTEGER,
    ancestor_entry_points_count INTEGER,
    ancestor_exit_points_count INTEGER,

    is_entry_point BOOLEAN,
    is_exit_point BOOLEAN,
    is_in_attack_surface BOOLEAN,

    entry_point_reachability REAL,
    shallow_entry_point_reachability_depth_1 REAL,
    shallow_entry_point_reachability_depth_2 REAL,
    exit_point_reachability REAL,

    page_rank REAL,
    entry_page_rank REAL,
    exit_page_rank REAL
);
// separator
CREATE TABLE descendant_entry_points
(
    id SERIAL PRIMARY KEY NOT NULL,
    node_id INTEGER,
    descendant_node_id INTEGER
);
// separator
CREATE TABLE descendant_exit_points
(
    id SERIAL PRIMARY KEY NOT NULL,
    node_id INTEGER,
    descendant_node_id INTEGER
);
// separator
CREATE TABLE ancestor_entry_points
(
    id SERIAL PRIMARY KEY NOT NULL,
    node_id INTEGER,
    ancestor_node_id INTEGER
);
// separator
CREATE TABLE ancestor_exit_points
(
    id SERIAL PRIMARY KEY NOT NULL,
    node_id INTEGER,
    ancestor_node_id INTEGER
);
// separator
CREATE TABLE edges
(
    id SERIAL PRIMARY KEY NOT NULL,
    caller_node_id INTEGER,
    callee_node_id INTEGER
);