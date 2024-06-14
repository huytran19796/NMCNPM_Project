import json
import re
import os, time

# Hàm tách trường Location thành City và Country
def split_location(conference):
    location = conference.get("location", "")
    if location == "???" or not location or "post-proceedings" in location:
        conference["City"] = "updating"
        conference["Country"] = "updating"
    else:
        parts = location.rsplit(',', 1)
        if len(parts) == 2:
            city, country = parts
            conference["City"] = city.strip()
            conference["Country"] = country.strip()
        else:
            conference["City"] = "updating"
            conference["Country"] = "updating"
    
    # Xóa trường Location sau khi tách
    if "location" in conference:
        del conference["location"]

# Đường dẫn đến tệp JSON
input_file = '/opt/airflow/data_stage_2/conferences.json'
output_file_conferences = '/opt/airflow/data_stage_2/conferences.json'
output_file_locations = '/opt/airflow/data_stage_2/locations.json'

# Kiểm tra sự tồn tại của tệp đầu vào
time.sleep(15)
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Tệp {input_file} không tồn tại. Vui lòng kiểm tra đường dẫn.")

# Đọc dữ liệu từ file JSON
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Áp dụng định dạng lại cho từng hội nghị trong dữ liệu
for conference in data:
    split_location(conference)

# Tạo bảng location và thêm cột location_id vào bảng conference
locations = []
location_map = {}
location_id_counter = 1

for conference in data:
    city = conference.get("City", "updating")
    country = conference.get("Country", "updating")
    
    location_key = (city, country)
    if location_key not in location_map:
        location_map[location_key] = location_id_counter
        locations.append({
            "id": location_id_counter,
            "City": city,
            "Country": country
        })
        location_id_counter += 1
    
    conference["location_id"] = location_map[location_key]
    del conference["City"]
    del conference["Country"]

# Xuất dữ liệu JSON đã định dạng lại
with open(output_file_conferences, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

with open(output_file_locations, 'w', encoding='utf-8') as file:
    json.dump(locations, file, indent=4, ensure_ascii=False)

print(f"Dữ liệu đã được định dạng lại và lưu vào {output_file_conferences} và {output_file_locations}")
