def veto_aggregation(ranking_list):
    n_items = len(ranking_list[0])
    n_rankings = len(ranking_list)
    scores = [0] * n_items

    for item_idx in range(n_items):
        for ranking_idx in range(n_rankings):
            if ranking_list[ranking_idx][item_idx] == n_items+1:
                scores[item_idx] += 1
                break

    sorted_items = [x+1 for _, x in sorted(zip(scores, range(n_items)), reverse=False)]

    return sorted_items
