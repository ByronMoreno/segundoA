from flask import Flask, jsonify, render_template, request, redirect
from psycopg2 import connect, extras

#Instanciar la clase de flask
app = Flask(__name__)

#Contantes la base de datos
host = 'localhost'
port = 5432
dbname = 'byron'
username = 'postgres'
password = 123

#Funcion para conectar a la base de datos
def get_database():
    conn = connect(host=host, port=port, dbname=dbname, user=username, password=password)
    return conn

@app.route('/')
def index():
    #return 'Prueba de funcionamiento'
    return render_template('index.html')

#Consultar todos los usuarios
@app.get('/ap/users')
def get_users():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users")
    #Paso 4 sacar datos a pantalla
    user = cursor.fetchall()
    #Paso 5 convertir un objeto diccionario en un objeto json
    print(user)    
    return jsonify(user)

#Metodo es para html
#Consultar todos los usuarios
@app.route('/personas', methods=['GET'])
def get_users_html():
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users")
    #Paso 4 sacar datos a pantalla
    datos_consulta_select = cursor.fetchall()
    #Paso 5 enviar los datos de la consulta al html
    return render_template('select.html', usuarios=datos_consulta_select)

#Actualizar desde html
@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update_user_html(id):
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("select * from users where id = %s", (id,))
    #Paso 4 sacar datos a pantalla
    consultaPorId = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST': 
        nombre = request.form['nombre'] 
        edad = request.form['age']
        descripcion = request.form['description']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute("UPDATE users SET name=%s, age=%s, description=%s WHERE id=%s RETURNING *",
                    (nombre, edad, descripcion, id))
        #Paso 4 sacar datos a pantalla
        user_updating = cursor.fetchone()
        if user_updating:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/personas')
        #abort(404)
    return render_template('update.html', user=consultaPorId)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_user_html(id):
    #Paso 1, conectar a la base de datos
    conn = get_database()
    #Paso 2 definir el cursor
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    #Paso 3 enviar la sentencia sql al cursor
    cursor.execute("DELETE FROM users where id = %s RETURNING *", (id,))
    #Paso 4 sacar datos a pantalla
    user_deleting = cursor.fetchone()

    if request.method == 'POST': 
        
        if user_deleting:
            conn.commit()
            cursor.close()
            conn.close()
        return redirect('/personas')
        #abort(404)
    return render_template('delete.html', user=user_deleting)

#Crear desde html
@app.route('/crear', methods=['GET', 'POST'])
def crear_user_html():

    if request.method == 'GET':   
        return render_template('create.html')

    if request.method == 'POST': 
        nombre = request.form['nombre'] 
        edad = request.form['age']
        descripcion = request.form['description']
        #Conectar a la base de datos
        conn = get_database()
        #Paso 2 definir el cursor
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        #Paso 3 enviar la sentencia sql al cursor
        cursor.execute('INSERT INTO users(name,age,description) VALUES (%s,%s,%s) RETURNING *',
                (nombre, edad, descripcion))
        #Paso 4 sacar datos a pantalla
        user_creating = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/personas')
        #abort(404)
    

#Para colocar en modo debug, modo desarrallador
if __name__ == '__main__':
    app.run(debug=True)