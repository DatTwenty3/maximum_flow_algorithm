import time
class Edge:
    def __init__(self, v, flow, C, rev):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev

# Residual Graph
class Graph:
    def __init__(self, V):
        self.adj = [[] for i in range(V)]
        self.V = V
        self.level = [0 for i in range(V)]

    def addEdge(self, u, v, C):
        a = Edge(v, 0, C, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)

    def BFS(self, s, t):
        for i in range(self.V):
            self.level[i] = -1
        self.level[s] = 0
        q = []
        q.append(s)
        while q:
            u = q.pop(0)
            for i in range(len(self.adj[u])):
                e = self.adj[u][i]
                if self.level[e.v] < 0 and e.flow < e.C:
                    self.level[e.v] = self.level[u] + 1
                    q.append(e.v)
        return False if self.level[t] < 0 else True

    def sendFlow(self, u, flow, t, start):
        if u == t:
            return flow
        while start[u] < len(self.adj[u]):
            e = self.adj[u][start[u]]
            if self.level[e.v] == self.level[u] + 1 and e.flow < e.C:
                curr_flow = min(flow, e.C - e.flow)
                temp_flow = self.sendFlow(e.v, curr_flow, t, start)
                if temp_flow and temp_flow > 0:
                    e.flow += temp_flow
                    self.adj[e.v][e.rev].flow -= temp_flow
                    return temp_flow
            start[u] += 1

    def DinicMaxflow(self, s, t):
        if s == t:
            return -1
        total = 0
        while self.BFS(s, t) == True:
            start = [0 for i in range(self.V + 1)]
            while True:
                flow = self.sendFlow(s, float('inf'), t, start)
                if not flow:
                    break
                total += flow
        return total

# Read input from a text file
def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    V = len(lines)
    g = Graph(V)
    for i in range(V):
        data = list(map(int, lines[i].split()))
        for j in range(V):
            if data[j] > 0:
                g.addEdge(i, j, data[j])
    return g

# Usage
if __name__ == "__main__":
    g = read_input("data/1000_1000.txt")
    start_time = time.time()
    print(f"Maximum Flow of Dinic’s Algorithm:", g.DinicMaxflow(0, 999))
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")
