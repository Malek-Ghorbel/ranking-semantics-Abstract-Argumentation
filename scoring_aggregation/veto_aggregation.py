def veto_aggregation(ranking_list):
    n_items = len(ranking_list[0])
    n_rankings = len(ranking_list)
    scores = [0] * n_items

    for item_idx in range(n_items):
        for ranking_idx in range(n_rankings):
            if ranking_list[ranking_idx][item_idx] == n_items+1:
                scores[item_idx] += 1
                break
    
    print(scores)
    sorted_items = [x+1 for _, x in sorted(zip(scores, range(n_items)), reverse=False)]

    return sorted_items



import numpy as np

def median_ranking(rankings):
    # Compute the median rank of each item across all expert rankings
    median_ranks = np.median(rankings, axis=0)
    
    # Rank the items based on their median rank
    ranked_items = np.sort(median_ranks)
    return ranked_items

import numpy as np
from scipy.optimize import minimize

def minimax_method(rankis) :
    rankings = np.array(rankis)
    veto_threshold = 1
    n_experts, n_items = rankings.shape
    
    # Count the number of vetoes for each item
    veto_counts = np.zeros(n_items)
    for i in range(n_items):
        veto_counts[i] = np.sum(rankings[:, i] == -1)
        
    # Identify the items that have been vetoed by more than the threshold number of experts
    vetoed_items = np.where(veto_counts > veto_threshold)[0]
    
    # Remove the vetoed items from consideration
    rankings[:, vetoed_items] = -1
    
    # Compute the scores for each item based on its rank in each expert's ranking
    scores = np.zeros(n_items)
    for i in range(n_items):
        scores[i] = np.sum(rankings[:, i] != -1) * np.mean(rankings[:, i][rankings[:, i] != -1])
    
    # Rank the items based on their scores
    ranked_items = np.argsort(-scores)
    
    return [x+1 for x in ranked_items]



def calculate_kendall_distance(rank1, rank2):
    # Calculate the Kendall distance between two rankings
    pairwise_disagreements = 0
    n = len(rank1)
    
    for i in range(n):
        for j in range(i+1, n):
            if (rank1[i] < rank1[j] and rank2[i] > rank2[j]) or (rank1[i] > rank1[j] and rank2[i] < rank2[j]):
                pairwise_disagreements += 1
    
    kendall_distance = pairwise_disagreements / (n * (n-1) / 2)
    return kendall_distance


def aggregate_rankings(rankings):
    n = len(rankings[0])
    num_rankings = len(rankings)
    dissimilarity_matrix = np.zeros((num_rankings, num_rankings))

    # Calculate pairwise Kendall distances
    for i in range(num_rankings):
        for j in range(i+1, num_rankings):
            kendall_distance = calculate_kendall_distance(rankings[i], rankings[j])
            dissimilarity_matrix[i][j] = kendall_distance
            dissimilarity_matrix[j][i] = kendall_distance
    
    # Perform Borda count aggregation
    aggregated_ranking = np.zeros(n)
    for i in range(n):
        for j in range(num_rankings):
            aggregated_ranking[i] += np.sum(np.argsort(dissimilarity_matrix[j])[::-1] == i)
    
    return aggregated_ranking.argsort()[::-1] + 1  # Return the aggregated ranking in ascending order

