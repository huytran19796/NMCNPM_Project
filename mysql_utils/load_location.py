import pymysql
import json

conn = pymysql.connect(
        host='mysql',
        user='airflow', 
        password = "airflow",
        db='airflow',
        )
cur = conn.cursor()

with open('/opt/airflow/data_stage_2/locations.json', 'r') as json_file:
    data = json.load(json_file)
    for row in data:
        cur.execute('INSERT INTO locations(id, city, country) VALUES(%s, %s, %s)', (row['id'], row['City'], row['Country']))
    conn.commit()

conn.close()