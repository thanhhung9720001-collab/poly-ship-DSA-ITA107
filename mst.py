class DisjointSetUnion:
    """
    Cấu trúc dữ liệu Disjoint Set Union (DSU) / Union-Find 
    để quản lý các tập hợp rời rạc và kiểm tra chu trình đồ thị.
    Hỗ trợ tối ưu hóa Path Compression và Union by Rank.
    """
    def __init__(self, elements):
        self.parent = {el: el for el in elements}
        self.rank = {el: 0 for el in elements}
        
    def find(self, i):
        # Path compression: Gán trực tiếp nút cha là đại diện tổ tiên
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i, j):
        # Union by rank: Hợp nhất cây thấp hơn vào cây cao hơn
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

def kruskal_mst(vertices, edges):
    """
    Tìm Cây khung tối thiểu (MST) bằng thuật toán Kruskal.
    Input:
        vertices: Danh sách các đỉnh (tên kho hàng) độc nhất.
        edges: Danh sách các cạnh dạng (u, v, cost).
    Output:
        mst_edges: Danh sách các cạnh được chọn vào cây khung tối thiểu.
        total_cost: Tổng chi phí đường truyền liên thông tối thiểu.
    """
    dsu = DisjointSetUnion(vertices)
    
    # Sắp xếp các cạnh tăng dần theo chi phí (cost)
    sorted_edges = sorted(edges, key=lambda x: x[2])
    
    mst_edges = []
    total_cost = 0
    
    for u, v, cost in sorted_edges:
        # u và v phải nằm trong vertices
        if u not in dsu.parent or v not in dsu.parent:
            continue
            
        # Hợp nhất tập hợp, nếu thành công tức là không tạo chu trình
        if dsu.union(u, v):
            mst_edges.append((u, v, cost))
            total_cost += cost
            # Nếu đã chọn đủ V - 1 cạnh thì dừng sớm
            if len(mst_edges) == len(vertices) - 1:
                break
                
    return mst_edges, total_cost

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử độc lập kiểm tra giải thuật
    SAMPLE_VERTICES = ["WH1", "WH2", "HCM", "DN", "HN", "HP"]
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
    
    print("Mạng lưới kho hàng kiểm thử:")
    for u, v, cost in SAMPLE_EDGES:
        print(f"  {u} <-> {v} (Chi phí: {cost})")
        
    mst_edges, total_cost = kruskal_mst(SAMPLE_VERTICES, SAMPLE_EDGES)
    print("\nKết quả cây khung tối thiểu Kruskal:")
    for u, v, cost in mst_edges:
        print(f"  + Kết nối: {u} <-> {v} : Chi phí: {cost}")
    print(f"Tổng chi phí mạng thiết lập tối thiểu: {total_cost}")
