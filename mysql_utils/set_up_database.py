import pymysql
import json

conn = pymysql.connect(
        host='mysql',
        user='airflow', 
        password = "airflow",
        db='airflow',
        )
cur = conn.cursor()

cur.execute('USE airflow;')
conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS fields (id INT NOT NULL PRIMARY KEY,name VARCHAR(100));')
conn.commit()

cur.execute(' \
    CREATE TABLE IF NOT EXISTS locations ( \
    id INT NOT NULL PRIMARY KEY, \
    city VARCHAR(100), \
    country VARCHAR(100) \
);')
conn.commit()

cur.execute(' \
    CREATE TABLE IF NOT EXISTS presenters ( \
    id INT NOT NULL PRIMARY KEY, \
    fullname VARCHAR(100), \
    position VARCHAR(100), \
    organization VARCHAR(100) \
);')
conn.commit()

cur.execute('\
    CREATE TABLE IF NOT EXISTS conferences (\
    id INT NOT NULL PRIMARY KEY,\
    name VARCHAR(100),\
    field_id INT,\
    location_id INT,\
    presenter_id INT,\
    link VARCHAR(200),\
    deadline DATE,\
    from_date DATE,\
    to_date DATE,\
    report_date DATE,\
    subformat VARCHAR(200),\
    CONSTRAINT fk_post_field FOREIGN KEY (field_id) REFERENCES fields(id),\
    CONSTRAINT fk_post_location FOREIGN KEY (location_id) REFERENCES locations(id),\
    CONSTRAINT fk_post_presenter FOREIGN KEY (presenter_id) REFERENCES presenters(id)\
);')
conn.commit()

conn.close()