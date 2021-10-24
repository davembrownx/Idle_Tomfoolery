from flask import Flask, jsonify,request,render_template

app  = Flask(__name__)

stores = [{'name': 'Dave\'s Awesome Store',
           'items': [{'name': 'Dog Polish', 'price': 4.99}]
          },
          {'name': 'Dave\'s Garden of Earthly Pleasures',
           'items': [{'name': 'Trout Shoes', 'price': 18.99}]
          }
         ]

@app.route('/')
def home():
    return render_template('Store_Info.html')

@app.route('/store',methods=['POST'])
def create_store():
    request_dict = request.get_json()
    new_store = {'name': request_dict['name'],
                 'items': []
                }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'Error': 'No store found with name '+name})

app.route('store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            new_item = {'name': request_dict['name'],
                        'price': request_dict['price']
                       }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'Error': 'No store found with name '+name})

@app.route('/store/<string:name>/<string:item_name>')
def get_item_in_store(name,item_name):
    for store in stores:
        if store['name'] == name:
            for item in store['items']:
                if item['name'] == item_name:
                    return jsonify(item)
            return jsonify({'Error': 'No item with name '+item_name+' found in store '+name})
    return jsonify({'Error': 'No store found with name '+name})

app.run(port=5000)
