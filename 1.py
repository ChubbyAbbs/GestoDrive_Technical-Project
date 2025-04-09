import heapq
from collections import defaultdict

def bellman_ford(graph, V, src):
    dist = [float('inf')] * V
    dist[src] = 0
    for _ in range(V - 1):
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return dist

def dijkstra(graph, V, src):
    dist = [float('inf')] * V
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

def johnsons_algorithm(original_graph, V):
    # Step 1: Add dummy node V connected to all others with 0-weight edges
    graph = defaultdict(list, original_graph)
    graph[V] = [(v, 0) for v in range(V)]

    # Step 2: Bellman-Ford from dummy node
    h = bellman_ford(graph, V + 1, V)

    # Step 3: Reweight the edges
    reweighted_graph = defaultdict(list)
    for u in original_graph:
        for v, w in original_graph[u]:
            new_weight = w + h[u] - h[v]
            reweighted_graph[u].append((v, new_weight))

    # Step 4: Run Dijkstra for each vertex and re-adjust distances
    distance_matrix = []
    for u in range(V):
        dijkstra_result = dijkstra(reweighted_graph, V, u)
        adjusted = [d - h[u] + h[v] if d != float('inf') else float('inf') for v, d in enumerate(dijkstra_result)]
        distance_matrix.append(adjusted)

    return distance_matrix
# Example graph: 4 vertices, edges with positive and negative weights (no negative cycle)
original_graph = {
    0: [(1, 1), (2, 4)],
    1: [(2, -3)],
    2: [(3, 2)],
    3: [(1, 7)]
}

V = 4

# Run Johnson's Algorithm
result = johnsons_algorithm(original_graph, V)

# Print the shortest distance matrix
print("Shortest distance matrix using Johnson's Algorithm:")
for i, row in enumerate(result):
    print(f"From vertex {i}: {row}")

