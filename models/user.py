import sqlite3
from db import db

class UserModel(db.Model):

    # Define db table
    __tablename__ = "users"

    # Column names
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) # 80 characters
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        
        self.username = username
        self.password = password

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):

        ## 
            # connection = sqlite3.connect("data.db")
            # cursor = connection.cursor()

            # query = "SELECT * FROM users WHERE username=?"
            # result = cursor.execute(query, (username,))
            # row = result.fetchone() 

            # if row:
            #     user = cls(*row) # *row = row[0], row[1], row[2]
            # else:
            #     user = None

            # connection.close()
            # return user
        ## 
        return cls.query.filter_by(username=username).first() 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() 
