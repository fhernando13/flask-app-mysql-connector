from flask import Flask, render_template, request, url_for, redirect
from conexion import conectar
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute('select * from persona')
        data = cursor.fetchall()
        return render_template('index.html', personas = data)

@app.route("/agregar", methods=['POST'])
def agregar():
    if request.method == 'POST':
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                nombre = request.form['nombre']
                apellido = request.form['apellido']
                edad = request.form['edad']
                email = request.form['email']
                cursor.execute('insert into persona (nombre, apellido, edad, email) values (%s,%s,%s,%s)', (nombre, apellido, edad, email))
                conexion.commit()
                conexion.close()
        except Exception as e:
            conexion.rollback()
            conexion.close()
            return f'error: {e}'
        return redirect(url_for('index'))

@app.route('/eliminar/<string:id>')
def eliminar(id):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('delete from persona where id = {0}'.format(id))
            conexion.commit()
            conexion.close()
    except Exception as e:
        conexion.rollback()
        conexion.close()
        return f'error: {e}'
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    try: 
        conexion = conectar()
        with conexion.cursor() as cursor:
            cursor.execute('select * from persona where id = %s', (id,))
            data = cursor.fetchall()
            return render_template('editar.html', persona = data[0])
    except Exception as e:
        return f'error: {e}'

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                nombre = request.form['nombre']
                apellido = request.form['apellido']
                edad = request.form['edad']
                email = request.form['email']
                cursor.execute('UPDATE persona SET nombre = %s, apellido = %s, edad = %s, email = %s WHERE id = %s', (nombre, apellido, edad, email, id))
                conexion.commit()
                conexion.close()
        except Exception as e:
            conexion.rollback()
            conexion.close()
            return f'error: {e}'
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()