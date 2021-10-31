from models.item import ItemModel

class StoreModel:
    def __init__(self,name,items = None):
        self.name = name
        self.items = [] if not items else items

    @classmethod
    def find_store_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        row = cursor.execute("select * from stores where name = ?",(name,)).fetchone()
        connection.close()
        if row:
            return StoreModel(name)
        return None

    def find_item_by_name(self,item_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items where store_name = ? and name = ?"
        row = cursor.execute(query,(self.name,item_name)).fetchone()
        connection.close()
        if row:
            return ItemModel(item_name,row[1])
        return None

