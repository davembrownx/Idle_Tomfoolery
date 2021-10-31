from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.store_inventory import Store,StoreList,Item,ItemList

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity)


api.add_resource(Store,'/<string:name>')
api.add_resource(StoreList,'/')
api.add_resource(Item,'/<string:store_name>/item/<string:item_name>')
api.add_resource(ItemList,'/<string:name>/items')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
