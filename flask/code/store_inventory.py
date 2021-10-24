from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Store(Resource):
    @classmethod
    def find_store_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        row = cursor.execute("select * from stores where name = ?",(name,)).fetchone()
        connection.close()
        return row


    @jwt_required()
    def get(self,name):
        row = self.find_store_by_name(name)
        if row:
            return {"store":{"name": row[0]}}
        return {"message": "No store with name {} found.".format(name)}


    def post(self,name):
        if self.find_store_by_name(name):
            return {'message': "Store with name {} already exists".format(name)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("insert into stores values (?)",(name,))

        connection.commit()
        connection.close()
        new_store = {'name': name, 'items':[]}
        return new_store, 201

    def delete(self,name):
        if not self.find_store_by_name(name):
            return {"message": "No store with name {} found.".format(name)}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("delete from stores where name = ?",(name,))
        
        connection.commit()
        connection.close()
        return {'message': 'Store deleted'}

    def put(self,name):
        data = request.get_json()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if not self.find_store_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("insert into stores values (?)",(name,))
            connection.commit()
            connection.close()

        return {"name": name}


class StoreList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select name from stores"
        rows = cursor.execute(query).fetchall()
        connection.close()
        return {'stores': [x[0] for x in rows]}


class Item(Resource):
    @classmethod
    def find_item_by_name_and_store_name(cls,store_name,item_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from items where store_name = ? and name = ?"
        row = cursor.execute(query,(store_name,item_name)).fetchone()
        connection.close()
        return row


    def get(self,store_name,item_name):
        if not Store.find_store_by_name(store_name):
            return {'message':'No store found with name '+store_name+'.'},404

        row = self.find_item_by_name_and_store_name(store_name,item_name)


        if not row:
            return {'message': "No items in store {} with name {}.".format(store_name,item_name)},404

        return {'name':row[0] , 'price': row[1]}


    def post(self,store_name,item_name):
        data = request.get_json()
        if not Store.find_store_by_name(store_name):
            return {'message':'No store found with name '+store_name+'.'},404

        if self.find_item_by_name_and_store_name(store_name,item_name):
            return {'message': "An item with name '{0}' already exists in store {1}".format(item_name,store_name)},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item_add_query = "insert into items values (?,?,?)"
        cursor.execute(item_add_query,(item_name,data['price'],store_name))
        connection.commit()
        connection.close()
        new_item = {'name':item_name,'price':data['price']}
        return new_item, 201


    def put(self,store_name,item_name):
        data = request.get_json()
        if not Store.find_store_by_name(store_name):
            return {'message':'No store found with name '+store_name+'.'},404

        if self.find_item_by_name_and_store_name(store_name,item_name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            item_upd_query = "update items set price = ? where name = ? and store_name = ?"
            cursor.execute(item_upd_query,(data['price'],item_name,store_name))
            connection.commit()
            connection.close()
            new_item = {'name':item_name,'price':data['price']}
            return new_item, 201

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item_add_query = "insert into items values (?,?,?)"
        cursor.execute(item_add_query,(item_name,data['price'],store_name))
        connection.commit()
        connection.close()
        new_item = {'name':item_name,'price':data['price']}
        return new_item, 201


    def delete(self,store_name,item_name):
        if not Store.find_store_by_name(store_name):
            return {'message': "No store found with name '{}'".format(store_name)},404

        if not self.find_item_by_name_and_store_name(store_name,item_name):
            return {'message': "No item with name '{0}' found in store '{1}'".format(item_name,store_name)},404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("delete from items where store_name = ? and name = ?",(store_name,item_name))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self,name):
        if not Store.find_store_by_name(name):
            return {'message': 'No store found with name '+name},404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item_query = "select * from items where store_name = ?"
        rows = cursor.execute(item_query,(name,)).fetchall()

        if not rows:
            return {"message": "No items found in store {}.".format(name)}

        return {'items': [{"name":x[0], "price": x[1]} for x in rows]}
