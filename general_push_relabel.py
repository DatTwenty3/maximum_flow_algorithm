import time

#Config parametter at here!
data_path = 'data/6_6.txt'
#source = 0
#sink = 99


class Edge:
    def __init__(self, flow, capacity, u, v):
        self.flow = flow
        self.capacity = capacity
        self.u = u
        self.v = v

class Vertex:
    def __init__(self, h, e_flow):
        self.h = h
        self.e_flow = e_flow

class Graph:
    def __init__(self, V):
        self.V = V
        self.edge = []
        self.ver = []
        for i in range(V):
            self.ver.append(Vertex(0, 0))

    def addEdge(self, u, v, capacity):
        self.edge.append(Edge(0, capacity, u, v))

    def preflow(self, s):
        self.ver[s].h = self.V
        for i in range(len(self.edge)):
            if self.edge[i].u == s:
                self.edge[i].flow = self.edge[i].capacity
                self.ver[self.edge[i].v].e_flow += self.edge[i].flow
                self.edge.append(Edge(-self.edge[i].flow, 0, self.edge[i].v, s))

    def overFlowVertex(self):
        for i in range(1, len(self.ver) - 1):
            if self.ver[i].e_flow > 0:
                return i
        return -1

    def updateReverseEdgeFlow(self, i, flow):
        u = self.edge[i].v
        v = self.edge[i].u
        for j in range(0, len(self.edge)):
            if self.edge[j].v == v and self.edge[j].u == u:
                self.edge[j].flow -= flow
                return
        e = Edge(0, flow, u, v)
        self.edge.append(e)

    def push(self, u):
        for i in range(len(self.edge)):
            if self.edge[i].u == u:
                if self.edge[i].flow == self.edge[i].capacity:
                    continue
                if self.ver[u].h > self.ver[self.edge[i].v].h:
                    flow = min(self.edge[i].capacity - self.edge[i].flow, self.ver[u].e_flow)
                    self.ver[u].e_flow -= flow
                    self.ver[self.edge[i].v].e_flow += flow
                    self.edge[i].flow += flow
                    self.updateReverseEdgeFlow(i, flow)
                    return True
        return False

    def relabel(self, u):
        mh = 2100000
        for i in range(len(self.edge)):
            if self.edge[i].u == u:
                if self.edge[i].flow == self.edge[i].capacity:
                    continue
                if self.ver[self.edge[i].v].h < mh:
                    mh = self.ver[self.edge[i].v].h
                    self.ver[u].h = mh + 1

    def getMaxFlow(self, s, t):
        self.preflow(s)
        while self.overFlowVertex() != -1:
            u = self.overFlowVertex()
            if not self.push(u):
                self.relabel(u)
        return self.ver[len(self.ver) - 1].e_flow

# Function to read the flow network data from a text file
def read_flow_network_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            V = len(lines)
            g = Graph(V)
            for i in range(V):
                capacities = list(map(int, lines[i].strip().split()))
                for j in range(V):
                    if capacities[j] > 0:
                        g.addEdge(i, j, capacities[j])
            return g
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

# Example usage:
file_path = data_path
g = read_flow_network_from_file(file_path)

if g is not None:
    s = 0
    t = g.V - 1
    start_time = time.time()
    max_flow = g.getMaxFlow(s, t)
    end_time = time.time()
    print(f"Maximum Flow of Push Relabel Algorithm: {max_flow}")
    print(f"Execution Time: {end_time - start_time} seconds")