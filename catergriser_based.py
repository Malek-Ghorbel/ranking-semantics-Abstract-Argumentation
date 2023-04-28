def categoriser_based_ranking(G) :
    # Initialize
    categoriser_values = {}
    for node in G.nodes():
        categoriser_values[node] = 1

    # Compute categoriser values
    for node in G.nodes():
     if len(list(G.predecessors(node))) == 0:
        categoriser_values[node] = 1
     else:
        total_sum = sum(categoriser_values[pred] for pred in G.predecessors(node))
        categoriser_values[node] = 1 / (1 + total_sum)

    # Rank
    sorted_nodes = sorted(G.nodes(), key=lambda x: categoriser_values[x], reverse=True)
    return sorted_nodes



