import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from datetime import timedelta

# local
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///data.db") #"postgresql://wrgmusxmocfrli:a8667ac025befb8a8270a0c1188f106ebe3cf755ba16a18f9a2318d865696df1@ec2-18-202-1-222.eu-west-1.compute.amazonaws.com:5432/ddhhq76qmtaunp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
api = Api(app)

# JSON Web token
jwt = JWT(app, authenticate, identity)

# Add resources to app
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")


if __name__ == '__main__':

    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
