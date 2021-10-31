from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store_inventory import StoreModel, ItemModel
import sqlite3

class Store(Resource):

    @jwt_required()
    def get(self,name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {"store":{"name": store.name}}
        return {"message": "No store with name {} found.".format(name)}


    def post(self,name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'message': "Store with name {} already exists".format(name)}, 400

        store = StoreModel(name)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("insert into stores values (?)",(store.name,))

        connection.commit()
        connection.close()
        new_store = {'name': store.name, 'items':[]}
        return new_store, 201

    def delete(self,name):
        store = StoreModel.find_store_by_name(name)
        if not store:
            return {"message": "No store with name {} found.".format(name)}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("delete from stores where name = ?",(store.name,))
        
        connection.commit()
        connection.close()
        return {'message': 'Store deleted'}

    def put(self,name):
        data = request.get_json()
        store = StoreModel.find_store_by_name(name)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if not store:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("insert into stores values (?)",(name,))
            if store.items:
                for data_item in data['items']:
                    item = ItemModel(data_item['name'],data_item['price'])
                    store.insert_item(item)

        for data_item in data['items']:
            item = ItemModel(data_item['name'],data_item['price'])
            item_upd = store.find_item_by_name(item.name)
            if item_upd:
                store.update_item(item_upd,item.price)
            else:
                store.insert_item(item)
        connection.commit()
        connection.close()

        return {"name": name,"items":[{"name": x['name'],"price": x['price']} for x in data['items']]}


class StoreList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select name from stores"
        rows = cursor.execute(query).fetchall()
        connection.close()
        return {'stores': [x[0] for x in rows]}


class Item(Resource):

    def get(self,store_name,item_name):
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message':'No store found with name '+store_name+'.'},404

        item = store.find_item_by_name(item_name)


        if not item:
            return {'message': "No items in store {} with name {}.".format(store_name,item_name)},404

        return {'name':item.name , 'price': item.price}


    def post(self,store_name,item_name):
        data = request.get_json()
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message':'No store found with name '+store_name+'.'},404

        if store.find_item_by_name(item_name):
            return {'message': "An item with name '{0}' already exists in store {1}".format(item_name,store_name)},400

        item = ItemModel(item_name,data['price'])
        new_item = store.insert_item(item)

        return new_item, 201


    def put(self,store_name,item_name):
        data = request.get_json()
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message':'No store found with name '+store_name+'.'},404

        if store.find_item_by_name(item_name):
            item = store.find_item_by_name(item_name)
            updated_item = store.update_item(item,data['price'])
            return updated_item, 201

        item = ItemModel(item_name,data['price'])
        new_item = store.insert_item(store_name)

        return new_item, 201


    def delete(self,store_name,item_name):
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message': "No store found with name '{}'".format(store_name)},404

        if not store.find_item_by_name(item_name):
            return {'message': "No item with name '{0}' found in store '{1}'".format(item_name,store_name)},404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("delete from items where store_name = ? and name = ?",(store_name,item_name))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self,name):
        store = StoreModel.find_store_by_name(name)
        if not store:
            return {'message': 'No store found with name '+name},404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item_query = "select * from items where store_name = ?"
        rows = cursor.execute(item_query,(name,)).fetchall()

        if not rows:
            return {"message": "No items found in store {}.".format(name)}

        return {'items': [{"name":x[0], "price": x[1]} for x in rows]}
