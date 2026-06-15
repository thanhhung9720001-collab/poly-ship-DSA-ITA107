# anagrams.py
# Yêu cầu 2.2: Nhóm các mã coupon là Anagram của nhau (đối xứng chữ cái)

def group_coupon_anagrams(codes):
    """Nhóm các mã coupon là Anagram của nhau"""
    groups = {}
    for code in codes:
        sorted_code = "".join(sorted(code.upper()))
        if sorted_code not in groups:
            groups[sorted_code] = []
        groups[sorted_code].append(code)
    return list(groups.values())

if __name__ == "__main__":
    import sys
    # Đảm bảo console in ra Tiếng Việt Unicode không bị lỗi trên Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Chạy thử độc lập kiểm tra giải thuật
    SAMPLE_COUPONS = ["SAVE10", "AVES10", "SALE5", "LASE5", "EVAS10"]
    print("--- Chạy thử độc lập bài toán Gom nhóm Anagrams ---")
    print("Đầu vào:", SAMPLE_COUPONS)
    print("Kết quả:", group_coupon_anagrams(SAMPLE_COUPONS))
