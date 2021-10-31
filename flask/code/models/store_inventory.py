from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name,items = None):
        self.name = name
        self.items = [] if not items else items

    @classmethod
    def find_stores(cls):
        return cls.query

    @classmethod
    def find_store_by_name(cls,name):
        store = StoreModel.query.filter_by(name=name).first()
        if store:
            store.items = []
            for item in ItemModel.query.filter_by(store_name=store.name):
                store.items.append(item)
            return store
        return None
    
    def upsert_store(self):
        for item in self.items:
            self.upsert_item_in_store(item)
        db.session.add(self)
        db.session.commit()

    def delete_store(self):
        for item in self.items:
            self.delete_item_from_store(item)
        db.session.delete(self)
        db.session.commit()

    def find_items(self):
        return ItemModel.query.filter_by(store_name=self.name)

    def find_item_by_name(self,item_name):
        return ItemModel.query.filter_by(name = item_name, store_name = self.name).first()
 
    def upsert_item_in_store(self,item):
        item.store_name = self.name
        item.upsert_item()

    def delete_item_from_store(self,item):
        item.store_name = self.name
        item.delete_item()



class ItemModel(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_name = db.Column(db.String(80),foreign_key=True)

    def __init__(self,name,price,store_name):
        self.name = name
        self.price = price
        self.store_name = store_name

    def upsert_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
