'''
This contains database functions. create_table will create the
table if it does not exist. The insert_data function inserts data
into the database.
'''

import os
import psycopg2

database_url = os.environ['DATABASE_URI']


def create_table():
    '''Create table in database'''

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
            id serial PRIMARY KEY,
            date_time TIMESTAMP NOT NULL,
            sensor1 REAL NOT NULL,
            sensor2 REAL NOT NULL,
            sensor3 REAL NOT NULL
            )''')
        conn.commit()
    except Exception as e:
        print(e)
        return


def insert_data(date_time, sensor1, sensor2, sensor3):
    '''Insert data into database'''

    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    cur.execute('''INSERT INTO sensor_data (
        date_time, sensor1, sensor2, sensor3) VALUES (
        %s, %s, %s, %s)''', (date_time, sensor1, sensor2, sensor3))
    conn.commit()
    conn.close()


create_table()
