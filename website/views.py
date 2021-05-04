from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Producto, MiProducto
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/donaciones', methods=['GET', 'POST'])
def donaciones():
    if request.method == 'POST':

        nombre = request.form.get('nombre')
        imagen = request.form.get('imagen')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        user_id=current_user.id
        if categoria=="1" :
         precio = 1000
        elif categoria=="2":
         precio=2000
        elif categoria=="3":
         precio=3000
        elif categoria=="4":
         precio=4000 

        
        new_producto = Producto( nombre = nombre,imagen = imagen, descripcion = descripcion, categoria = categoria, precio = precio,user_id=user_id)
        new_miproducto = MiProducto( nombre = nombre,imagen = imagen, descripcion = descripcion, categoria = categoria, precio = precio,user_id=user_id)
        db.session.add(new_producto)
        db.session.add(new_miproducto)
        db.session.commit()
        flash('Producto creado!', category='success')
    
    return render_template("donaciones.html", user=current_user)

@views.route('/misdonaciones', methods=['GET', 'POST'])
def misdonaciones():
    if request.method == 'GET':
        
        nombres=db.session.query(MiProducto.nombre).filter_by(user_id=current_user.id)
        descripciones=db.session.query(MiProducto.descripcion).filter_by(user_id=current_user.id)
        imagenes=db.session.query(MiProducto.imagen).filter_by(user_id=current_user.id)
        categorias=db.session.query(MiProducto.categoria).filter_by(user_id=current_user.id)
        cantidad=db.session.query(MiProducto.nombre).filter_by(user_id=current_user.id).count()


        flash('Tus productos donados', category='success')
    
    return render_template("misdonaciones.html", user=current_user,nombres=nombres,descripciones=descripciones,imagenes=imagenes,categorias=categorias,cantidad=cantidad)
    
@views.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    if request.method == 'GET':
        id = db.session.query(Producto.id)
        nombres=db.session.query(Producto.nombre)
        descripciones=db.session.query(Producto.descripcion)
        imagenes=db.session.query(Producto.imagen)
        categorias=db.session.query(Producto.categoria)
        cantidad=db.session.query(Producto.nombre).count()
        valor = db.session.query(Producto.precio)

        flash('Todos los productos', category='success')
    

    if request.method == 'POST':

        id = db.session.query(Producto.nombre)
        print(id)
        return redirect(url_for('views.carrito'))

        
    return render_template("catalogo.html", user=current_user,nombres=nombres,descripciones=descripciones,imagenes=imagenes,categorias=categorias,cantidad=cantidad,precios=valor)

@views.route('/carrito', methods=['GET', 'POST'])
def carrito():
    

    

    return render_template("carrito.html",user=current_user)
