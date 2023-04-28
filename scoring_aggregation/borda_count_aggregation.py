def borda_count_aggregation(rankings):
    """
    Aggregates rankings using the Borda Count scoring rule.
    """
    items = set()
    for ranking in rankings:
        items.update(ranking)
    num_items = len(items)
    scores = [0] * num_items
    for ranking in rankings:
        if isinstance(ranking, list):
            for i, item in enumerate(ranking):
                scores[list(items).index(item)] += num_items - i + 1
    return [x for _, x in sorted(zip(scores, list(items)), reverse=True)]
