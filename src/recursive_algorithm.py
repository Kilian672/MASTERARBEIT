import numpy as np 
import random
import time
import copy

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

# Third Algorithm
class FAIRCLUSTERING: 

    def __init__(self): 
        self.lookup = {}

    def isFeasible(self, g, r, alpha, beta): 

        if g < 0 or r < 0: 
            return False
        if g+r == 0: 
            return False
    
        constr1 = alpha[0] <= g/(g+r)
        constr2 = beta[0] >= g/(g+r)
        constr3 = alpha[1] <= r/(g+r)
        constr4 = beta[1] >= r/(g+r)

        return constr1 and constr2 and constr3 and constr4 

    def getRadius(self, V, g_sub, r_sub, g_new, r_new):
    
        used_nodes = []
        for v in enumerate(V): 
            if g_sub == 0 and r_sub == 0: 
                break
            else: 
                if v[1] == 'g' and g_sub > 0: 
                    used_nodes.append(v)
                    g_sub = g_sub-1
                if v[1] == 'r' and r_sub > 0: 
                    used_nodes.append(v)
                    r_sub = r_sub-1
        
        erg = []
        for v in V:  
            
            if g_new == 0 and r_new == 0: 
                break
            elif v in used_nodes: 
                continue
            else: 
                if v[1] == 'g' and g_new > 0: 
                    erg.append(v)
                    g_new = g_new-1
                if v[1] == 'r' and r_new > 0: 
                    erg.append(v)
                    r_new = r_new-1
                
      
        return (erg[len(erg)-1][0]-erg[0][0])/2

    def getRadiusOfSubprob(self, V, subproblem): 

        k = len(subproblem)
        used_nodes = []
        phi = {i: [] for i in range(1,k+1)}
        for i, comb in enumerate(subproblem): 
            g, r = comb[0], comb[1]
    
            for j in range(len(V)-1, -1, -1): 
                if r == 0 and g == 0: 
                    break 
                if V[j] in used_nodes: 
                    continue
                if V[j][1] == 'g' and g > 0: 
                    g = g-1
                    phi[k-i].append(V[j])
                    used_nodes.append(V[j])
                if V[j][1] == 'r' and r > 0: 
                    r = r-1
                    phi[k-i].append(V[j])
                    used_nodes.append(V[j])

        rad = 0 
        for value in phi.values(): 
            minValue = min([v[0] for v in value])
            maxValue = max([v[0] for v in value])
            rad = max(rad, (maxValue-minValue)/2)

        return (rad, phi)
    
    def getRadiusOfSubproblem(self,i,j, V): 

        if len(V) == 0: 
            return (float("inf"), [])

        Cont = []
        minVal = 0
        maxVal = V[len(V)-1][0]
        while len(V) > 0: 
            l = len(V)-1
            if i == 0 and j == 0: 
                break 
            if V[l][1] == "g":
                if i > 0:
                    minVal = V[l][0]
                    V.pop()
                    i = i-1
                else:   
                    Cont.append(V[l])
                    V.pop()
            else:  
                if j > 0: 
                    minVal = V[l][0]
                    V.pop()
                    j = j-1
                else: 
                    Cont.append(V[l])
                    V.pop()
                
        return ((maxVal-minVal)/2, V+Cont)

    def fairClustering3(self, V, G, R, alpha, beta, k): 
        
        if (G,R,k) in self.lookup.keys(): 
            return self.lookup[(G,R,k)]

        if k==1:
            if self.isFeasible(G,R,alpha,beta): 
                r, phi = self.getRadiusOfSubprob(V, [(G,R)])
                return [(G,R)], phi
            else: 
                return ([], {})

        feasCombs = []
        for g in range(G): 
            for r in range(R): 
                if self.isFeasible(g,r,alpha,beta): 
                    feasCombs.append((g,r))
        
        if feasCombs == []: 
            return ([], {})

        best_rad, best_phi, best_sub = float("inf"), {}, []
        for comb in feasCombs: 
            tup = (G-comb[0], R-comb[1], k-1)
            subproblem = self.fairClustering3(V, G-comb[0], R-comb[1], alpha, beta, k-1)[0]
            if tup not in self.lookup.keys(): 
                self.lookup[tup] = subproblem
            
            if subproblem != ([], {}): 
                subproblem.append(comb)
                rad, phi = self.getRadiusOfSubprob(V, subproblem)
                if rad < best_rad: 
                    best_rad = rad
                    best_phi = phi
                    best_sub = subproblem 
            
        
        return best_sub, best_phi

    def fairClustering4(self, V, alpha, beta, K): 

        G = len([v for v in V if v[1] == 'g'])
        R = len([v for v in V if v[1] == 'r'])

        dp = {i: {} for i in range(1,K+1)}
        for k in range(1, K+1):
            for g in range(1,G+1): 
                    for r in range(1,R+1):  
                        if k == 1: 
                            if self.isFeasible(g,r,alpha,beta): 
                                opt_rad, opt_phi = self.getRadiusOfSubprob(V, [(g,r)])
                                dp[k][(g,r)] = (opt_rad, [(g,r)], opt_phi)
                        else: 
                            opt_rad, opt_sub, opt_phi= float("inf"), [], {}
                            for i in range(g): 
                                for j in range(r):
                                    if self.isFeasible(i, j, alpha, beta) and (g-i, r-j) in dp[k-1].keys(): 
                                        current_sub = dp[k-1][(g-i,r-j)][1]+[(i,j)]
                                        current_rad, current_phi = self.getRadiusOfSubprob(V, current_sub)
                                        if current_rad < opt_rad: 
                                            opt_rad = current_rad
                                            opt_sub = current_sub
                                            opt_phi = current_phi

                            dp[k][(g,r)] = (opt_rad, opt_sub, opt_phi)


        return dp[K][(G,R)][2]

    

            
        
def generatePath(n): 

    G = n/2
    R = n/2
    path = []
    for i in range(1,n+1):
        X = random.randint(1,2)
        if X == 1 and G > 0: 
            path.append((i,'g'))
            G = G-1
        elif X == 1 and G==0:
            path.append((i,'r'))
            R = R-1
        elif X == 2 and R > 0: 
            path.append((i,'r'))
            R = R-1
        else: 
            path.append((i,'g'))
            G = G-1 

    return path
                    




if __name__ == "__main__": 

    V = generatePath(20)
    #V = [(1,'g'), (2,'g'), (3,'g'), (4,'g'), (5,'g'), (6,'r'), (7,'r'), (8,'r'), (9,'r'), (10,'r')]
    alpha = (1/4, 1/4)
    beta = (3/4, 3/4)
    k = 5
    print(fairClustering(V, alpha, beta, k))
    #G = len([v for v in V if v[1] == 'g'])
    #R = len([v for v in V if v[1] == 'r'])
    fairClust = FAIRCLUSTERING()
    #print(fairClust.getRadius(V,4,3,2,2))
    
    start_time = time.perf_counter()
    #print(fairClust.fairClustering3(V,G,R,alpha, beta, k))
    print(fairClust.fairClustering4(V, alpha, beta, k))
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")

    
    
    
    
