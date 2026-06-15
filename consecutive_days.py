# consecutive_days.py
# Yêu cầu 2.3: Tìm chuỗi ngày giao hàng liên tiếp dài nhất

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

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử độc lập kiểm tra giải thuật
    SAMPLE_DAYS = [100, 4, 200, 1, 3, 2, 5]
    print("--- Chạy thử độc lập bài toán Chuỗi ngày giao hàng liên tiếp dài nhất ---")
    print("Đầu vào:", SAMPLE_DAYS)
    print("Kết quả (Độ dài chuỗi liên tiếp):", longest_consecutive_days(SAMPLE_DAYS))
