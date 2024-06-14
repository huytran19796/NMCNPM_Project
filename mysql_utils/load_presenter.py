import pymysql
import json

conn = pymysql.connect(
        host='mysql',
        user='airflow', 
        password = "airflow",
        db='airflow',
        )
cur = conn.cursor()

with open('/opt/airflow/data_stage_2/presenters.json', 'r') as json_file:
    data = json.load(json_file)
    for row in data:
        cur.execute('INSERT INTO presenters(id, fullname, position, organization) VALUES(%s, %s, %s, %s)', (row['id'], row['fullname'], row['position'], row['organization']))
    conn.commit()

conn.close()