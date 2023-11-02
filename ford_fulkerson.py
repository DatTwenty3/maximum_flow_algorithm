from collections import defaultdict
import time

class Graph:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    def BFS(self, s, t, parent):
        visited = [False] * (self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False

    def FordFulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0
        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow += path_flow
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        return max_flow

# Read input from a text file
def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    V = len(lines)
    graph = []
    for line in lines:
        row = list(map(int, line.split()))
        graph.append(row)
    return graph

# Usage
if __name__ == "__main__":
    graph_data = read_input("data/1000_1000.txt")
    g = Graph(graph_data)
    source = 0
    sink = 999
    start_time = time.time()
    print(f"Maximum Flow of Ford-Fulkerson Algorithm:", g.FordFulkerson(source, sink))
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")