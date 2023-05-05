def kemeny_aggregation(rankings):
    """
    Computes the Kemeny-Young aggregation of a set of ranking lists.
    
    Parameters:
        rankings (list of lists): A list of ranking lists, where each list contains the items ranked in order.
        
    Returns:
        list: The Kemeny-Young aggregation, i.e., the ranking that minimizes the total number of pairwise swaps.
    """
    n = len(rankings[0])  # Number of items
    m = len(rankings)  # Number of rankings
    
    # Construct pairwise preference matrix
    P = [[0]*n for i in range(n)]
    for r in rankings:
        for i in range(n):
            for j in range(i+1, n):
                P[r[i]-1][r[j]-1] += 1
    
    # Initialize arbitrary ranking
    R = list(range(1, n+1))
    cost = kemeny_distance(R, P)
    
    # Iterate until Kemeny optimal aggregation is found
    while True:
        swap_found = False
        for i in range(n):
            for j in range(i+1, n):
                # Check if swapping (i,j) reduces the cost
                R_new = R.copy()
                R_new[i], R_new[j] = R_new[j], R_new[i]
                cost_new = kemeny_distance(R_new, P)
                if cost_new < cost:
                    R = R_new
                    cost = cost_new
                    swap_found = True
        if not swap_found:
            break
    
    return R
    
def kemeny_distance(ranking, P):
    """
    Computes the Kemeny distance between a ranking and a pairwise preference matrix.
    
    Parameters:
        ranking (list): A ranking, i.e., a list of items in order.
        P (list of lists): A pairwise preference matrix, where P[i][j] is the number of times item i is preferred over item j.
        
    Returns:
        int: The Kemeny distance between the ranking and P.
    """
    n = len(ranking)
    cost = 0
    for i in range(n):
        for j in range(i+1, n):
            d = (ranking.index(i+1) - ranking.index(j+1)) * ((P[i][j] > P[j][i]) - (P[j][i] > P[i][j]))
            cost += abs(d)
    return cost

from itertools import permutations

from itertools import permutations

def kemeny_young(rankings):
    n = len(rankings[0])
    pairwise = [[0]*n for _ in range(n)]
    for ranking in rankings:
        for i, j in permutations(range(n), 2):
            pairwise[ranking[i]][ranking[j]] += 1
    
    min_kendall_tau = float('inf')
    min_permutation = None
    for permutation in permutations(range(n)):
        kendall_tau = 0
        for i, j in permutations(range(n), 2):
            kendall_tau += pairwise[i][j] * (1 if permutation.index(i) < permutation.index(j) else -1)
        if kendall_tau < min_kendall_tau:
            min_kendall_tau = kendall_tau
            min_permutation = permutation
    
    return [x for x in min_permutation]



input_rankings = [[1, 6, 10, 3, 2, 4, 8, 5, 7, 9], [1, 6, 10, 3, 2, 4, 8, 5, 7, 9], [1, 6, 10, 5, 7, 3, 2, 4, 8, 9]]
kemeny_aggregation = kemeny_young(input_rankings)
print(kemeny_aggregation)


