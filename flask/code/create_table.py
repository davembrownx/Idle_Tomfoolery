import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "create table if not exists users(id INTEGER PRIMARY KEY, username text, password text)"

cursor.execute(create_table)


store_name_1 = "Dave's Awesome Store"
store_name_2 = "Dave's Garden of Earthly Delights"
create_table = "create table if not exists stores(name text)"
cursor.execute(create_table)
insert_string = "insert into stores values (?),(?),('Dave')"
cursor.execute(insert_string,(store_name_1,store_name_2))

create_table = "create table if not exists items(name text, price real, store_name text)"
cursor.execute(create_table)
insert_string = "insert into items values ('Chicken Shoes',18.99,?),('Dog Polish',4.99,?), ('Trout Soother',6.99,?),('Tooth Extractor',15.99,?)"
cursor.execute(insert_string,(store_name_1,store_name_1,store_name_2,store_name_2))

connection.commit()
connection.close()
