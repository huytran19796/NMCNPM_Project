import pymysql
import json
from datetime import datetime

def convert_date_format(date_str):
    # Convert from DD/MM/YYYY to YYYY-MM-DD
    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

conn = pymysql.connect(
    host='mysql',
    user='airflow', 
    password='airflow',
    db='airflow',
)

cur = conn.cursor()

with open('/opt/airflow/data_stage_2/conferences.json', 'r') as json_file:
    data = json.load(json_file)
    id = 1
    for row in data:
        # Convert date fields
        deadline = convert_date_format(row['deadline'])
        from_date = convert_date_format(row['from_date'])
        to_date = convert_date_format(row['to_date'])
        report_date = convert_date_format(row['report_date'])

        # Execute insert statement
        cur.execute(
            "INSERT INTO conferences(id, name, link, deadline, subformat, field_id, presenter_id, location_id, from_date, to_date, report_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (id, row['name'], row['link'], deadline, row['subformat'], row['field_id'], row['presenter_id'], row['location_id'], from_date, to_date, report_date)
        )
        id = id + 1

    conn.commit()

conn.close()
