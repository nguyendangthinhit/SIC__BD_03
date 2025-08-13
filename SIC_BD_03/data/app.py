from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Cấu hình repo bạn cần chia sẻ
GITHUB_REPO = "nguyendangthinhit/SIC__BD_03"
GITHUB_BRANCH = "data"
GITHUB_FOLDER = "SIC_BD_03/data"



# Nếu repo public, không cần token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # có thể bỏ nếu public
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

@app.route("/get_file", methods=["GET"])
def get_file():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    file_path = f"{GITHUB_FOLDER}/{filename}" if GITHUB_FOLDER else filename

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}?ref={GITHUB_BRANCH}"

    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return jsonify({"error": "File not found", "detail": r.json()}), r.status_code

    data = r.json()
    raw_url = data["download_url"]

    file_content = requests.get(raw_url).text

    return jsonify({
        "file": filename,
        "content": file_content
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
