from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySqlConnection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'InventarioFDI'  # Cambiado a 'InventarioFDI'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM edificios')  # Cambiado a 'edificios'
    edificios = cursor.fetchall()
    return render_template('index.html', edificios=edificios)

@app.route('/add_edificio', methods=['POST'])
def add_edificio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO edificios (nombre, ubicacion) VALUES (%s, %s)',
                       (nombre, ubicacion))
        mysql.connection.commit()
        flash('Edificio Agregado Exitosamente')
        return redirect(url_for('Index'))

@app.route('/edit_edificio/<id>')
def get_edificio(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM edificios WHERE id_edificio = %s', (id,))
    edificio = cursor.fetchall()
    return render_template('edit_edificio.html', edificio=edificio[0])

@app.route('/update_edificio/<id>', methods=['POST'])
def update_edificio(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE edificios
                          SET nombre = %s, 
                              ubicacion = %s
                          WHERE id_edificio = %s""", (nombre, ubicacion, id))
        mysql.connection.commit()
        flash('Edificio Actualizado Exitosamente')
        return redirect(url_for('Index'))

@app.route('/delete_edificio/<string:id>')
def delete_edificio(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM edificios WHERE id_edificio = %s', (id,))
    mysql.connection.commit()
    flash('Edificio Eliminado Exitosamente')
    return redirect(url_for('Index'))

@app.route('/salones/<id>')
def salones(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM salones WHERE edificio_id = %s', (id,))  # Cambiado a 'edificio_id'
    salones = cursor.fetchall()
    return render_template('salones.html', salones=salones, edificio_id=id)

@app.route('/add_salon/<id>', methods=['POST'])
def add_salon(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        capacidad = request.form['capacidad']
        tipo = request.form['tipo']
        proyector = 'proyector' in request.form  # Checkbox
        ventilador = 'ventilador' in request.form  # Checkbox
        repetidor = 'repetidor' in request.form  # Checkbox
        sillas = request.form['sillas']
        escritorio = 'escritorio' in request.form  # Checkbox
        pantalla = 'pantalla' in request.form  # Checkbox
        pintarron = 'pintarron' in request.form  # Checkbox
        piso = request.form['piso']
        luces = 'luces' in request.form  # Checkbox
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO salones (edificio_id, nombre, capacidad, tipo, proyector, ventilador, repetidor, sillas, escritorio, pantalla, pintarron, piso, luces) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (id, nombre, capacidad, tipo, proyector, ventilador, repetidor, sillas, escritorio, pantalla, pintarron, piso, luces))
        mysql.connection.commit()
        flash('Salón Agregado Exitosamente')
        return redirect(url_for('salones', id=id))

@app.route('/edit_salon/<id>')
def get_salon(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM salones WHERE id_salon = %s', (id,))
    salon = cursor.fetchall()
    return render_template('edit_salon.html', salon=salon[0])

@app.route('/update_salon/<id>', methods=['POST'])
def update_salon(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        capacidad = request.form['capacidad']
        tipo = request.form['tipo']
        proyector = 'proyector' in request.form  # Checkbox
        ventilador = 'ventilador' in request.form  # Checkbox
        repetidor = 'repetidor' in request.form  # Checkbox
        sillas = request.form['sillas']
        escritorio = 'escritorio' in request.form  # Checkbox
        pantalla = 'pantalla' in request.form  # Checkbox
        pintarron = 'pintarron' in request.form  # Checkbox
        piso = request.form['piso']
        luces = 'luces' in request.form  # Checkbox
        
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE salones
                          SET nombre = %s, 
                              capacidad = %s,
                              tipo = %s,
                              proyector = %s,
                              ventilador = %s,
                              repetidor = %s,
                              sillas = %s,
                              escritorio = %s,
                              pantalla = %s,
                              pintarron = %s,
                              piso = %s,
                              luces = %s
                          WHERE id_salon = %s""", (nombre, capacidad, tipo, proyector, ventilador, repetidor, sillas, escritorio, pantalla, pintarron, piso, luces, id))
        mysql.connection.commit()
        flash('Salón Actualizado Exitosamente')
        return redirect(url_for('salones', id=id))

@app.route('/delete_salon/<string:id>')
def delete_salon(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM salones WHERE id_salon = %s', (id,))
    mysql.connection.commit()
    flash('Salón Eliminado Exitosamente')
    return redirect(url_for('salones', id=id))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
