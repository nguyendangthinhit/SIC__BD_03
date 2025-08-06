import json
import re
import os
from datetime import datetime
from unidecode import unidecode

# ====== 1. LOAD FILE ======
base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "mau.json"), "r", encoding="utf-8") as f:
    raw_data = json.load(f)


with open("links_fb.json", "r", encoding="utf-8") as f:
    time_data = json.load(f)

# ====== 2. TẠO BẢN ĐỒ TỪ LINK → TIME THẬT ======
time_lookup = {item["source_url"].strip(): item["time"].strip() for item in time_data}

# ====== 3. HÀM LỌC COMMENT RÁC ======
def is_valid_comment(text):
    if not text or len(text.strip()) < 5:
        return False
    if re.fullmatch(r"[^\w\s]+", text.strip()):
        return False
    if "http" in text or "facebook.com" in text or "tiktok.com" in text:
        return False
    if re.match(r"^[A-ZÀ-Ỵa-zà-ỹ0-9_.\- ]{1,20}[:\-]?$", text.strip()):
        return False
    return True

# ====== 4. GOM Ý KIẾN (tạm thời = bằng keyword, chưa dùng ML) ======
def classify_opinions(comments):
    opinions = []
    group_1 = []
    group_2 = []
    neutral = []

    for c in comments:
        text = c["text"].lower()
        if "thương" in text or "cảm động" in text or "xúc động" in text:
            group_1.append(c)
        elif "làm sao" in text or "hướng dẫn" in text or "coi sao" in text:
            group_2.append(c)
        else:
            neutral.append(c)

    if group_1:
        opinions.append({
            "label": "Đồng cảm",
            "description": "Nhiều người bày tỏ cảm xúc thương cảm và xúc động.",
            "example_comments": group_1[:2]
        })
    if group_2:
        opinions.append({
            "label": "Hỏi cách xem",
            "description": "Nhiều người quan tâm cách xem lại hình ảnh cũ trên Google Maps.",
            "example_comments": group_2[:2]
        })
    if neutral:
        opinions.append({
            "label": "Ý kiến khác",
            "description": "Một số bình luận khác chưa rõ xu hướng.",
            "example_comments": neutral[:2]
        })

    return {
        "num_opinions": len(opinions),
        "opinions": opinions
    }

# ====== 5. XỬ LÝ TOÀN BỘ DỮ LIỆU ======
processed = []
for post in raw_data:
    # 1. Gộp poster + author
    poster = post.get("poster") or post.get("author")

    # 2. Chuẩn hóa thời gian bài viết
    real_time = time_lookup.get(post["url"].strip(), post["time"])

    # 3. Lọc comment
    raw_comments = post.get("comments", [])
    valid_comments = [c for c in raw_comments if is_valid_comment(c["text"])]

    # 4. Gom ý kiến dư luận
    summary = classify_opinions(valid_comments)

    # 5. Đóng gói kết quả
    processed.append({
        "url": post["url"].strip(),
        "poster": poster.strip(),
        "content": post["content"].strip(),
        "time": real_time,
        "comments": {
            "summary": summary
        }
    })

# ====== 6. GHI FILE ======
with open("test_du_lieu.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print("✅ Đã xử lý xong. File xuất: test_du_lieu.json")
