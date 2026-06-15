# rolling_hash.py
# Yêu cầu 2.5: Tìm kiếm pattern log sử dụng thuật toán Rabin-Karp (Rolling Hash)

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

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử độc lập kiểm tra giải thuật
    SAMPLE_TEXT = "SYSTEM_LOG_WARN_AVES10_LOG_SAVE10_PROCESS_ERROR"
    SAMPLE_PATTERN = "SAVE10"
    print("--- Chạy thử độc lập bài toán Rabin-Karp Rolling Hash ---")
    print(f"Văn bản (Text): {SAMPLE_TEXT}")
    print(f"Mẫu cần tìm (Pattern): {SAMPLE_PATTERN}")
    print("Các chỉ số trùng khớp tìm thấy:", rolling_hash_search(SAMPLE_TEXT, SAMPLE_PATTERN))
