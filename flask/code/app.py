from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from store_inventory import Store,StoreList,Item,ItemList

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app,authenticate,identity)

#stores = [{'name':'Dave\'s Awesome Store',
#           'items':[{'name':'Chicken Shoes',
#                     'price': 18.99},
#                    {'name':'Dog Polish',
#                     'price': 4.99}
#                   ]
#           },
#           {'name': 'Dave\'s Garden of Earthly Delights',
#            'items': [{'name': 'Trout Soother',
#                       'price': 6.99},
#                      {'name': 'Tooth Extractor',
#                       'price': 15.99}
#                     ]
#            },
#            {'name': 'Dave', 'items':[]}
#           ]


api.add_resource(Store,'/<string:name>')
api.add_resource(StoreList,'/')
api.add_resource(Item,'/<string:store_name>/item/<string:item_name>')
api.add_resource(ItemList,'/<string:name>/items')
api.add_resource(UserRegister,'/register')

app.run(debug=True)
