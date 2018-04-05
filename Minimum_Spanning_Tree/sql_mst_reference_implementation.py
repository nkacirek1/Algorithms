import sqlite3


def read_edge_file(filename):
    conn = sqlite3.connect(filename + '.db')
    conn.execute('DROP TABLE IF EXISTS edges')
    conn.execute('CREATE TABLE edges (source, dest, weight)')
    with open(filename) as f:
        for line in f:
            v1, v2, w = line.split()
            conn.execute('INSERT INTO edges VALUES (?, ?, ?)', (v1, v2, int(w)))
            conn.execute('INSERT INTO edges VALUES (?, ?, ?)', (v2, v1, int(w)))
    conn.commit()
    return conn


def setup_tree(conn):
    conn.execute('DROP TABLE IF EXISTS tree')
    conn.execute('CREATE TABLE tree (node)')
    root = conn.execute('SELECT source FROM edges LIMIT 1').fetchone()[0]
    conn.execute('INSERT INTO tree VALUES (?)', (root,))
    conn.execute('DROP TABLE IF EXISTS tree_edges')
    conn.execute('CREATE TABLE tree_edges (parent, child, weight)')


def next_tree_edge(conn):
    return conn.execute(
    '''
    SELECT source, dest, weight FROM edges
      WHERE edges.source IN
        (SELECT tree.node FROM tree)
      AND edges.dest NOT IN 
        (SELECT tree.node FROM tree)
    ORDER BY edges.weight
    LIMIT 1
    '''
    ).fetchone()


def write_tree_edges(conn, filename):
    with open(filename, mode='w') as f:
        for v1, v2, w in conn.execute('SELECT parent, child, weight FROM tree_edges'):
            f.write("{} {} {}\n".format(v1, v2, w))


def compute_mst(filename):
    conn = read_edge_file(filename)
    setup_tree(conn)
    node_count = conn.execute('SELECT COUNT(DISTINCT source) FROM edges').fetchone()[0]
    for i in range(node_count - 1):
        source, dest, weight = next_tree_edge(conn)
        conn.execute('INSERT INTO tree VALUES (?)', (dest,))
        conn.execute('INSERT INTO tree_edges VALUES (?, ?, ?)', (source, dest, weight))
    conn.commit()
    write_tree_edges(conn, filename + '.sql.mst')
    conn.close()

if __name__ == '__main__':
    import sys
    # compute_mst(sys.argv[1])
    compute_mst(sys.argv[1])