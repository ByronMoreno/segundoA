from flask import Flask, jsonify, render_template
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

#Para colocar en modo debug, modo desarrallador
if __name__ == '__main__':
    app.run(debug=True)