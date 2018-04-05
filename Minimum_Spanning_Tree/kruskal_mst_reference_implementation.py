from Minimum_Spanning_Tree.helpers.undirected_graph import Graph


def initialize_disjoint_set(items):
    return {item: None for item in items}


def canonical_item(ds, item):
    path = [item]
    parent = ds[path[-1]]
    while parent:
        path.append(parent)
        parent = ds[path[-1]]
    for i in path[:-1]:
        ds[i] = path[-1]
    return path[-1]


def same_set(ds, item1, item2):
    c1 = canonical_item(ds, item1)
    c2 = canonical_item(ds, item2)
    return c1 == c2


def merge_sets(ds, item1, item2):
    c1 = canonical_item(ds, item1)
    c2 = canonical_item(ds, item2)
    ds[c1] = c2


def read_weighted_undirected_graph(filename):
    g = Graph()
    with open(filename) as f:
        for line in f:
            try:
                v1, v2, w = line.split()
                g.add_edge(v1, v2, {'weight': int(w)})
            except:
                pass
    return g


def write_tree_edges_to_file(edges, filename):
    with open(filename, mode='w') as f:
        for v1, v2, w in edges:
            f.write("{} {} {}\n".format(v1, v2, w))


def compute_mst(filename):
    g = read_weighted_undirected_graph(filename)
    import time
    start_time = time.process_time()
    node_sets = initialize_disjoint_set(g.get_nodes())
    node_count = len(node_sets)
    edges = [(g.attributes_of(v, u)['weight'], v, u) for u,v in g.get_edges()]
    edges.sort()
    tree_edges = []
    for weight, v, u in edges:
        if not same_set(node_sets, v, u):
            tree_edges.append((v, u, weight))
            merge_sets(node_sets, v, u)
        if len(tree_edges) == node_count - 1:
            break
    end_time = time.process_time()
    write_tree_edges_to_file(tree_edges, filename + '.kruskal.mst')
    print("Ran in: {:.5f} secs".format(end_time - start_time))

if __name__ == '__main__':
    import sys
    # compute_mst(sys.argv[1])
    compute_mst(sys.argv[1])