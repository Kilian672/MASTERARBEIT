# First Algorithm
def isFeasible(g, r, alpha, beta): 

    if g+r == 0: 
        return False

    constr1 = alpha[0] <= g/(g+r)
    constr2 = beta[0] >= g/(g+r)
    constr3 = alpha[1] <= r/(g+r)
    constr4 = beta[1] >= r/(g+r)

    return constr1 and constr2 and constr3 and constr4 

def getBestSubsets(V, feasCombs): 
    B = []
    for c in feasCombs: 
        g = c[0]
        r = c[1]
        S_c = []
        minValue = float("inf")
        maxValue = 0
        for v in V: 
            if v[1] == 'g' and g > 0: 
                S_c.append(v)
                g = g-1
                if v[0] < minValue: 
                    minValue = v[0]
                if v[0] > maxValue: 
                    maxValue = v[0]
            if v[1] == 'r' and r > 0: 
                S_c.append(v)
                r = r-1
                if v[0] < minValue: 
                    minValue = v[0]
                if v[0] > maxValue: 
                    maxValue = v[0]
        
        r_c = (maxValue-minValue)/2
        B.append((r_c, S_c))

    return B

def setDiff(list1, list2): 
    diff = []
    for x in list1: 
        if x in list2: 
            continue
        diff.append(x)
    return diff

def fairClustering(V, alpha, beta, k): 

    # Get number of green and red nodes in list
    G = len([v for v in V if v[1] == 'g'])
    R = len([v for v in V if v[1] == 'r'])
    
    # Base case
    if k==1: 
        if isFeasible(G,R, alpha, beta):
            indices = [v[0] for v in V]
            maxValue = max(indices)
            minValue = min(indices) 
            return ((maxValue-minValue)/2, {1: V})
        else: 
            return (float("inf"), {})
    
    # Get feasible combinations
    feasCombs = []
    for g in range(1, G+1): 
        for r in range(1, R+1): 
            if isFeasible(g, r, alpha, beta): 
                feasCombs.append((g,r))
    
    if feasCombs == []: 
        return (float("inf"), {})
    
    B = getBestSubsets(V, feasCombs)
    r_opt = float("inf")
    phi_opt = {}
    for b in B: 
        diff = setDiff(V, b[1])
        r, phi = fairClustering(diff, alpha, beta, k-1)
        r = max(b[0], r)
        if r < r_opt: 
            phi_opt = {}
            r_opt = r
            phi_opt = phi
            phi_opt[k] = b[1]


    return (r_opt, phi_opt)  

# Second Algorithm
def getFeasibleCombinations(G, R, alpha, beta, k): 
    
    if k==1: 
        if isFeasible(G,R,alpha,beta): 
            return [[(G,R)]] 
        else: 
            return []

    feasCombs = []
    for g in range(G): 
        for r in range(R): 
            if isFeasible(g,r,alpha,beta): 
                feasCombs.append((g,r))

    tree = []
    for comb in feasCombs: 
        subproblem = getFeasibleCombinations(G-comb[0], R-comb[1], alpha, beta, k-1)
        if subproblem != []: 
            for i in range(len(subproblem)): 
                path = subproblem[i]
                path.append(comb)
                tree.append(path)

    return tree

def getAssgnFromComb(V, comb): 

    k = len(comb)
    i = 0
    g, r = comb[i][0], comb[i][1]
    phi_c = {i: [] for i in range(1,k+1)}
    container = []
    while len(V) > 0 or len(container) > 0: 
        if g == 0 and r == 0: 
            i = i+1
            g, r = comb[i][0], comb[i][1]
            V = container + V
            container = []
        else: 
            # V = [(1,'g'), (2,'g'), ..., (n,'r')]
            col = V[0][1]
            if col == 'g' and g > 0: 
                phi_c[i+1].append(V[0])
                g = g-1
            elif col == 'r' and r > 0: 
                phi_c[i+1].append(V[0])
                r = r-1
            else: 
                container.append(V[0])
            
            V = V[1:]

    r_c = 0 
    for key, values in phi_c.items(): 
        minValue = min([v[0] for v in values])
        maxValue = max([v[0] for v in values])
        r_c = max(r_c, (maxValue-minValue)/2)

    return (r_c, phi_c)

def fairClustering2(V, alpha, beta, k): 

    G = len([v for v in V if v[1] == 'g'])
    R = len([v for v in V if v[1] == 'r'])
    combinations = getFeasibleCombinations(G, R, alpha, beta, k)
    
    best_radius = float("inf")
    best_assgn = {}
    for comb in combinations: 
        current_radius, current_assgn = getAssgnFromComb(V, comb)
        if current_radius < best_radius: 
            min_radius = current_radius
            best_assgn = current_assgn

    return (min_radius, best_assgn)