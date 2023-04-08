import sys

def has_cycle(G):
  nodes = list(G.nodes())
  n = G.number_of_nodes()
  p = [list(G.successors(i)) for i in G.nodes()]

  cycle = False
  vis = [False for _ in range(n)]
  for i in range(n) :
    while(p[i]):
      pp = []
      if (nodes[i] in p[i]) :
        cycle = True 
      for j in p[i] :
        if (vis[p[i].index(j)]) :
          continue 
        else :
          vis[p[i].index(j)] = True
          for l in list(G.successors(j)) :
            pp.append(l)
      p[i] = pp

  return cycle

def tuples_cmp(va , vb) :
  p =0
  i=1
  if (len(va[i]) == len(vb[i]) and len(va[p]) == len(vb[p])):
    if (va[p] <= vb[p] and va[i] >= vb[i]) :
      return True
    else :
      if (va[p] >= vb[p] and va[i] <= vb[i]):
        return False
  else:
    if (len(va[i]) >= len(vb[i]) and len(va[p]) >= len(vb[p]) ):
      return False
    else:
      if (len(va[i]) <= len(vb[i]) and len(va[p]) >= len(vb[p])) :
        return True

    
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if tuples_cmp( left_half[i][1] , right_half[j][1]):
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def tuple_based(G) :
  if has_cycle(G):
    print("graph has cycles can't provide a ranking")
  else:
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    m = [0 for _ in range(n)]
    p = [list(G.predecessors(i)) for i in G.nodes()]
    l = [[[],[]] for _ in range(n)]

    for i in range(n) :
      if not(p[i]) :
        l[i][0] = sys.maxsize

    m = [[] for _ in range(n)]

    index = 0
    while( (not (p == m)) ) :
      index = index +1  
      d = [[] for _ in range(n)]
      for i in range(n) :
        for j in p[i] :
          pred = list(G.predecessors(j))
          if (not (pred)) :
            #root element 
            if (index % 2 == 1 ) :
              l[i][1].append(index)
            else :
              l[i][0].append(index)
          for k in list(G.predecessors(j)) :
            d[i].append( k )
      p = d

    nodes_scores = list(zip(nodes ,  l ))

    first_ones = [x for x in nodes_scores if x[1][0] == sys.maxsize]
    others = [x for x in nodes_scores if x not in first_ones]
    
    merge_sort(others)
    first = [x[0] for x in first_ones]
    other = [x[0] for x in others]
    
    ranking = first + other
    return ranking