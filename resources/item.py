from flask_jwt import JWT, current_identity, jwt_required
from flask_restful import Api, Resource, reqparse
import sqlite3
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    #@jwt_required()
    def get(self, name):
        # broke
        # return {'item': next(filter(lambda x: x['name'] == name, items), None)}

        # woke 
        item = ItemModel.find_by_name(name) # Return ItemModel instance
        if item:
            return item.json()
        
        return {"message": "Item not found"}, 404
        
    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name=name, price=data['price'], store_id=data["store_id"])
        
        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {"message": "An error occured inserting the item."}, 500
        
        return item.json()

    def delete(self, name):

        # Bullshit global variabe method
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        
        # Weak db method
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name, ))
        # connection.commit()
        # connection.close()

        # Strong db 
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):

        # Parse data
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        if item is None:

            # Insert new item 
            item = ItemModel(name, data['price'], data["store_id"])

        else:

            item.price = data["price"]
        
        item.save_to_db()

        return item.json()

class ItemList(Resource):

    def get(self):

        # Return all items like a cool kid
        return {"items": [item.json() for item in ItemModel.query.all()]}
        
        # Lambda also works (Use when working with people programming in other languages)
        #return {"items": list(map(lambda x: x.json() ItemModel.query.all()))}
        
        # return them like a peasant
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = [] 

        # for row in result:

        #     items.append({
        #         "name": row[0],
        #         "price": row[1]
        #     })       

        # connection.close()

        # return {'items': items}