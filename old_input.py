def readFromOldFormat(filename):
    nodes = []
    edges=[]
    with open('filename.txt', 'r') as file:
        for line in file:
                line = line.strip()
                if line.startswith('arg(') and line.endswith(')'):
                    node_name = line[4:-2]
                    nodes.add(node_name)

                elif line.startswith('att(') and line.endswith(')'):
                     edges.add(line[3:-1])


    return nodes,edges