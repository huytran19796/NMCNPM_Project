import json
import re
import random
import os
import time

# Đường dẫn đến tệp JSON
input_file = '/opt/airflow/data_stage_2/conferences.json'
output_file_conferences = '/opt/airflow/data_stage_2/conferences.json'
output_file_presenters = '/opt/airflow/data_stage_2/presenters.json'

# Kiểm tra sự tồn tại của tệp đầu vào

time.sleep(5)
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Tệp {input_file} không tồn tại. Vui lòng kiểm tra đường dẫn.")

# Đọc dữ liệu từ file JSON
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Tạo dữ liệu cho bảng presenter
presenters = [
    {"id": 1, "fullname": "John Doe", "position": "Senior Researcher", "organization": "ABC Corporation"},
    {"id": 2, "fullname": "Alice Smith", "position": "Data Scientist", "organization": "XYZ Corp"},
    {"id": 3, "fullname": "Michael Johnson", "position": "Software Engineer", "organization": "Tech Solutions Inc."},
    {"id": 4, "fullname": "Emily Brown", "position": "Project Manager", "organization": "Global Innovations Ltd."},
    {"id": 5, "fullname": "David Wilson", "position": "Professor", "organization": "University of Science"},
    {"id": 6, "fullname": "Jessica Taylor", "position": "Product Manager", "organization": "TechGenius"},
    {"id": 7, "fullname": "Daniel Clark", "position": "Research Associate", "organization": "Tech Innovations Ltd."},
    {"id": 8, "fullname": "Sophia Garcia", "position": "Software Developer", "organization": "Data Systems Corp"},
    {"id": 9, "fullname": "James Anderson", "position": "Data Analyst", "organization": "Analytics Inc."},
    {"id": 10, "fullname": "Olivia Martinez", "position": "Team Lead", "organization": "Innovate Solutions"},
    {"id": 11, "fullname": "Alexander Lee", "position": "UX Designer", "organization": "Digital Creations Ltd."},
    {"id": 12, "fullname": "Emma Rodriguez", "position": "Systems Architect", "organization": "Tech Systems Ltd."},
    {"id": 13, "fullname": "William Wright", "position": "Research Scientist", "organization": "Tech Innovations Inc."},
    {"id": 14, "fullname": "Ava Scott", "position": "Product Owner", "organization": "Agile Solutions Corp"},
    {"id": 15, "fullname": "Liam Green", "position": "Software Engineer", "organization": "Code Masters Ltd."},
    {"id": 16, "fullname": "Isabella Adams", "position": "Data Engineer", "organization": "Big Data Inc."},
    {"id": 17, "fullname": "Mason Baker", "position": "Project Coordinator", "organization": "Tech Solutions Inc."},
    {"id": 18, "fullname": "Mia Perez", "position": "Research Assistant", "organization": "Innovate Labs"},
    {"id": 19, "fullname": "Logan Evans", "position": "Business Analyst", "organization": "Tech Innovations Ltd."},
    {"id": 20, "fullname": "Charlotte Cox", "position": "Software Developer", "organization": "Data Systems Corp"},
    {"id": 21, "fullname": "Benjamin Flores", "position": "UX Designer", "organization": "Digital Creations Ltd."},
    {"id": 22, "fullname": "Amelia Stewart", "position": "Systems Architect", "organization": "Tech Systems Ltd."},
    {"id": 23, "fullname": "Elijah Richardson", "position": "Research Scientist", "organization": "Tech Innovations Inc."},
    {"id": 24, "fullname": "Harper Gray", "position": "Product Owner", "organization": "Agile Solutions Corp"},
    {"id": 25, "fullname": "Abigail Rivera", "position": "Software Engineer", "organization": "Code Masters Ltd."},
    {"id": 26, "fullname": "Ethan Murphy", "position": "Data Engineer", "organization": "Big Data Inc."},
    {"id": 27, "fullname": "Evelyn Long", "position": "Project Coordinator", "organization": "Tech Solutions Inc."},
    {"id": 28, "fullname": "Michaela Morris", "position": "Research Assistant", "organization": "Innovate Labs"},
    {"id": 29, "fullname": "Jackson Bell", "position": "Business Analyst", "organization": "Tech Innovations Ltd."},
    {"id": 30, "fullname": "Sofia Rivera", "position": "Software Developer", "organization": "Data Systems Corp"},
    {"id": 31, "fullname": "Jacob Martinez", "position": "UX Designer", "organization": "Digital Creations Ltd."},
    {"id": 32, "fullname": "Madison Baker", "position": "Systems Architect", "organization": "Tech Systems Ltd."},
    {"id": 33, "fullname": "Noah Adams", "position": "Research Scientist", "organization": "Tech Innovations Inc."},
    {"id": 34, "fullname": "Avery Scott", "position": "Product Owner", "organization": "Agile Solutions Corp"},
    {"id": 35, "fullname": "Grace Green", "position": "Software Engineer", "organization": "Code Masters Ltd."},
    {"id": 36, "fullname": "Lucas Evans", "position": "Data Engineer", "organization": "Big Data Inc."},
    {"id": 37, "fullname": "Lily Cox", "position": "Project Coordinator", "organization": "Tech Solutions Inc."},
    {"id": 38, "fullname": "Aiden Flores", "position": "Research Assistant", "organization": "Innovate Labs"},
    {"id": 39, "fullname": "Brooklyn Stewart", "position": "Business Analyst", "organization": "Tech Innovations Ltd."},
    {"id": 40, "fullname": "Daniel Murphy", "position": "Software Developer", "organization": "Data Systems Corp"},
    {"id": 41, "fullname": "Ella Richardson", "position": "UX Designer", "organization": "Digital Creations Ltd."},
    {"id": 42, "fullname": "Nathan Gray", "position": "Systems Architect", "organization": "Tech Systems Ltd."},
    {"id": 43, "fullname": "Scarlett Long", "position": "Research Scientist", "organization": "Tech Innovations Inc."},
    {"id": 44, "fullname": "Samuel Morris", "position": "Product Owner", "organization": "Agile Solutions Corp"},
    {"id": 45, "fullname": "Hannah Bell", "position": "Software Engineer", "organization": "Code Masters Ltd."},
    {"id": 46, "fullname": "Dylan Rivera", "position": "Data Engineer", "organization": "Big Data Inc."},
    {"id": 47, "fullname": "Addison Baker", "position": "Project Coordinator", "organization": "Tech Solutions Inc."},
    {"id": 48, "fullname": "Mila Scott", "position": "Research Assistant", "organization": "Innovate Labs"},
    {"id": 49, "fullname": "Andrew Evans", "position": "Business Analyst", "organization": "Innovate Labs"}
]

# Tạo danh sách các presenter_id
presenter_ids = [presenter["id"] for presenter in presenters]

# Áp dụng định dạng lại cho từng hội nghị trong dữ liệu
for conference in data:
    # Thêm cột presenter_id ngẫu nhiên từ danh sách presenter_ids
    conference["presenter_id"] = random.choice(presenter_ids)

# Xuất dữ liệu JSON đã định dạng lại
with open(output_file_conferences, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
    
with open(output_file_presenters, 'w', encoding='utf-8') as file:
    json.dump(presenters, file, indent=4, ensure_ascii=False)