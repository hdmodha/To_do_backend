import sqlite3
# Connect to sqlite database
conn = sqlite3.connect('To_Do.db')
# cursor object
cursor = conn.cursor()
# drop query
cursor.execute("DROP TABLE IF EXISTS TASKS")
# create query
query = """CREATE TABLE TASKS(
        TASKID VARCHAR PRIMARY KEY NOT NULL,
        USERID VARCHAR,
        TASKSTATUS VARCHAR,
        DATECREATED LONG,
        TASKNAME CHAR(20) NOT NULL, 
        TASKDETAILS CHAR(20))"""
cursor.execute(query)

conn.commit()
conn.close()
