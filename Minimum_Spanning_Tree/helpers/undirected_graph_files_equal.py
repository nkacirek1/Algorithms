from Minimum_Spanning_Tree.helpers.undirected_graph import Graph

#Use for testing

def read_weighted_undirected_graph(filename):
    """A helper to read the edges of a graph described in the file
    into a graph object."""
    g = Graph()
    with open(filename) as f:
        for line in f:
            try:
                v1, v2, w = line.split()
                g.add_edge(v1, v2, {'weight': int(w)})
            except:
                pass
    return g


def graph_files_equal(filename1, filename2):
    """Compares two graphs to see if they contain the same edges.
    Here, the files specifying the graphs describe one edge per line in
    the format: <a node> <another node> <weight of edge>, just like the
    format produced by the graph generator functions."""
    g1 = read_weighted_undirected_graph(filename1)
    g2 = read_weighted_undirected_graph(filename2)
    # Calls the __eq__(self, other) method of the g1 Graph object
    return g1 == g2
