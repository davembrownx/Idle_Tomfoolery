from models.store import StoreModel

class Item:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def insert_item(self,store_name):
        connection = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "insert into items values (?,?,?)"
        cursor.execute(query,(self.name,self.price,store_name))
        connection.commit()
        connection.close()
        return {"name": self.name,"price":self.price}

    def update_item(self,price,store_name):
        connection = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "update items set price = ? where item_name = ? and store_name = ?"
        cursor.execute(query,(price,self.name,store_name))
        connection.commit()
        connection.close()
        return {"name": item_name,"price":price}
