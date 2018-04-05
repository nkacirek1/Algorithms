from Minimum_Spanning_Tree.helpers.undirected_graph import Graph
import heapq


def write_tree_edges_to_file(edges, filename):
    with open(filename, 'w') as file:
        for x in range (1, len(edges)):
            file.write(edges[x] + '\n')

def compute_mst(filename):

    #convert the file to a graph using undirected_graph.py
    g = Graph()
    #data is a list of lists for each row/edge ['v0', 'v1', edge weight]
    data = read_numbers_by_row(filename)
    # print("data:", data)
    for i in range (0, len(data)):
        g.add_edge(data[i][0], data[i][1], {'weight': int(data[i][2])})

    '''Use Prim's algorithm to compute the minimum spanning tree of the weighted undirected graph
    described by the contents of the file named filename.'''
    tree_edges = []

    # V is a list with all of the nodes in it
    V = list(g.get_nodes())
    #min priority queue Q = {}
    q = []
    S = set()
    import time
    start_time = time.process_time()
    # a[starting node] = 0 - first node read in is the starting node
    heapq.heappush(q, (0, None, V[0]))
    #while Q is not empty:
    while q:
        #extract the min element from Q and put into u
        w, pi, u = heapq.heappop(q)
        # Add u to set S
        add = str(pi) + " " + str(u) + " " + str(w)
        if u not in S:
            tree_edges.append(add)
            S.add(u)
            #for each edge e = (u,v) incident to u
            #dictionary of all the edges
            edges = g.edges[u]
            adj = list(g.neighbors(u))
            for i in range (0, len(adj)):
                v = adj[i]
                weight = edges[v]['weight']
                #if ((v is not in S) and ( the weight of e is < a[v] )
                    #decrease priority a[v] to the weight of e
                    #v.pi = u
                # cole's method: add tuple to the priority queue
                heapq.heappush(q, (weight, u, v))
    end_time = time.process_time()
    write_tree_edges_to_file(tree_edges, filename + '_Output.mst')
    print("Ran in: {:.5f} secs".format(end_time - start_time))

def read_lines(filename):
    with open(filename) as f:
        return f.readlines()


def parse_line(line):
    return [x for x in line.split()]


def read_numbers_by_row(filename):
    lines = read_lines(filename)
    return [parse_line(line) for line in lines]


if __name__ == '__main__':
    import sys
    # compute_mst(sys.argv[1])
    compute_mst(sys.argv[1])

