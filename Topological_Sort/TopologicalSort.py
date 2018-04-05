from Topological_Sort.helpers import graph


def read_topo_sort_from_file(filename):
    """This reads the first line of the file. In a topological sort solution file,
    the first line holds the nodes in topological sort order on the first line,
    separated by whitespace."""
    with open(filename) as f:
        string = f.readline()
    return string


def parse_tps(tps_str):
    """ Gets a string of ordering of nodes for topological
    ordering and creates a list of integers from that. """
    return [int(x) for x in tps_str.split()]


def contains_sink_node(graph):
    """ Checks if there is a node without outgoing edge. """
    # empty collections are boolean false, so this asks if all
    # nodes have a non-empty set of neighbors (outgoing edges)
    return all(graph[i] for i in graph)


def check_TPS(graph, tps):
    """ Takes a out-edge graph dictionary and a list of integers for
    topological ordering and checks if that topological ordering is correct. """
    for i in reversed(range(len(tps))):
        for j in range(i):
            if tps[j] in graph[tps[i]]:
                print("Fault: There is a backward edge from ", tps[i], " to ", tps[j])
                return False
    if len(graph.keys()) != len(tps):
        return False
    return True


def write_tps_to_file(tps, filename):
    with open('output_' + filename, 'w') as file:
        for node in tps:
            file.write(node + ' ')



def compute_tps(filename):
    # read in input file
    import time
    start_time = time.process_time()
     # For each edge (line in filename) there is a source node, space, and then the destination node.
        # There is an edge from the first number (node) to the second number (node)
     # The graphs may have multiple connected components. Your answer should cover all the nodes of the graph

    # Using the function 'read_double_graph', you can read the input graph to 2 dictionaries; one for the outgoing edges
     # of the graph, and one for the incoming edges. key is a node and the value for that is the number
    # of incoming/outgoing edges.
    #adjList
    adjList, in_graph = graph.read_double_graph(filename)

    # V = the list of all nodes - in the order they are read in the from the file
    V = list(adjList.keys())

    #need to store the node info : node, color, u.disovceryTime, u.finishTime, p (pi) - predecessor
    color = {}
    discovery = {}
    finish = {}
    pred = {}
    for node in range(0, len(V)):
        color[V[node]] = 'w'
        discovery[V[node]] = float('inf')
        finish[V[node]] = float('inf')
        pred[V[node]] = None


    # empty list that will contain the sorted nodes
    tps = []

    # for every u in V,
    for x in range (0, len(V)):
        u = V[x]
        # if u.color == white; dfsVisit(u)
        if color[u] == 'w':
            dfsVisit(u, color, discovery, finish, pred, adjList, tps)

    # Used DFS to compute finish t's for each vertex
    # insert each vertex into the front of the linked list as it is finished
    # (insert it to the end of the list and then reverse it)
    tps.reverse()

    #print("check_TPS", check_TPS(adjList, tps))

    for i in range (0, len(tps)):
        tps[i] = str(tps[i])

    end_time = time.process_time()
    #write tps to a file
    write_tps_to_file(tps, filename)
    print("Ran in: {:.5f} secs".format(end_time - start_time))


time = 0

def dfsVisit(u, color, discovery, finish, pred, adjList, tps):
    #insert depth first search code here
    global time
    time = time + 1
    discovery[u] = time
    color[u] = 'g'

    #grab u's adjaceny list
    uAdj = adjList[u]
    for x in range (0, len(uAdj)):
        v = uAdj[x]
        if color[v] == 'w':
            pred[v] = u
            dfsVisit(v, color, discovery, finish, pred, adjList, tps)

    color[u] = 'b'
    time = time + 1
    finish[u] = time
    tps.append(u)
    return

if __name__ == '__main__':
    """ Write code here to run compute_tps for your testing purposes"""
    import sys
    filename = sys.argv[1]
    compute_tps(filename)

