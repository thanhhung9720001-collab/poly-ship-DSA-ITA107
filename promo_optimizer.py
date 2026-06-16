# promo_optimizer.py
# Module giải thuật Quy hoạch động (Dynamic Programming) cho POLY-SHIP

def fib_tab(n):
    """Tính số Fibonacci thứ n bằng bottom-up (Tabulation). Trả về (kết quả, danh sách các bước tính)"""
    if n <= 0:
        return 0, ["F(0) = 0"]
    if n == 1:
        return 1, ["F(0) = 0", "F(1) = 1"]
    
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    steps = ["F(0) = 0", "F(1) = 1"]
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        steps.append(f"F({i}) = F({i-1}) + F({i-2}) = {dp[i-1]} + {dp[i-2]} = {dp[i]}")
        
    return dp[n], steps

def climb_stairs(n):
    """Tính số cách leo lên n bậc thang. Trả về (kết quả, danh sách các bước tính)"""
    if n <= 0:
        return 0, []
    if n == 1:
        return 1, ["Stairs(1) = 1 (Cách đi: [1])"]
    if n == 2:
        return 2, ["Stairs(1) = 1", "Stairs(2) = 2 (Cách đi: [1, 1], [2])"]
        
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    steps = ["Stairs(1) = 1", "Stairs(2) = 2"]
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        steps.append(f"Stairs({i}) = Stairs({i-1}) + Stairs({i-2}) = {dp[i-1]} + {dp[i-2]} = {dp[i]}")
        
    return dp[n], steps

def build_combo_dp_table(prices, scores, B):
    """
    Xây dựng bảng quy hoạch động 2D cho bài toán cái túi Knapsack 0/1.
    prices: danh sách giá (weights)
    scores: danh sách điểm ưu tiên (values)
    B: ngân sách tối đa (capacity)
    Trả về ma trận dp kích thước (N+1) x (B+1)
    """
    N = len(prices)
    dp = [[0] * (B + 1) for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        p = prices[i-1]
        s = scores[i-1]
        for b in range(B + 1):
            if p <= b:
                dp[i][b] = max(dp[i-1][b], dp[i-1][b-p] + s)
            else:
                dp[i][b] = dp[i-1][b]
                
    return dp

def trace_combo_from_dp(dp, prices, scores, B):
    """
    Truy vết tìm các sản phẩm được chọn từ bảng dp 2D.
    Trả về danh sách các chỉ số sản phẩm được chọn (0-indexed)
    """
    selected_indices = []
    i = len(prices)
    b = B
    
    while i > 0 and b > 0:
        if dp[i][b] != dp[i-1][b]:
            selected_indices.append(i-1)
            b -= prices[i-1]
        i -= 1
        
    selected_indices.reverse()
    return selected_indices

def combo_knapsack_1d(prices, scores, B):
    """
    Giải thuật Knapsack 1D tối ưu hóa không gian bộ nhớ.
    prices: danh sách giá (weights)
    scores: danh sách điểm ưu tiên (values)
    B: ngân sách tối đa (capacity)
    Trả về (max_score, selected_indices)
    """
    N = len(prices)
    dp = [0] * (B + 1)
    # selected[b] lưu danh sách các chỉ số sản phẩm được chọn tại mức ngân sách b
    selected = [[] for _ in range(B + 1)]
    
    for i in range(N):
        p = prices[i]
        s = scores[i]
        for b in range(B, p - 1, -1):
            if dp[b - p] + s > dp[b]:
                dp[b] = dp[b - p] + s
                selected[b] = selected[b - p] + [i]
                
    return dp[B], selected[B]


def demo_promo_optimizer():
    print("--- Chạy thử độc lập Quy hoạch động tối ưu khuyến mãi ---")
    prices = [10, 20, 30, 15, 25]
    scores = [60, 100, 120, 70, 90]
    B = 50
    
    print(f"Giá sản phẩm: {prices}")
    print(f"Điểm ưu tiên: {scores}")
    print(f"Ngân sách tối đa B: {B}\n")
    
    # 2D Knapsack
    dp_2d = build_combo_dp_table(prices, scores, B)
    selected_2d = trace_combo_from_dp(dp_2d, prices, scores, B)
    print(f"Knapsack 2D: Max Score = {dp_2d[-1][-1]}")
    print(f"Các sản phẩm được chọn (2D): {selected_2d}")
    
    # 1D Knapsack
    max_score_1d, selected_1d = combo_knapsack_1d(prices, scores, B)
    print(f"Knapsack 1D: Max Score = {max_score_1d}")
    print(f"Các sản phẩm được chọn (1D): {selected_1d}")
    
    # Fibonacci & Stairs
    fib_val, fib_steps = fib_tab(6)
    print(f"\nFibonacci(6) = {fib_val}")
    print(f"Các bước: {fib_steps}")
    
    stairs_val, stairs_steps = climb_stairs(5)
    print(f"ClimbStairs(5) = {stairs_val}")
    print(f"Các bước: {stairs_steps}")

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    demo_promo_optimizer()
