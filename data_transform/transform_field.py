import json
import re
import random
import os
import time

# Đường dẫn đến tệp JSON
input_file = '/opt/airflow/data_stage_1/stage_1.json'
output_file_conferences = '/opt/airflow/data_stage_2/conferences.json'
output_file_fields = '/opt/airflow/data_stage_2/fields.json'

# Kiểm tra sự tồn tại của tệp đầu vào

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Tệp {input_file} không tồn tại. Vui lòng kiểm tra đường dẫn.")

# Đọc dữ liệu từ file JSON
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Tạo dữ liệu cho bảng field
fields = [
    {"id": 1, "name": "Computer Science"},
    {"id": 2, "name": "Artificial Intelligence"},
    {"id": 3, "name": "Machine Learning"},
    {"id": 4, "name": "Data Science"},
    {"id": 5, "name": "Cybersecurity"},
    {"id": 6, "name": "Software Engineering"}
]

# Tạo danh sách các field_id
field_ids = [field["id"] for field in fields]

# Áp dụng định dạng lại cho từng hội nghị trong dữ liệu
for conference in data:
    # Thêm cột field_id ngẫu nhiên từ danh sách field_ids
    conference["field_id"] = random.choice(field_ids)

# Xuất dữ liệu JSON đã định dạng lại
with open(output_file_conferences, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

with open(output_file_fields, 'w', encoding='utf-8') as file:
    json.dump(fields, file, indent=4, ensure_ascii=False)