from random import randint, shuffle, sample


def read_lines(filename):
    with open(filename) as f:
        return f.readlines()


def parse_line(line):
    return [int(x) for x in line.split()]


def read_numbers_by_row(filename):
    lines = read_lines(filename)
    return [parse_line(line) for line in lines]


def read_graph(filename):
    """ Reads a graph written in a file to a dictionary in which
    each key is a node and the associated value is a list of nodes to which
    it has an outgoing edge. """
    data = read_numbers_by_row(filename)
    graph = {}
    for row in data:
        if row[0] not in graph:
            graph[row[0]] = [row[1]]
        else:
            graph[row[0]].append(row[1])
        if row[1] not in graph:
            graph[row[1]] = []
    return graph


def compute_in_degrees(digraph):
    """ Gets a directed graph as input and returns a dictionary
    in which each key is a node and the value for that is the number
    of incoming edges. """
    in_degree = {node: 0 for node in digraph.keys()}
    for node, neighbors in digraph.items():
        for n in neighbors:
            in_degree[n] += 1
    return in_degree


def read_double_graph(filename):
    """ Read a graph from input file and generates 2 dictionaries. The dictionaries
    are like those produced by the read_graph function.
    One for outgoing edges and one for incoming edges."""
    data = read_numbers_by_row(filename)
    out_graph = {}
    in_graph = {}
    for row in data:
        if row[0] not in out_graph:
            out_graph[row[0]] = [row[1]]
        else:
            out_graph[row[0]].append(row[1])
        if row[1] not in out_graph:
            out_graph[row[1]] = []

        if row[1] not in in_graph:
            in_graph[row[1]] = [row[0]]
        else:
            in_graph[row[1]].append(row[0])
        if row[0] not in in_graph:
            in_graph[row[0]] = []
    return out_graph, in_graph


def del_node(out_graph, in_graph, node):
    """ Removes a node and its connected edges from out_graph (not in_graph). """
    out_graph.pop(node)
    for neighbor in in_graph[node]:
        out_graph[neighbor].remove(node)


def random_permutation(nodes):
    nodes = list(nodes)
    nodes_shuffled = list(nodes)
    shuffle(nodes_shuffled)
    return {k: v for k,v in zip(nodes, nodes_shuffled)}


def generate_random_DAG(num_nodes):
    """ Gets a number and generates a random Directed Acyclic Graph.
    The output is the list of edges of the graph. """
    edges = []
    for i in reversed(range(num_nodes)):
        neighbors = sample(range(i), k=(randint(0, i)))
        for j in sorted(neighbors):
            edges.append((i, j))
    # At this point we have a random dag. But the topological sort
    # is obvious, it's just the order we constructed the graph in.
    # So we randomize the identity of the nodes.
    p = random_permutation(range(num_nodes))
    permuted = [[p[x] for x in row] for row in edges]
    shuffle(permuted)
    return permuted


def gen_and_write_DAG(num_nodes, filename):
    """ Gets a number as input, generates a DAG of that size,
    and writes the result into a file. Each edge in a separate line:
    sourcenode destnode."""
    with open('DAG_' + str(num_nodes) + '_' + filename + '.txt', 'w') as file:
        edges = generate_random_DAG(num_nodes)
        for edge in edges:
            file.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')


if __name__ == '__main__':
    gen_and_write_DAG(5, "5test")
    #gen_and_write_DAG(50, "50test")
    #gen_and_write_DAG(100, "100test")
    #gen_and_write_DAG(200, "200test")
    #gen_and_write_DAG(500, "500test")
    #gen_and_write_DAG(1000, "1000test")
    #gen_and_write_DAG(2500, "2500test")
    #gen_and_write_DAG(5000, "5000test")

