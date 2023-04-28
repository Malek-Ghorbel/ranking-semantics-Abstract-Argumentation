# Calculate the strengths of each argument
import networkx as nx

def calculate_strengths(G):
  strengths = {}
  for node in G.nodes():
    strengths[node] = 1 - max([max([G.edges[x, y].get('weight', nx.pagerank(G)[node]), nx.pagerank(G)[y]]) for x, y in G.in_edges(node)] + [0])
  return strengths



# Assign ranks to each argument based on strength and value of zero-sum game
def zero_sum(G):
  s = calculate_strengths(G)
  values = {}
  for x in G.nodes():
      value = 0
      for y in G.nodes():
          if (x, y) in G.edges:
              value += s[y]
          elif (y, x) in G.edges:
              value -= s[y]
      values[x] = value
  return values



# Define the Matt and Toni ranking 

def mt_ranking(G, values):
    ranking = sorted(G.nodes(), key=lambda x: values[x], reverse=True)
    return {arg: rank for rank, arg in enumerate(ranking)}


# values = zero_sum(G)
# mt = mt_ranking(G, values)

# for arg, rank in mt.items():
#     print(f"{arg} -> {rank}")