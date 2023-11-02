import numpy as np
import time

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        graph = [list(map(int, line.split())) for line in lines]
    return graph

def ford_fulkerson(graph, source, sink):
    def dfs(graph, node, path, visited):
        if node == sink:
            return path
        for next_node, capacity in enumerate(graph[node]):
            if visited[next_node] or capacity <= 0:
                continue
            visited[next_node] = True
            new_path = path + [(node, next_node)]
            result = dfs(graph, next_node, new_path, visited)
            if result is not None:
                return result
        return None

    max_flow = 0
    while True:
        visited = [False] * len(graph)
        path = dfs(graph, source, [], visited)
        if path is None:
            break
        min_capacity = min(graph[u][v] for u, v in path)
        max_flow += min_capacity
        for u, v in path:
            graph[u][v] -= min_capacity
            graph[v][u] += min_capacity

    return max_flow

if __name__ == "__main__":
    input_file = "data/6_6.txt"
    graph = read_input_file(input_file)
    source = 0  # Điểm bắt đầu
    sink = 5   # Điểm kết thúc

    start_time = time.time()
    max_flow = ford_fulkerson(graph, source, sink)
    end_time = time.time()

    print(f"Maximum Flow of Ford-Fulkerson Algorithm: {max_flow}")
    print(f"Execution Time: {end_time - start_time} seconds")