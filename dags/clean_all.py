import pymysql
import os

def delete_data_if_table_exists(table_name):
    cur.execute(f"SHOW TABLES LIKE '{table_name}';")
    result = cur.fetchone()
    if result:
        cur.execute(f'DELETE FROM {table_name};')
        conn.commit()
        print(f"Data from table '{table_name}' has been deleted.")
    else:
        print(f"Table '{table_name}' does not exist.")

# Drop table in Database
conn = pymysql.connect(
        host='mysql',
        user='airflow', 
        password = "airflow",
        db='airflow',
        )
cur = conn.cursor()

cur.execute('USE airflow;')
conn.commit()

delete_data_if_table_exists('conferences')
delete_data_if_table_exists('presenters')
delete_data_if_table_exists('locations')
delete_data_if_table_exists('fields')

conn.close()

# Remove old data: data_stage_2 and data_stage_1
stage_2_conferences='/opt/airflow/data_stage_2/conferences.json'
stage_2_locations='/opt/airflow/data_stage_2/locations.json'
stage_2_fields='/opt/airflow/data_stage_2/fields.json'
stage_2_presenters='/opt/airflow/data_stage_2/presenters.json'
stage_1='/opt/airflow/data_stage_1/stage_1.json'


if os.path.exists(stage_2_conferences):
    os.remove(stage_2_conferences)

if os.path.exists(stage_2_locations):
    os.remove(stage_2_locations)

if os.path.exists(stage_2_fields):
    os.remove(stage_2_fields)

if os.path.exists(stage_2_presenters):
    os.remove(stage_2_presenters)

if os.path.exists(stage_1):
    os.remove(stage_1)
    