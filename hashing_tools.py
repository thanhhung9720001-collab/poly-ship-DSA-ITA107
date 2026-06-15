# hashing_tools.py
# Module giải thuật Hashing cho đơn hàng và dữ liệu của Poly-Ship

class Node:
    """Đại diện cho một nút trong Danh sách liên kết đơn (xử lý đụng độ Separate Chaining)"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class OrderHashTable:
    """
    Bảng băm quản lý đơn hàng sử dụng cơ chế xử lý đụng độ Separate Chaining.
    Mỗi phần tử trong mảng buckets là đầu của một Danh sách liên kết.
    """
    def __init__(self, size=10):
        self.size = size
        self.buckets = [None] * size
        self.count = 0  # Đếm số phần tử hiện tại
        
    def _hash(self, key):
        """Hàm băm chuỗi ký tự đơn giản (Polynomial rolling hash mô phỏng)"""
        hash_val = 0
        for char in key:
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val
        
    def insert(self, order_id, order_data):
        """Chèn mới hoặc cập nhật một đơn hàng. Trả về True nếu là chèn mới, False nếu cập nhật."""
        index = self._hash(order_id)
        if not self.buckets[index]:
            self.buckets[index] = Node(order_id, order_data)
            self.count += 1
            return True
            
        curr = self.buckets[index]
        while True:
            if curr.key == order_id:
                curr.value = order_data  # Cập nhật thông tin nếu trùng ID
                return False  # Cập nhật
            if not curr.next:
                curr.next = Node(order_id, order_data)
                self.count += 1
                return True  # Chèn mới thành công
            curr = curr.next
            
    def get(self, order_id):
        """Tìm kiếm chi tiết đơn hàng theo ID, trả về dữ liệu hoặc None"""
        index = self._hash(order_id)
        curr = self.buckets[index]
        while curr:
            if curr.key == order_id:
                return curr.value
            curr = curr.next
        return None
        
    def remove(self, order_id):
        """Xóa đơn hàng khỏi bảng băm. Trả về True nếu xóa thành công, ngược lại False"""
        index = self._hash(order_id)
        curr = self.buckets[index]
        prev = None
        
        while curr:
            if curr.key == order_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.buckets[index] = curr.next
                self.count -= 1
                return True
            prev = curr
            curr = curr.next
        return False

# --- 2.2. Group Anagrams ---
def group_coupon_anagrams(codes):
    """Nhóm các mã coupon là Anagram của nhau"""
    groups = {}
    for code in codes:
        sorted_code = "".join(sorted(code.upper()))
        if sorted_code not in groups:
            groups[sorted_code] = []
        groups[sorted_code].append(code)
    return list(groups.values())

# --- 2.3. Longest Consecutive Days ---
def longest_consecutive_days(days):
    """Tìm chuỗi ngày giao hàng liên tiếp dài nhất"""
    day_set = set(days)
    longest_streak = 0
    for day in day_set:
        # Nếu day là phần tử bắt đầu của chuỗi liên tiếp
        if day - 1 not in day_set:
            current_day = day
            current_streak = 1
            while current_day + 1 in day_set:
                current_day += 1
                current_streak += 1
            longest_streak = max(longest_streak, current_streak)
    return longest_streak

# --- 2.4. Subarray Sum = K (Count Revenue Windows) ---
def count_revenue_windows(revenues, k):
    """Đếm số khoảng ngày liên tiếp có tổng doanh thu đúng bằng k sử dụng Prefix Sum + Hash Map"""
    prefix_sums = {0: 1}  # Lưu tần suất xuất hiện của prefix_sum
    current_sum = 0
    count = 0
    for rev in revenues:
        current_sum += rev
        if current_sum - k in prefix_sums:
            count += prefix_sums[current_sum - k]
        prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1
    return count

# --- 2.5. Rabin-Karp Rolling Hash ---
def rolling_hash_search(text, pattern):
    """Tìm kiếm vị trí của pattern trong text sử dụng thuật toán Rabin-Karp"""
    d = 256 # Số ký tự trong bảng mã
    q = 101 # Một số nguyên tố lớn để chia lấy dư tránh tràn số
    M = len(pattern)
    N = len(text)
    
    if M > N or M == 0:
        return []
        
    p_hash = 0  # mã băm cho pattern
    t_hash = 0  # mã băm cho text cửa sổ trượt
    h = 1
    
    # Giá trị của h sẽ là "pow(d, M-1) % q"
    for i in range(M - 1):
        h = (h * d) % q
        
    # Tính mã băm ban đầu của pattern và cửa sổ trượt đầu tiên
    for i in range(M):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
        
    results = []
    # Trượt pattern trên text từng ký tự một
    for i in range(N - M + 1):
        # Kiểm tra nếu mã băm khớp thì đối chiếu ký tự thực tế tránh đụng độ băm
        if p_hash == t_hash:
            match = True
            for j in range(M):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                results.append(i)
                
        # Tính mã băm cho cửa sổ tiếp theo: bỏ ký tự đầu, thêm ký tự cuối
        if i < N - M:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + M])) % q
            # Chuyển mã băm thành số dương nếu bị âm
            if t_hash < 0:
                t_hash = t_hash + q
                
    return results

def demo_order_hash_table():
    print("--- Chạy thử độc lập Hash Table đơn hàng ---")
    ht = OrderHashTable(size=5)
    
    # Chèn dữ liệu mẫu
    ht.insert("HD01", "Giao HN - 250k")
    ht.insert("HD02", "Giao HCM - 120k")
    ht.insert("HD11", "Giao HP - 90k")  # Mã này dễ đụng độ băm với HD01
    
    print(f"Tra cứu HD01: {ht.get('HD01')}")
    print(f"Tra cứu HD11: {ht.get('HD11')}")
    print(f"Tra cứu HD02: {ht.get('HD02')}")
    
    # Thử xóa
    print(f"Xóa HD11: {ht.remove('HD11')}")
    print(f"Tra cứu lại HD11 sau khi xóa: {ht.get('HD11')}")

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
    demo_order_hash_table()
