import networkx as nx
from discussion_based import discussion_based
from tuple_based import tuple_based
G = nx.DiGraph()

with open('input.txt', 'r') as file:
    for line in file:
        if (line[0] == '#' ):
            continue
        elif ( line[0] == 'p'):
            content = line.split()
            nb_nodes = int(content[-1])
            nodes = [i+1 for i in range(nb_nodes)]
            G.add_nodes_from(nodes)
        else :
            content = line.split()
            G.add_edge(int(content[0]) , int(content[1]))

print(discussion_based(G,5))
print(tuple_based(G))