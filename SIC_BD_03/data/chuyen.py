import json
import pandas as pd
import os

# Load dữ liệu JSON (nếu lưu nhiều file thì bạn có thể dùng vòng lặp duyệt thư mục)
with open("data_web.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Nếu là một đối tượng, cho vào list
if isinstance(data, dict):
    data = [data]

# Chuyển sang DataFrame
df = pd.DataFrame(data)

# Lưu ra Excel
df.to_excel("output.xlsx", index=False)





