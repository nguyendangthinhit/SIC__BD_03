import os
import json
import sys
from transformers import pipeline
from unidecode import unidecode
from tqdm import tqdm

# ==========================
# CONFIG
# ==========================
candidate_labels = [
    "Đồng cảm", "Chỉ trích", "Hỏi thông tin", "Cổ vũ", 
    "Spam", "Ý kiến khác", "Phân tích", "Giải trí", "Tiêu cực", "Tích cực"
]
MODEL_NAME = "facebook/bart-large-mnli"

# ==========================
# LOAD MODEL
# ==========================
classifier = pipeline("zero-shot-classification", model=MODEL_NAME)
print("✅ Model loaded")

# ==========================
# PREPROCESSING
# ==========================
def is_spam(comment_text):
    """Loại bỏ comment không ý nghĩa như icon-only, link, quá ngắn,..."""
    text = comment_text.strip()
    if len(text) < 5:
        return True
    if all(ord(char) < 128 and not char.isalnum() for char in text):
        return True
    if "http" in text or "www" in text:
        return True
    return False

def classify_comment(text):
    result = classifier(text, candidate_labels)
    label = result["labels"][0]
    score = result["scores"][0]
    return label, score

# ==========================
# COMMENT SUMMARY
# ==========================
def summarize_comments(comments):
    summary = {}
    for comment in comments:
        text = comment.get("text", "").strip()
        if not text or is_spam(text):
            continue
        label, _ = classify_comment(text)
        if label not in summary:
            summary[label] = []
        summary[label].append(comment)
    result = []
    for label, examples in summary.items():
        result.append({
            "label": label,
            "description": f"{len(examples)} comment mang xu hướng '{label}'",
            "example_comments": examples[:3]  # Chỉ lấy 3 comment đầu minh họa
        })
    return {
        "num_opinions": len(result),
        "opinions": result
    }

# ==========================
# MAIN
# ==========================
def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    processed = []

    for post in tqdm(data, desc="🔍 Processing posts"):
        comments = post.get("comments", [])
        if isinstance(comments, dict) and "summary" in comments:
            continue  # Skip nếu đã được xử lý
        post["comments"] = {
            "summary": summarize_comments(comments)
        }
        processed.append(post)

        # Optional: save every 10 posts
        if len(processed) % 10 == 0:
            with open(output_path, "w", encoding="utf-8") as fw:
                json.dump(processed, fw, ensure_ascii=False, indent=2)

    with open(output_path, "w", encoding="utf-8") as fw:
        json.dump(processed, fw, ensure_ascii=False, indent=2)
    print(f"✅ Done! Processed {len(processed)} posts → {output_path}")

# ==========================
# RUN FROM COMMAND LINE
# ==========================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Thiếu đối số đầu vào: python process_drama.py <input_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = input_path.replace(".json", "_test_data.json")
    process_file(input_path, output_path)
