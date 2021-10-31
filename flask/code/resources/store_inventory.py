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
        data = request.get_json()
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'message': "Store with name {} already exists".format(name)}, 400

        store = StoreModel(name,[ItemModel(x['name'],x['price'],name) for x in data['items']])
        store.upsert_store()
        new_store = {'name': store.name, 'items':[{"name": x.name, "price": x.price} for x in store.items]}
        return new_store, 201

    def delete(self,name):
        store = StoreModel.find_store_by_name(name)
        if not store:
            return {"message": "No store with name {} found.".format(name)}
        
        store.delete_store()

        return {'message': 'Store deleted'}

    def put(self,name):
        data = request.get_json()
        store = StoreModel.find_store_by_name(name)
        if not store:
            store = StoreModel(name,[ItemModel(x['name'],x['price'],name) for x in data['items']])
        else:
            for item in [ItemModel(x['name'],x['price'],name) for x in data['items']]:
                item_found = store.find_item_by_name(item.name)
                if item_found:
                    item_found.price = item.price
                    store.upsert_item_in_store(item_found)
                else:
                    store.upsert_item_in_store(item)
        store.upsert_store()

        return {"name": store.name,"items":[{"name": x['name'],"price": x['price']} for x in data['items']]}


class StoreList(Resource):
    def get(self):
        rows = StoreModel.find_stores()
        return {'stores': [x.name for x in rows]}


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

        item = ItemModel(item_name,data['price'],store_name)
        new_item = store.upsert_item_in_store(item)

        new_item = {"name": item.name,"price": item.price}
        return new_item, 201


    def put(self,store_name,item_name):
        data = request.get_json()
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message':'No store found with name '+store_name+'.'},404

        if store.find_item_by_name(item_name):
            item = store.find_item_by_name(item_name)
            item.price = data['price']
            updated_item = store.upsert_item_in_store(item)
            return updated_item, 201

        item = ItemModel(item_name,data['price'],store_name)
        store.upsert_item_in_store(item)

        new_item = {"name": item.name,"price": item.price}
        return new_item, 201


    def delete(self,store_name,item_name):
        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return {'message': "No store found with name '{}'".format(store_name)},404

        item = store.find_item_by_name(item_name)
        if not item:
            return {'message': "No item with name '{0}' found in store '{1}'".format(item_name,store_name)},404

        store.delete_item_from_store(item)

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self,name):
        store = StoreModel.find_store_by_name(name)
        if not store:
            return {'message': 'No store found with name '+name},404

        rows = store.find_items()

        if not rows:
            return {"message": "No items found in store {}.".format(name)}

        return {'items': [{"name":x.name, "price": x.price} for x in rows]}
