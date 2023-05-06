def same_position_ratio(list1, list2):
    count = 0
    for i in range(len(list1)):
        if i < len(list2) and list1[i] == list2[i]:
            count += 1
    return count / len(list1)


def closest_ranking(rank , rankings) :
    print(rank)
    print(rankings)
    distances = []
    for ranking in rankings :
        distances.append(same_position_ratio(rank , ranking))
    print(distances)
    print(max(distances))
    return distances.index(max(distances))


