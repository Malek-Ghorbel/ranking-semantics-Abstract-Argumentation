def plurality_aggregation(rankings):
    """
    Aggregates rankings using the Plurality scoring rule.
    Returns a list of items sorted by their score in descending order.
    """
    num_items = len(rankings[0])
    scores = [0] * num_items
    
    for ranking in rankings:
        scores[ranking[0]-1] += 1
    #print(scores)
    item_scores = [(i+1, scores[i]) for i in range(num_items)]
    item_scores_sorted = sorted(item_scores, key=lambda x: x[1], reverse=True)
    return [i for (i, score) in item_scores_sorted]

