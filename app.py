from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/projectFit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=False)

    def __init__(self, nombre, precio, stock, imagen, activo=False):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.activo = activo

class Programa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=False)

    def __init__(self, nombre, precio, imagen, activo=False):
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen
        self.activo = activo

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return f'App Web para registrar nombres de productos'

# Crear un registro en la tabla Productos
@app.route("/registro", methods=['POST'])
def registro():
    nombre_recibido = request.json["nombre"]
    precio = request.json['precio']
    stock = request.json['stock']
    imagen = request.json['imagen']
    activo = request.json.get('activo', False)
    nuevo_registro = Producto(nombre_recibido, precio, stock, imagen, activo)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud de post recibida"

# Retornar todos los registros en un Json
@app.route("/productos", methods=['GET'])
def productos():
    all_registros = Producto.query.all()
    data_serializada = []

    for objeto in all_registros:
        data_serializada.append({"id": objeto.id, "nombre": objeto.nombre, "precio": objeto.precio, "stock": objeto.stock, "imagen": objeto.imagen, "activo": objeto.activo})

    return jsonify(data_serializada)


@app.route('/update/<id>', methods=['PUT'])
def update(id):
    producto = Producto.query.get(id)

    nombre = request.json["nombre"]
    precio = request.json['precio']
    stock = request.json['stock']
    imagen = request.json['imagen']
    activo = request.json.get('activo', False)

    producto.nombre = nombre
    producto.precio = precio
    producto.stock = stock
    producto.imagen = imagen
    producto.activo = activo
    db.session.commit()

    data_serializada = [{"id": producto.id, "nombre": producto.nombre, "precio": producto.precio, "stock": producto.stock, "imagen": producto.imagen, "activo": producto.activo}]

    return jsonify(data_serializada)


@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()

    data_serializada = [{"id": producto.id, "nombre": producto.nombre, "precio": producto.precio, "stock": producto.stock, "imagen": producto.imagen, "activo": producto.activo}]

    return jsonify(data_serializada)

@app.route('/activar-desactivar/<id>', methods=['PUT'])
def activar_desactivar_producto(id):
    try:
        producto = Producto.query.get(id)

        if producto:
            producto.activo = not producto.activo
            db.session.commit()

            return jsonify({'mensaje': f'Estado actualizado para el producto con ID {id}'}), 200
        else:
            return jsonify({'mensaje': f'Producto con ID {id} no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#PROGRAMAS

# Retornar todos los registros de Programas en JSON
@app.route("/programas", methods=['GET'])
def programas():
    all_registros = Programa.query.all()
    data_serializada = []

    for objeto in all_registros:
        data_serializada.append({"id": objeto.id, "nombre": objeto.nombre, "precio": objeto.precio, "imagen": objeto.imagen, "activo": objeto.activo})

    return jsonify(data_serializada)

# Crear un registro en la tabla Programas
@app.route("/registro-programa", methods=['POST'])
def registro_programa():
    nombre_recibido = request.json["nombre"]
    precio = request.json['precio']
    imagen = request.json['imagen']
    activo = request.json.get('activo', False)
    nuevo_registro = Programa(nombre_recibido, precio, imagen, activo)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud de post de programa recibida"

# Actualizar un registro de la tabla Programas
@app.route('/update-programa/<id>', methods=['PUT'])
def update_programa(id):
    programa = Programa.query.get(id)

    nombre = request.json["nombre"]
    precio = request.json['precio']
    imagen = request.json['imagen']
    activo = request.json.get('activo', False)

    programa.nombre = nombre
    programa.precio = precio
    programa.imagen = imagen
    programa.activo = activo
    db.session.commit()

    data_serializada = [{"id": programa.id, "nombre": programa.nombre, "precio": programa.precio, "imagen": programa.imagen, "activo": programa.activo}]

    return jsonify(data_serializada)

@app.route('/borrar-programa/<id>', methods=['DELETE'])
def borrar_programa(id):
    programa = Programa.query.get(id)
    db.session.delete(programa)
    db.session.commit()

    data_serializada = [{"id": programa.id, "nombre": programa.nombre, "precio": programa.precio, "imagen": programa.imagen, "activo": programa.activo}]

    return jsonify(data_serializada)

@app.route('/activar-desactivar-programa/<id>', methods=['PUT'])
def activar_desactivar_programa(id):
    try:
        programa = Programa.query.get(id)

        if programa:
            programa.activo = not programa.activo
            db.session.commit()

            return jsonify({'mensaje': f'Estado actualizado para el programa con ID {id}'}), 200
        else:
            return jsonify({'mensaje': f'Programa con ID {id} no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
