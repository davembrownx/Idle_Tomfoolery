import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "create table users(id int, username text, password text)"

cursor.execute(create_table)

user1 = (1,'david','asdf')
insert_query = "insert into users values (?, ?, ?)"

cursor.execute(insert_query,user1)

userlist = [(2,'alice','sdgg'),(3,'bob','dfgh')]
cursor.executemany(insert_query,userlist)

select_query = "select * from users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
