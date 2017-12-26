
from db import db


class ItemModel(db.Model):   #ItemModel is our internal representation . So, it also has to contain properties of an item as object properties.

    __tablename__='items'

    id = db.Column(db.Integer , primary_key=True)  #it will pump all these column in to __init__ method and will create object of them
    name= db.Column(db.String(80))
    price=db.Column(db.Float(precision=2))

    store_id  = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name, price, store_id):
        self.name=name
        self.price=price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()   #SELECT * FROM items WHERE name=name


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()   #here session is the collection of object  that we  are going to write to the database

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
