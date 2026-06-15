# subarray_sum.py
# Yêu cầu 2.4: Đếm số khoảng ngày liên tiếp có tổng doanh thu bằng K (Subarray Sum = K)

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

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử độc lập kiểm tra giải thuật
    SAMPLE_REVENUES = [10, 2, -2, -20, 10]
    SAMPLE_K = -10
    print("--- Chạy thử độc lập bài toán Subarray Sum = K ---")
    print(f"Đầu vào doanh thu: {SAMPLE_REVENUES}, K mục tiêu: {SAMPLE_K}")
    print("Kết quả (Số lượng khoảng ngày):", count_revenue_windows(SAMPLE_REVENUES, SAMPLE_K))
