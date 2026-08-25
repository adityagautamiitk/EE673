import heapq

def dijkstra(graph, start_node):
    """
    Computes the shortest paths and routing table for a given start node 
    using Dijkstra's algorithm.
    """
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    
    previous_nodes = {node: None for node in nodes}
    pq = [(0, start_node)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    routing_table = {}
    for dest in nodes:
        if dest == start_node:
            routing_table[dest] = "-"
        else:
            current = dest
            while previous_nodes[current] is not None and previous_nodes[current] != start_node:
                current = previous_nodes[current]
                
            if previous_nodes[current] is None:
                routing_table[dest] = "Unreachable"
            else:
                routing_table[dest] = current
                
    return distances, routing_table

def main():
    # Hardcoded graph based on Figure 1 from the assignment
    graph = {
        0: {1: 1, 2: 3, 3: 7},
        1: {0: 1, 2: 1},
        2: {0: 3, 1: 1, 3: 2},
        3: {0: 7, 2: 2}
    }
    
    print("Link-State Routing Algorithm (Dijkstra's)")
    print("="*45)
    
    for node in graph:
        distances, routing_table = dijkstra(graph, node)
        
        print(f"Routing Table for Node {node}:")
        print(f"{'Destination':<15} | {'Total Cost':<12} | {'Next Hop':<10}")
        print("-" * 45)
        for dest in sorted(graph.keys()):
            cost = distances[dest]
            next_hop = routing_table[dest]
            print(f"Node {dest:<10} | {cost:<12} | {next_hop}")
        print("\n")

if __name__ == "__main__":
    main()
