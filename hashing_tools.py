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
