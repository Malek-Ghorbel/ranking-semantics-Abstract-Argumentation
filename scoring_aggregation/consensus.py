def jaccard_distance(set1, set2):
    intersection = set1 & (set2)
    union = set1 | (set2)
    return 1 - len(intersection) / len(union)

def closest_ranking(rank , rankings) :
    distances = []
    for ranking in rankings :
        distances.append(jaccard_distance(rank , ranking))
    distances.index(min(distances))