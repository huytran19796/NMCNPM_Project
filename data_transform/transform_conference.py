import json
import re
import os
from datetime import datetime

# Đường dẫn đến tệp JSON
input_file = '/opt/airflow/data_stage_2/conferences.json'
output_file_conferences = '/opt/airflow/data_stage_2/conferences.json'

# Bản đồ từ tên tháng sang số tháng
MONTHS = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

# Hàm định dạng lại trường deadline
def format_deadline(conference):
    deadline = conference.get("deadline", "")
    if not deadline:
        return
    
    # Trường hợp có hai ngày và một tháng, hoặc hai ngày và hai tháng
    match = re.match(r"(\d{1,2})/(\d{1,2}) (\w+) / (\w+) (\d{4})", deadline)
    if match:
        day1, day2, month1, month2, year = match.groups()
        formatted_deadline = f"{day1.zfill(2)}/{MONTHS[month1]}/{year}"
        conference["deadline"] = formatted_deadline
        return

    # Trường hợp có hai ngày và một tháng
    match = re.match(r"(\d{1,2})/(\d{1,2}) (\w+) (\d{4})", deadline)
    if match:
        day1, day2, month, year = match.groups()
        formatted_deadline = f"{day1.zfill(2)}/{MONTHS[month]}/{year}"
        conference["deadline"] = formatted_deadline
        return

    # Trường hợp có hai tháng và hai ngày
    match = re.match(r"(\d{1,2}) (\w+) / (\d{1,2}) (\w+) (\d{4})", deadline)
    if match:
        day1, month1, day2, month2, year = match.groups()
        formatted_deadline = f"{day1.zfill(2)}/{MONTHS[month1]}/{year}"
        conference["deadline"] = formatted_deadline
        return

    # Trường hợp có một mốc thời gian
    match = re.match(r"(\d{1,2}) (\w+) (\d{4})", deadline)
    if match:
        day, month, year = match.groups()
        formatted_deadline = f"{day.zfill(2)}/{MONTHS[month]}/{year}"
        conference["deadline"] = formatted_deadline
        return
    
    # Kiểm tra định dạng cuối cùng
    match = re.match(r"(\d{2})/(\d{2})/(\d{4})", deadline)
    if match:
        try:
            datetime.strptime(deadline, "%d/%m/%Y")
        except ValueError:
            deadline = datetime.now().strftime("%d/%m/%Y")
    else:
        deadline = datetime.now().strftime("%d/%m/%Y")
    
    conference["deadline"] = deadline

# Hàm định dạng lại trường date và tạo hai trường from_date và to_date
def format_date(conference):
    date = conference.get("date", "")
    deadline = conference.get("deadline", "")
    
    # Đảm bảo rằng date là một chuỗi
    if not isinstance(date, str):
        date = ""

    # Trường hợp có hai ngày và một tháng, hoặc hai ngày và hai tháng
    match = re.match(r"(\d{1,2})-(\d{1,2}) (\w+) (\d{4})", date)
    if match:
        day1, day2, month, year = match.groups()
        from_date = f"{day1.zfill(2)}/{MONTHS[month]}/{year}"
        to_date = f"{day2.zfill(2)}/{MONTHS[month]}/{year}"
        conference["from_date"] = from_date
        conference["to_date"] = to_date
    else:
        # Trường hợp có hai ngày và hai tháng
        match = re.match(r"(\d{1,2}) (\w+)-(\d{1,2}) (\w+) (\d{4})", date)
        if match:
            day1, month1, day2, month2, year = match.groups()
            from_date = f"{day1.zfill(2)}/{MONTHS[month1]}/{year}"
            to_date = f"{day2.zfill(2)}/{MONTHS[month2]}/{year}"
            conference["from_date"] = from_date
            conference["to_date"] = to_date
        else:
            # Trường hợp có một ngày
            match = re.match(r"(\d{1,2}) (\w+) (\d{4})", date)
            if match:
                day, month, year = match.groups()
                from_date = to_date = f"{day.zfill(2)}/{MONTHS[month]}/{year}"
                conference["from_date"] = from_date
                conference["to_date"] = to_date
            else:
                # Trường hợp date null hoặc không hợp lệ, sử dụng deadline
                if deadline:
                    conference["from_date"] = deadline
                    conference["to_date"] = deadline
                else:
                    conference["from_date"] = "updating"
                    conference["to_date"] = "updating"
    
    # Xóa trường date sau khi định dạng lại
    if "date" in conference:
        del conference["date"]

# Kiểm tra sự tồn tại của tệp đầu vào
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Tệp {input_file} không tồn tại. Vui lòng kiểm tra đường dẫn.")

# Đọc dữ liệu từ file JSON
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Áp dụng định dạng lại cho từng hội nghị trong dữ liệu
for conference in data:
    format_deadline(conference)
    format_date(conference)
    
    # Thêm cột report_date giống như deadline
    conference["report_date"] = conference.get("deadline", "updating")

# Xuất dữ liệu JSON đã định dạng lại
with open(output_file_conferences, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"Dữ liệu đã được định dạng lại và lưu vào {output_file_conferences}")
