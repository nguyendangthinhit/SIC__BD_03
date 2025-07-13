import json
import re
import os

def normalize(text):
    """Chuẩn hóa chuỗi: loại bỏ khoảng trắng thừa ở đầu, cuối, và rút gọn giữa"""
    return re.sub(r'\s+', ' ', text.strip())

def is_duplicate_link_and_add(new_entry, file_path='links.json'):
    # Chuẩn hóa input mới
    new_name = normalize(new_entry.get('name', ''))
    new_time = normalize(new_entry.get('time', ''))
    new_content = normalize(new_entry.get('content', ''))

    new_entry_normalized = {
        "name": new_name,
        "time": new_time,
        "content": new_content,
        "source_url": new_entry.get("url", ""),  # giữ nguyên content gốc
    }

    # Tải dữ liệu từ file (nếu có)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    # Kiểm tra trùng
    for entry in data:
        name = normalize(entry.get('name', ''))
        time = normalize(entry.get('time', ''))
        content = normalize(entry.get('content', ''))
        if new_name == name and new_time == time and new_content == content:
            return "trùng rồi"

    # Nếu không trùng, thêm vào file
    data.append(new_entry_normalized)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return "oke"

# =============================
# 👇 Đoạn test mẫu
# =============================

if __name__ == "__main__":
    test_input = {
        "name": "Kaito Kid",
        "time": "10 tháng 7 lúc 14:17",
        "content": "Đề thi tốt nghiệp THPT quá khó, Quốc hội yêu cầu báo cáo",
        "source_url": "https://www.facebook.com/share/p/1C8B5TNDDp/"
    }

    print(is_duplicate_link_and_add(test_input))  # Kết quả: "oke" hoặc "trùng rồi"
