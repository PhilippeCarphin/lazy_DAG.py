#!/usr/bin/python
# Inspired by https://github.com/thieman/py-dag
from collections import OrderedDict
from collections import deque
import numpy as np


class lazy_DAG(object):
    def __init__(self, filename=None, ordered_dict=None, lazy_dag=None):
        # Attributes
        self.n_nodes = 0
        self.n_edges = 0
        self.adj_dict = OrderedDict()
        self.active = None
        self.active_nodes = 0

        # Initialization from filename
        if filename != None:
            file = open(filename, "r")

            first_line = file.readline().split()
            self.n_nodes = int(first_line[0])
            self.n_edges = int(first_line[1])

            # 2) Add all the nodes
            self.adj_dict = OrderedDict()
            for node in range(self.n_nodes):
                self.adj_dict[node] = set()

            # 3) Add all the edges
            for i in range(self.n_edges):
                edge = file.readline().split()
                self.adj_dict[int(edge[0])].add(int(edge[1]))

        # Initialization from other ordered dictionnary
        elif ordered_dict != None:
            self.adj_dict = OrderedDict(ordered_dict)
            self.n_nodes = 0
            self.n_edges = 0
            for node in ordered_dict:
                self.n_nodes += 1
                self.n_edges += len(ordered_dict[node])
        elif lazy_dag != None:
            self.n_nodes = lazy_dag.n_nodes
            self.n_edges = lazy_dag.n_edges
            self.adj_dict = OrderedDict(lazy_dag.adj_dict)
        else:
            raise exception

        self.active = np.ones((self.n_nodes)) # Cree un numpy array
        self.active_nodes = self.n_nodes

    def _is_active(self, node):
        """ Returns True if a node is active """
        return self.active[node]

    def empty(self):
        """ Returns true if the graph is empty in the sense that it either has
        no nodes or has had all of it's nodes removed """
        return self.active_nodes == 0

    def reset(self):
        """ Resets all the nodes to active """
        self.active.fill(True)
        self.active_nodes = self.n_nodes

    def remove_node(self, node):
        """ Lazy removes a node from the graph """
        if not self.active[node]:
            return
        else:
            self.active[node] = False
            self.active_nodes -= 1

    def remove_list(self, l):
        """ Lazy removes a list of nodes from the graph """
        for node in l:
            self.remove_node(node)

    def add_node(self, node):
        """ Lazy adds a node to the graph.  This only works for nodes that were
        added to the internal graph during creation.  That is you can only add a
        node that was lazy removed """
        if self.active[node]:
            return
        else:
            self.active[node] = True
            self.active_nodes += 1

    def add_edge(self, u,v):
        """ Adds an edge u -> v to the graph """
        if v not in self.adj_dict[u]:
            self.n_edges += 1
            self.adj_dict[u].add(v)

    def has_edge(self, u, v):
        """ Checks if the graph has an edge u -> v, this function must be called
        with nodes that have not been removed """
        assert (self._is_active(u) and self._is_active(v)), "has_edge cannot be called on nodes that have been removed"
        assert u < self.n_nodes and v < self.n_nodes
        return v in self.adj_dict[u]

    def nodes(self):
        """ Returns a list of active nodes in the graph """
        return [v for v in range(self.n_nodes) if self._is_active(v)]

    def successors(self, u):
        """ Returns the list of successors of the node u in the graph.  This
        function must be called with a node that has not been removed """
        assert self._is_active(u), "successors cannot be called on a node that has been removed"
        return [v for v in self.adj_dict[u] if self._is_active(v)]

    def predecessors(self, v):
        """ Returns the list of predecessors of v.  This function must be called
        with a node that has not been removed."""
        assert self._is_active(v), "predecessors cannot be called on a node that has been removed"
        return [u for u in self.nodes() if self.has_edge(u,v)]

    def in_degree(self, v):
        """ Returns the in_degree of a node: the number of edges coming into the
        node = the number of predecessors """
        assert self._is_active(v), "in_degree cannot be called with a node that has been removed"
        return len(self.predecessors(v))

    def in_degree_0(self):
        """ Returns a list of nodes that do not have any predecessors """
        return [v for v in self.nodes() if self.in_degree(v) == 0]

    def transitive_close(self):
        """ Transitively closes a graph """
        for u in self.adj_dict:
            nodes_seen = []
            node_queue = deque(self.adj_dict[u])
            while len(node_queue) != 0:
                v = node_queue.popleft()
                nodes_seen.append(v)
                self.add_edge(u,v)
                node_queue += [v for v in self.adj_dict[v] if v not in nodes_seen]

    def transitive_closure(self):
        new_graph = lazy_DAG(lazy_dag=self)
        new_graph.transitive_close()
        return new_graph

if __name__ == "__main__":
    ld = lazy_DAG("./tp2-donnees/poset10-4a")
    ld2 = lazy_DAG(ordered_dict=ld.adj_dict)
    print(ld.adj_dict)
    print("in_degree_0():")
    print(ld.in_degree_0())
    ld.remove_node(9)
    print("in_degree_0(): after removing 9")
    print(ld.in_degree_0())
    ld.add_node(9)
    ld_close = ld.transitive_closure()
    print(ld_close.adj_dict)


