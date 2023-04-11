
import math

def l_norm(vec1, vec2):
  value = 0
  for i in range(len(vec1)):
    value += (vec1[i] - vec2[i])**2
  
  return math.sqrt(value)

def burden(num_nodes, attaquants, alpha, epsilon):
  burden_values = [1]*num_nodes
  burden_values_next = [0]*num_nodes
  
  while True:
    for i in range(num_nodes):
      value = 0
      for j in attaquants[i]:
        value += 1/burden_values[j]**alpha
      burden_values_next[i] = 1 + value**(1/alpha)
    
    if l_norm(burden_values_next , burden_values) < epsilon:
      break
    
    burden_values = burden_values_next[:]
  
  return burden_values_next


def alpha_burden_based(G, alpha) :
  #Initialization:
    node_to_index = {node: index for index, node in enumerate(G.nodes())}
    predecessors = {node_to_index[node]: [node_to_index[pred] for pred in G.predecessors(node)] for node in G.nodes()}
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())
    
    s_alpha_tab = [0] * num_nodes

    #Create the steps tab
    #for j in range(num_nodes):
      #s_alpha_tab[j] = s_alpha(j, alpha, predecessors, s_alpha_tab)
    
    s_alpha_tab = burden(num_nodes, predecessors, alpha, epsilon=0.00001)

    #print(s_alpha_tab)

    #Rank
    nodes_sa = list(zip(nodes ,  s_alpha_tab))
    sorted_nodes = [x[0] for x in sorted(nodes_sa, key=lambda x: x[1:])]
    return sorted_nodes