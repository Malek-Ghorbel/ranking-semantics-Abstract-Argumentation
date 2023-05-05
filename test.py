import networkx as nx

from discussion_based import discussion_based
from tuple_based import tuple_based
from Burden_based_semantic import burden_based
from Alpha_Burden_based_semantic import alpha_burden_based

from scoring_aggregation.borda_count_aggregation import borda_count_aggregation
from scoring_aggregation.plurality_aggregation import plurality_aggregation
from scoring_aggregation.biased_scoring_aggregation import biased_scoring_aggregation
from scoring_aggregation.veto_aggregation import veto_aggregation
from scoring_aggregation.top_k_aggregation import topk_aggregation

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


discussion_based = discussion_based(G,5)
tuple_based = tuple_based(G)
burden_based = burden_based(G,10)
alpha_burden_based = alpha_burden_based(G, 1)
rankings = [discussion_based, burden_based, alpha_burden_based]

# print("Discussion based: ",discussion_based)
# print("Tuple based: ",tuple_based)
# print("Burden based: ",burden_based)
# print("Alpha burden based: ",alpha_burden_based)

# aggregated_ranking = borda_count_aggregation(rankings)
# print("borda count aggregation: ", aggregated_ranking)

# aggregated_ranking1 = plurality_aggregation(rankings)
# print("plurality aggregation: ", aggregated_ranking1)

# aggregated_ranking3 = veto_aggregation(rankings)
# print("veto aggregation: ", aggregated_ranking3)

# aggregated_ranking4 = topk_aggregation(rankings, 3)
# print("top-k aggregation: ", aggregated_ranking4)

# weights = [5, 4, 3, 2, 1]
# aggregated_ranking2 = biased_scoring_aggregation(rankings, weights)
# print("biased scoring aggregation: ", aggregated_ranking2)

def readFromOldFormat(filename):
    p= True
    counter = 0
    with open('oldformat.apx', 'r') as file , open("newformat.txt" , 'w') as destination:
        for line in file:
                line = line.strip()
                if line.startswith('arg(') and line.endswith(').'):
                    counter += 1

                elif line.startswith('att(') and line.endswith(').'):
                    if (p) :
                        destination.write("p af " + str(counter) + '\n')
                        destination.write("# comment \n")
                        p =False
                    content = line[5:-2].split(',')
                    arg1_value = content[0].strip()
                    destination.write(arg1_value + ' ')
                    arg2_value = content[1].strip()
                    arg2_value = arg2_value[1:]
                    destination.write(arg2_value + '\n')

readFromOldFormat("a")