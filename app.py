from sys import set_coroutine_origin_tracking_depth
from flask import Flask, request, session
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import bcrypt
import jwt
import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://proyectodist:ADMIN2233@db4free.net:3306/proyectodist'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u276789818_distribuidora:HostCami2021@212.1.208.1:3306/u276789818_distHostinger'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key = 'appLogin'
db = SQLAlchemy(app)
ma = Marshmallow(app)

semilla = bcrypt.gensalt()


class Productos(db.Model):
    idproductos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    familia = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)


    def __init__(self,idproductos ,nombre, familia, stock, precio):
        self.idproductos = idproductos
        self.nombre = nombre
        self.familia = familia
        self.stock = stock
        self.precio = precio
    
    def __init__(self ,nombre, familia, stock, precio):
        self.nombre = nombre
        self.familia = familia
        self.stock = stock
        self.precio = precio



class ProductosSchema(ma.Schema):
    class Meta:
        fields = ('idproductos','nombre', 'familia', 'stock', 'precio')

class NewProductosSchema(ma.Schema):
    class Meta:
        fields = ('nombre', 'familia', 'stock', 'precio')

class ProductosVendidos(ma.Schema):
    class Meta:
        fields = ('nombre', 'familia', 'cantidad')


producto_schema = ProductosSchema()
productoNew_schema = NewProductosSchema()
productos_schema = ProductosSchema(many=True)
productosVendidos_schema = ProductosVendidos(many=True)


class Clientes(db.Model):
    idclientes = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    cuit = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(50), nullable=False)
    zona = db.Column(db.String(50), nullable=False)

    def __init__(self, idclientes,nombre, direccion, cuit, telefono, zona):
        self.idclientes = idclientes
        self.nombre = nombre
        self.direccion = direccion
        self.cuit = cuit
        self.telefono = telefono
        self.zona = zona

    def __init__(self,nombre, direccion, cuit, telefono, zona):
        self.nombre = nombre
        self.direccion = direccion
        self.cuit = cuit
        self.telefono = telefono
        self.zona = zona

class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('idclientes','nombre', 'direccion', 'cuit', 'telefono', 'zona')

class NewClientesSchema(ma.Schema):
    class Meta:
        fields = ('nombre', 'direccion', 'cuit', 'telefono', 'zona')

cliente_schema = ClientesSchema()
clientesNew_schema = NewClientesSchema()
clientes_schema = ClientesSchema(many=True)


class Usuarios(db.Model):
    idusuarios = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol

    def __init__(self, idusuarios, username, password, rol):
        self.idusuarios = idusuarios
        self.username = username
        self.password = password
        self.rol = rol

class UsuariosSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password', 'rol', 'token', 'status')

class UsuariosIDSchema(ma.Schema):
    class Meta:
        fields = ('idusuarios', 'username', 'password', 'rol', 'token', 'status')

user_schema = UsuariosSchema()
userID_schema = UsuariosIDSchema()
usersID_schema = UsuariosIDSchema(many=True)



class Pedidos(db.Model):
    idpedidos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idclientes = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    idusuario = db.Column(db.Integer, primary_key=True)

    def __init__(self, idpedidos, idclientes, nombre, fecha, total, idusuario):
        self.idpedidos = idpedidos
        self.idclientes = idclientes
        self.nombre = nombre
        self.fecha = fecha
        self.total = total
        self.idusuario = idusuario

    def __init__(self, idclientes, nombre, fecha, total, idusuario):
        self.idclientes = idclientes
        self.nombre = nombre
        self.fecha = fecha
        self.total = total
        self.idusuario = idusuario

class PedidosSchema(ma.Schema):
    class Meta:
        fields = ('idclientes', 'nombre', 'fecha', 'total', 'idusuario')

class PedidosIDSchema(ma.Schema):
    class Meta:
        fields = ('idpedidos', 'idclientes', 'nombre', 'fecha', 'total', 'idusuario')

pedido_schema = PedidosSchema()
pedidoID_schema = PedidosIDSchema()
pedidos_schema = PedidosIDSchema(many=True)


class Pedido_productos(db.Model):
    idpedido = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unidad = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    familia = db.Column(db.String(100), nullable=False)

    def __init__(self, idpedido, idproducto, cantidad, precio_unidad, nombre, familia):
        self.idpedido = idpedido
        self.idproducto = idproducto
        self.cantidad = cantidad
        self.precio_unidad = precio_unidad
        self.nombre = nombre
        self.familia = familia
       

class PedidosProdSchema(ma.Schema):
    class Meta:
        fields = ('idpedido', 'idproducto', 'cantidad', 'precio_unidad', 'nombre', 'familia')

pedidoprod_schema = PedidosProdSchema()
pedidoprodtos_schema = PedidosProdSchema(many=True)

    
@app.route('/registrar',methods = ['POST'])
def registrar():
    username = request.json['username']
    password = request.json['password']
    rol = request.json['rol']

    newUsername = Usuarios.query.filter_by(username = username).first()
    if newUsername != None:
        return "Este usuario ya esta registrado"
    else:
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode,semilla)

        newUser = Usuarios(username,password_encriptado,rol)
        db.session.add(newUser)
        db.session.commit()

        print(username)
        print(password)
        print(rol)
        print(password_encriptado)
        return user_schema.jsonify(newUser)

@app.route('/login',methods = ['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    password_encode = password.encode("utf-8")

    newUser = Usuarios.query.filter_by(username = username).first()
    if newUser != None:
        password_encriptado_encode = newUser.password.encode()
        if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
            token = jwt.encode({'public_id': newUser.idusuarios, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
            session['nombre']=username
            session['rol']=newUser.rol
            newUser.token = token
            newUser.status = 1
            return user_schema.jsonify(newUser)
        else:
            return user_schema.jsonify({'password': "", 'rol': "", 'token': "", 'username': "Contraseña Incorrecta", 'status': 0 })
            # return error_response("Contraseña Incorrecta")
    else:
        return user_schema.jsonify({'password': "", 'rol': "", 'token': "", 'username': "El usuario no esta registrado", 'status': 2 })
    
@app.route('/getIdUsuario/<username>',methods = ['GET'])
def get_usuario(username):
    user = Usuarios.query.filter_by(username = username).first()
    results = userID_schema.dump(user)
    return jsonify(results)

@app.route('/getProductos',methods = ['GET'])
def get_productos():
    try: 
        all_productos = Productos.query.all()
        results = productos_schema.dump(all_productos)
        return jsonify(results)
    except Exception as ee:
        print(ee)

   
@app.route('/getProductosDelPedido/<id>',methods = ['GET'])
def get_productosDelPedido(id):
    all_productos = Pedido_productos.query.filter_by(idpedido = id)
    results = pedidoprodtos_schema.dump(all_productos)
    return jsonify(results) 

@app.route('/getPedidos',methods = ['GET'])
def get_pedidos():
    all_pedidos =  Pedidos.query.all()
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)

@app.route('/getPedido/<idusuario>',methods = ['GET'])
def get_pedidosdelempleado(idusuario):
    all_pedidos = Pedidos.query.filter_by(idusuario = idusuario).all()
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)

@app.route('/getEmpleados',methods = ['GET'])
def get_empleados():
    all_empleados = Usuarios.query.filter_by(rol = 'EMPLEADO').all()
    results = usersID_schema.dump(all_empleados)
    return jsonify(results)

@app.route('/getProductos/<id>/',methods = ['GET'])
def get_onlyOne(id):
    producto = Productos.query.get(id)
    return producto_schema.jsonify(producto)


@app.route('/addProducto',methods = ['POST'])
def add_producto():
    print(request)
    nombre = request.json['nombre']
    familia = request.json['familia']
    stock = request.json['stock']
    precio = request.json['precio']

    prod = Productos(nombre,familia,stock,precio)
    db.session.add(prod)
    db.session.commit()
    return productoNew_schema.jsonify(prod)

@app.route('/updateProd/<id>/',methods = ['PUT'])
def update_prod(id):
    prod = Productos.query.get(id)

    stock = request.json['stock']
    precio = request.json['precio']
    
    prod.stock = stock
    prod.precio = precio

    db.session.commit()
    return producto_schema.jsonify(prod)

def update_stockProduct(id,stock):
    prod = Productos.query.get(id)

    prod.stock = stock

    db.session.commit()
    return producto_schema.jsonify(prod)

@app.route('/deleteProd/<id>/',methods = ['DELETE'])
def delete_prod(id):
    prod = Productos.query.get(id)
    db.session.delete(prod)
    db.session.commit()

    return producto_schema.jsonify(prod)

@app.route('/deleteCli/<id>/',methods = ['DELETE'])
def delete_cli(id):
    clien = Clientes.query.get(id)
    db.session.delete(clien)
    db.session.commit()

    return cliente_schema.jsonify(clien)


@app.route('/getClientes',methods = ['GET'])
def get_clientes():
    all_clientes = Clientes.query.all()
    results = clientes_schema.dump(all_clientes)
    return jsonify(results)

@app.route('/getClientes/<id>',methods = ['GET'])
def get_clienteOnlyOne(id):
    cliente = Clientes.query.get(id)
    results = cliente_schema.dump(cliente)
    return jsonify(results)

@app.route('/addCliente',methods = ['POST'])
def add_cliente():
    print(request)
    nombre = request.json['nombre']
    direccion = request.json['direccion']
    cuit = request.json['cuit']
    telefono = request.json['telefono']
    zona = request.json['zona']

    cli = Clientes(nombre,direccion,cuit,telefono,zona)
    db.session.add(cli)
    db.session.commit()
    return clientesNew_schema.jsonify(cli)

@app.route('/addPedido',methods = ['POST'])
def add_pedido():
    idclientes = request.json['idcliente']
    cli = get_clienteOnlyOne(idclientes)
    nombre = cli.json['nombre'] +" "+request.json['fecha']
 
    idusuario = get_usuario(request.json['usuario']).json['idusuarios']

    fecha = request.json['fecha']
    total = request.json['total']
    listaProd = request.json['productos']
    pedido = Pedidos(idclientes,nombre,fecha,total,idusuario)
    db.session.add(pedido)
    db.session.commit()
    idpedido = pedidoID_schema.jsonify(pedido).json['idpedidos']
    
    for x in listaProd:
        cantidad = x['cantidad']
        idproducto = x['idproductos']
        precio_unidad = x['precio']
        nombre = x['nombre']
        familia = x['familia']
        producto = Pedido_productos(idpedido,idproducto,cantidad,precio_unidad,nombre,familia)
        db.session.add(producto)
        db.session.commit()
    
    for x in listaProd:
        idproducto = x['idproductos']
        oldStock = get_onlyOne(idproducto)
        newStock = oldStock.json['stock'] - x['cantidad']
        print(newStock)
        update_stockProduct(idproducto,newStock)

    return pedido_schema.jsonify(pedido)

@app.route('/getPedidoPorFecha/<idusuario>/<fecha>',methods = ['GET'])
def get_pedidosPorFecha(idusuario,fecha):
    all_pedidos = Pedidos.query.filter_by(idusuario = idusuario, fecha = fecha).all()
    results = pedidos_schema.dump(all_pedidos)
    return jsonify(results)


@app.route('/getProdVendidosPorFecha/<fecha>',methods = ['GET'])
def getProductosVendidosPorFecha(fecha):
    all_productos = db.session.query(Productos.nombre, Productos.familia, db.func.sum(Pedido_productos.cantidad).label("cantidad")).select_from(Productos).join(Pedido_productos, Productos.idproductos == Pedido_productos.idproducto).join(Pedidos, Pedido_productos.idpedido == Pedidos.idpedidos).filter_by(fecha = fecha).group_by(Productos.idproductos).all()
    results = productosVendidos_schema.dump(all_productos)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)