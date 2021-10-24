import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = "select * from users where username = ?"
        result = cursor.execute(select_query,(name,))

        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = "select * from users where id = ?"
        result = cursor.execute(select_query,(_id,))

        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="This field is required.")
    parser.add_argument('password',type=str,required=True,help="This field is required.")
    def post(self):
        data = UserRegister.parser.parse_args()
        user_already_exists = User.find_by_username(data['username'])
        if user_already_exists:
            return {'message': "A user with name {} already exists".format(data['username'])},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into users values (null,?,?)"
        cursor.execute(query, (data['username'],data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User successfully created'}, 201
