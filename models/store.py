from db import db


class StoreModel(db.Model):   #ItemModel is our internal representation . So, it also has to contain properties of an item as object properties.

    __tablename__='stores'

    id = db.Column(db.Integer , primary_key=True)  #it will pump all these column in to __init__ method and will create object of them
    name= db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy='dynamic')   #after adding lazy='dynamic' it becomes a query builder and items is no longer a list

    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()   #SELECT * FROM items WHERE name=name


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()   #here session is the collection of object  that we  are going to write to the database

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
