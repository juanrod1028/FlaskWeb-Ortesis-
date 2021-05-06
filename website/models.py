from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    productos = db.relationship('Producto')
    budget = db.Column(db.Integer(), nullable=False, default=0)
    #carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'))    

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.precio
    

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    categoria = db.Column(db.String(255), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vDonacion = db.Column(db.Integer)

    def buy(self, user):
        self.user = user.id
        user.budget -= self.precio
        db.session.commit()
        
    def donar(self, user):
        self.user = user.id
        user.budget += self.precio
        db.session.commit()
   
class MiProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    categoria = db.Column(db.String(255), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vDonacion = db.Column(db.Integer)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
