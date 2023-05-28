def same_position_ratio(list1, list2):
    count = 0
    for i in range(len(list1)):
        if i < len(list2) and list1[i] == list2[i]:
            count += 1
    return (1 - count / len(list1))

def kendall_tau_distance(rank1, rank2):
    # Get the number of pairwise disagreements
    disagreements = 0
    for i in range(len(rank1)):
        for j in range(i + 1, len(rank1)):
            # Check for disagreements in the ordering
            if (rank1[i] < rank1[j] and rank2[i] > rank2[j]) or \
               (rank1[i] > rank1[j] and rank2[i] < rank2[j]):
                disagreements += 1

    # Calculate the Kendall Tau distance
    tau = disagreements / (len(rank1) * (len(rank1) - 1) / 2)
    return tau

def closest_ranking(rank , rankings) :
    distances = []
    for ranking in rankings :
        distances.append(same_position_ratio(rank , ranking))
    return distances

def kendall_closest_ranking(rank , rankings) :
    distances = []
    for ranking in rankings :
        distances.append(kendall_tau_distance(rank , ranking))
    return distances


