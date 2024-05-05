from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'proyectoFinalDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'tu_clave_secreta'

mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('¡Registro exitoso! Por favor inicia sesión.')
        return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM usuarios WHERE username = %s", [username])

        if result > 0:
            usuario = cur.fetchone()
            if check_password_hash(usuario['password'], password):
                user = User(usuario['id'])
                login_user(user)
                flash('¡Inicio de sesión exitoso!')

                # Obtener la lista de usuarios registrados
                cur.execute("SELECT username FROM usuarios")
                usuarios_registrados = cur.fetchall()

                return render_template('usuarios.html', usuarios=usuarios_registrados)
            else:
                flash('Contraseña incorrecta. Por favor, inténtalo de nuevo.')
        else:
            flash('Usuario no encontrado. Por favor, regístrate.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Sesión cerrada correctamente!')
    return redirect(url_for('index'))


@app.route('/usuarios')
@login_required
def usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM usuarios")
    usuarios_registrados = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=usuarios_registrados)

@app.route('/chat/<destinatario>', methods=['GET', 'POST'])
@login_required
def chat(destinatario):
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        remitente_id = current_user.id
        
        # Obtener el nombre de usuario del remitente
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM usuarios WHERE id = %s", (remitente_id,))
        remitente = cur.fetchone()['username']
        cur.close()
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO mensajes_chat (remitente, destinatario, mensaje) VALUES (%s, %s, %s)", (remitente_id, destinatario, mensaje))
            mysql.connection.commit()
            cur.close()
            return jsonify({'status': 'success', 'remitente': remitente})  # Enviar una respuesta JSON indicando éxito y el nombre de usuario del remitente
        except Exception as e:
            flash(f'Error al enviar el mensaje: {str(e)}')

    return render_template('chat.html', destinatario=destinatario)





if __name__ == '__main__':
    app.run(debug=True)
