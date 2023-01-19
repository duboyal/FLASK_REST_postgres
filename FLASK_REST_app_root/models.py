# app is visible form init filewhich is kinda weird but of 

# basically database models go here 

# from db import db
from app import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    
    # one to many relationship
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique = False, nullable = False) #!!! THIS IS WHAT LINKS IT

    store = db.relationship("StoreModel", back_populates = "items") # when we say my_item.store, it will be a store model object !
    # back populaates items is going to be used so that the storeModel class wiwll also have an items relationship here 
    # that allows each storemodel object to see very easily all of the items that are associated wwith it . 
    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "price" : self.price,
            "store_id" : self.store_id,
            "store" : self.store
            # "created_at" : str(self.created_at.strftime('%d-$m-%'))
            }


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(80), unique=True, nullable=False)

    

    items = db.relationship("ItemModel", back_populates="store")#, lazy = "dynamic") # will know thaat items is the other end of that relationship
    # and therefore to populate this variable go into items table find all the items that have store id equal to this stores id
    # forget bt lazy dynamic means wont fetch until we tell it to
    #could speed up your app but you need to 

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "items" : self.items
           
            }


'''
class Post(db.Model): #inherits from db.Model, and db in general, it inherits from sql alchemy class 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "created_at" : str(self.created_at.strftime('%d-$m-%'))

        }


'''
 