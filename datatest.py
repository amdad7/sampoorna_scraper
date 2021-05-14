import sqlite3

con=sqlite3.connect('8Bdatabase.sqlite3')
cur=con.cursor()
cur.execute('SELECT id,name FROM data WHERE gender=?',('Female',))
for row in cur:
    print(row)
