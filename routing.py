import heapq

def build_graph(edges):
    """
    Xây dựng danh sách kề (adjacency list) cho đồ thị vô hướng.
    Input: Danh sách các cạnh dạng (u, v, cost).
    Output: Dictionary graph = {u: [(v, cost), ...], ...}.
    """
    graph = {}
    for u, v, cost in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, cost))
        graph[v].append((u, cost))
    return graph

def dijkstra(graph, source):
    """
    Thuật toán Dijkstra tìm đường đi ngắn nhất từ đỉnh source.
    Sử dụng priority queue (heapq).
    Output:
        dist: Dictionary lưu chi phí nhỏ nhất từ source tới mỗi đỉnh.
        parent: Dictionary lưu đỉnh cha để phục vụ việc truy vết đường đi.
    """
    dist = {node: float('inf') for node in graph}
    parent = {node: None for node in graph}
    
    if source not in graph:
        return dist, parent
        
    dist[source] = 0
    pq = [(0, source)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Nếu đã tìm thấy đường đi ngắn hơn trước đó, bỏ qua chặng này
        if current_dist > dist[u]:
            continue
            
        for v, cost in graph[u]:
            distance = current_dist + cost
            if distance < dist[v]:
                dist[v] = distance
                parent[v] = u
                heapq.heappush(pq, (distance, v))
                
    return dist, parent

def shortest_route(graph, source, target):
    """
    Truy vết và trả về đường đi ngắn nhất từ source đến target.
    Output:
        total_cost: Chi phí của đường đi (float('inf') nếu không liên thông).
        route: Danh sách các đỉnh đi qua theo thứ tự từ source đến target.
    """
    if source not in graph or target not in graph:
        return float('inf'), []
        
    dist, parent = dijkstra(graph, source)
    
    if dist[target] == float('inf'):
        return float('inf'), []
        
    # Truy vết đường đi ngược từ target về source
    route = []
    curr = target
    while curr is not None:
        route.append(curr)
        curr = parent[curr]
    
    route.reverse()
    return dist[target], route

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử nghiệm nhỏ độc lập để kiểm tra
    SAMPLE_EDGES = [
        ("WH1", "WH2", 15),
        ("WH1", "HCM", 22),
        ("WH2", "HCM", 10),
        ("WH2", "DN", 30),
        ("HCM", "DN", 18),
        ("HN", "DN", 25),
        ("HN", "HP", 5),
        ("HP", "WH1", 40)
    ]
    
    graph = build_graph(SAMPLE_EDGES)
    print("Mạng kho hàng mẫu (danh sách kề):")
    for node, neighbors in graph.items():
        print(f"  {node} -> {neighbors}")
        
    source = "WH1"
    target = "HN"
    print(f"\nTìm đường đi ngắn nhất từ {source} đến {target}:")
    cost, route = shortest_route(graph, source, target)
    
    print(f"  - Chi phí: {cost}")
    print(f"  - Lộ trình: {' -> '.join(route)}")
