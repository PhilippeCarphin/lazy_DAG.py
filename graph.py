import numpy as np
import itertools

# Doesn't have anything to do with lazy_dag but I'm saving it in this repo
# because I have no better place to put it.

class graph(object):
    def __init__(self, n_nodes):
        self.adj_mat = np.zeros((n_nodes,n_nodes))
    def add_edge(self,u,v,weight):
        self.adj_mat[u,v] = weight
        self.adj_mat[v,u] = weight


class grille(object):
    def __init__(self, graph, dims):
        self.graph = graph
        self.arr = np.full((graph.n_nodes, graph.n_nodes), -1)

def eval_solution(graph, linear_solution):
    value = 0
    length = len(linear_solution)
    for i in range(length):
        u = linear_solution[i]
        for j in range(i+1, length):
            v = linear_solution[j]
            value += graph.adj_mat[u,v] * (j-i)
    # print(value)
    return value

def switch(solution, i,j):
    s = list(solution)
    s[i] = solution[j]
    s[j] = solution[i]
    # print("switched {} and {}, solution is now{}".format(i,j,s))
    return s


if __name__ == "__main__":
    g = graph(5)
    a=0
    b=1
    c=2
    d=3
    e=4

    g.add_edge(a,b,3)
    g.add_edge(a,c,4)
    g.add_edge(a,d,2)
    g.add_edge(a,e,7)

    g.add_edge(b,c,4)
    g.add_edge(b,d,6)
    g.add_edge(b,e,3)

    g.add_edge(c,d,5)
    g.add_edge(c,e,8)

    g.add_edge(d,e,6)

    solution = [d,c,b,e,a]
    solution = [a,b,c,d,e]

    eval_solution(g,solution)
    best_value = 97
    best_solution = solution
    for i in range(5):
        for j in range(i+1,5):
            current_s = switch(solution, i, j)
            v =  eval_solution(g,switch(solution, i, j))
            if v < best_value:
                best_solution = current_s
                best_value = v
    print("RETAINING BEST SOLUTION {} with value {}".format(best_solution,
        best_value))

    solution = best_solution
    for i in range(5):
        for j in range(i+1,5):
            current_s = switch(solution, i, j)
            v =  eval_solution(g,switch(solution, i, j))
            if v < best_value:
                best_solution = current_s
                best_value = v

    print("RETAINING BEST SOLUTION {} with value {}".format(best_solution,
        best_value))

    for s in itertools.permutations([a,b,c,d,e]):
        current_s = switch(solution, i, j)
        v =  eval_solution(g,switch(solution, i, j))
        if v < best_value:
            best_solution = current_s
            best_value = v

    print("RETAINING BEST SOLUTION {} with value {}".format(best_solution,
        best_value))
