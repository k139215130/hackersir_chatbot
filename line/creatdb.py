import sqlite3

conn = sqlite3.connect('log.db')
print ("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE NOTE
       (ID INT      NOT NULL,
       DATA  NOT NULL
      );''')
print ("Table created successfully")
conn.commit()
conn.close()