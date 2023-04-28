def biased_scoring_aggregation(ranking_list, weights):
    n_items = len(ranking_list[0])
    n_rankings = len(ranking_list)
    scores = [0] * n_items

    for item_idx in range(n_items):
        for ranking_idx in range(n_rankings):
            weight_idx = ranking_list[ranking_idx][item_idx] - 1
            scores[item_idx] += weights[weight_idx]

    sorted_items = [x+1 for _, x in sorted(zip(scores, range(n_items)), reverse=True)]

    return sorted_items
