import sys
import json
import re
from typing import List, Dict
from pathlib import Path

def parse_post_from_lines(lines: List[str]) -> Dict:
    post_data = {
        "url": "",
        "poster": "",
        "author": "",
        "content": "",
        "time": "",
        "comments": []
    }
    i = 0

    while i < len(lines):
        if lines[i].startswith("Link "):
            post_data["url"] = lines[i][5:].strip()
        elif lines[i].startswith("Bài viết của"):
            post_data["poster"] = lines[i][12:].strip()
        elif lines[i] == "Tác giả":
            post_data["author"] = lines[i+1].strip()
            i += 1
        elif lines[i].startswith("Nội dung bài viết:"):
            post_data["content"] = lines[i][20:].strip()
        elif re.match(r"\d+ (giây|phút|giờ|ngày|tuần|tháng|năm)", lines[i]):
            post_data["time"] = lines[i]
        elif lines[i] == "Trả lời":
            break
        i += 1

    while i < len(lines):
        if lines[i] in {"Trả lời", "Đã chỉnh sửa", "Fan cứng", "Fan đang lên", "Xem bản dịch"}:
            i += 1
            continue

        user = lines[i]
        text = lines[i+1] if i+1 < len(lines) else ""
        time = lines[i+2] if i+2 < len(lines) else ""
        if not re.match(r"\d+ (giây|phút|giờ|ngày|tuần|tháng|năm)", time):
            i += 1
            continue

        post_data["comments"].append({
            "user": user,
            "text": text,
            "time": time
        })
        i += 3

    return post_data

def main():
    if len(sys.argv) != 2:
        print("⚠️ Cách dùng: python process.py <path/tới/file.txt>")
        print("Ví dụ: python process.py thinh/cao.txt")
        # chỉ cần đặt tên đúng như bên readme tui nói rồi bấm y z là đc
        sys.exit(1)

    txt_path = Path(sys.argv[1])

    if not txt_path.exists():
        print(f"❌ Không tìm thấy file: {txt_path}")
        sys.exit(1)

    # Lấy tên người cào (thư mục cha)
    user_folder = txt_path.parent.name
    json_path = txt_path.parent / f"{user_folder}_all_posts.json"

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_post = parse_post_from_lines(lines)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            all_posts = json.load(f)
    except FileNotFoundError:
        all_posts = []

    all_posts.append(parsed_post)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã xử lý và thêm vào file {json_path}")

if __name__ == "__main__":
    main()
