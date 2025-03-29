import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'
DATABASE = 'messi_store.db'

# Funciones de la base de datos
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        # Crear tablas
        db.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                es_admin BOOLEAN DEFAULT 0
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS Pregunta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                opcion1 TEXT NOT NULL,
                opcion2 TEXT NOT NULL,
                opcion3 TEXT NOT NULL,
                opcion4 TEXT NOT NULL,
                respuesta_correcta INTEGER NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS Resultado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                pregunta_id INTEGER NOT NULL,
                respuesta_usuario INTEGER NOT NULL,
                es_correcta BOOLEAN NOT NULL,
                fecha DATETIME NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
                FOREIGN KEY (pregunta_id) REFERENCES Pregunta(id)
            )
        ''')
        
        # Verificar si ya existen preguntas antes de insertar
        existing_questions = db.execute('SELECT COUNT(*) as count FROM Pregunta').fetchone()['count']
        if existing_questions == 0:
            db.execute('''
                INSERT INTO Pregunta (texto, opcion1, opcion2, opcion3, opcion4, respuesta_correcta) VALUES
                    ('¿En qué año debutó Messi con el FC Barcelona?', '2002', '2004', '2006', '2008', 2),
                    ('¿Cuántos Balones de Oro ha ganado Messi?', '5', '6', '7', '8', 4),
                    ('¿Con qué selección nacional juega Messi?', 'Brasil', 'Argentina', 'España', 'Portugal', 2),
                    ('¿En qué club jugó Messi antes de unirse al Inter Miami?', 'PSG', 'Manchester City', 'Bayern Munich', 'Juventus', 1),
                    ('¿Cuál es el número de camiseta más asociado con Messi?', '7', '9', '10', '11', 3),
                    ('¿En qué año ganó Messi la Copa América con Argentina?', '2019', '2020', '2021', '2022', 3),
                    ('¿Cuántos goles anotó Messi en su mejor temporada con el Barcelona?', '50', '60', '70', '80', 3),
                    ('¿Qué posición juega principalmente Messi?', 'Defensa', 'Mediocampista', 'Delantero', 'Portero', 3),
                    ('¿En qué ciudad nació Messi?', 'Buenos Aires', 'Rosario', 'Córdoba', 'Mendoza', 2),
                    ('¿Cuál es el nombre completo de Messi?', 'Lionel Andrés Messi', 'Lionel Alejandro Messi', 'Lionel Antonio Messi', 'Lionel Adrián Messi', 1),
                    ('¿Cuántos títulos de Liga ganó Messi con el Barcelona?', '7', '8', '9', '10', 4),
                    ('¿En qué año ganó Messi su primer Balón de Oro?', '2007', '2008', '2009', '2010', 3),
                    ('¿Cuál es el récord de goles de Messi en un año calendario?', '75', '80', '85', '91', 4),
                    ('¿Qué premio individual ganó Messi en 2022?', 'Balón de Oro', 'The Best FIFA', 'Bota de Oro', 'Todos los anteriores', 4),
                    ('¿Cuántas Champions League ha ganado Messi?', '3', '4', '5', '6', 2),
                    ('¿En qué año debutó Messi con la selección argentina?', '2003', '2004', '2005', '2006', 3),
                    ('¿Cuál es el apodo más común de Messi?', 'El Fenómeno', 'La Pulga', 'El Comandante', 'El Matador', 2),
                    ('¿Qué número de camiseta usa Messi en el Inter Miami?', '7', '9', '10', '11', 3),
                    ('¿Cuántos goles ha anotado Messi en su carrera?', 'Más de 600', 'Más de 700', 'Más de 800', 'Más de 900', 3),
                    ('¿En qué año ganó Messi el Mundial con Argentina?', '2018', '2020', '2022', '2023', 3);
            ''')
        
        # Crear usuario admin si no existe
        admin = db.execute('SELECT * FROM Usuario WHERE email = ?', ('admin@example.com',)).fetchone()
        if not admin:
            hashed_password = generate_password_hash('admin123')
            db.execute('INSERT INTO Usuario (email, password, es_admin) VALUES (?, ?, ?)',
                      ('admin@example.com', hashed_password, 1))
        db.commit()

# Funciones de autenticación
def login_user(email, password):
    db = get_db()
    user = db.execute('SELECT * FROM Usuario WHERE email = ?', (email,)).fetchone()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['es_admin'] = user['es_admin']
        return True
    return False

def logout_user():
    session.clear()

def current_user():
    if 'user_id' in session:
        return {
            'id': session['user_id'],
            'email': session['email'],
            'es_admin': session['es_admin'],
            'is_authenticated': True
        }
    return {'is_authenticated': False}

# Rutas principales
@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user()['is_authenticated']:
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        pregunta_id = request.form['pregunta_id']
        respuesta_usuario = int(request.form.get(f'respuesta_{pregunta_id}', 0))
        
        # Registrar la respuesta
        pregunta = db.execute('SELECT * FROM Pregunta WHERE id = ?', (pregunta_id,)).fetchone()
        es_correcta = respuesta_usuario == pregunta['respuesta_correcta']
        
        db.execute('INSERT INTO Resultado (usuario_id, pregunta_id, respuesta_usuario, es_correcta, fecha) VALUES (?, ?, ?, ?, ?)',
                  (current_user()['id'], pregunta_id, respuesta_usuario, es_correcta, datetime.now()))
        db.commit()
        
        # Incrementar el índice de la pregunta actual
        if 'pregunta_actual' in session:
            session['pregunta_actual'] += 1
        
        return redirect(url_for('index'))
    
    # Obtener todas las preguntas
    preguntas = db.execute('SELECT * FROM Pregunta').fetchall()
    
    # Obtener el índice de la pregunta actual desde la sesión
    if 'pregunta_actual' not in session:
        session['pregunta_actual'] = 0
    
    pregunta_actual = session['pregunta_actual']
    
    # Verificar si hay más preguntas
    if pregunta_actual >= len(preguntas):
        session.pop('pregunta_actual', None)  # Reiniciar el índice
        return render_template('index.html', preguntas=[], total_preguntas=len(preguntas))
    
    return render_template('index.html', preguntas=preguntas, pregunta_actual=pregunta_actual, total_preguntas=len(preguntas))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if login_user(email, password):
            flash('Inicio de sesión exitoso!')
            return redirect(url_for('index'))
        flash('Correo electrónico o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión')
    return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        db = get_db()
        try:
            db.execute('INSERT INTO Usuario (email, password) VALUES (?, ?)',
                      (email, hashed_password))
            db.commit()
            flash('Registro exitoso! Por favor inicia sesión.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El correo electrónico ya está en uso')
    return render_template('registro.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    user = current_user()
    if not user or not user['es_admin']:
        flash('Acceso denegado')
        return redirect(url_for('index'))
    
    db = get_db()
    if request.method == 'POST':
        # Verificar si es una eliminación
        if 'eliminar' in request.form:
            pregunta_id = request.form['eliminar']
            db.execute('DELETE FROM Pregunta WHERE id = ?', (pregunta_id,))
            db.commit()
            flash('Pregunta eliminada correctamente')
            return redirect(url_for('admin_panel'))
        
        # Verificar si es una edición
        if 'editar' in request.form:
            pregunta_id = request.form['editar']
            pregunta = db.execute('SELECT * FROM Pregunta WHERE id = ?', (pregunta_id,)).fetchone()
            return render_template('editar_pregunta.html', pregunta=pregunta)
        
        # Agregar nueva pregunta
        texto = request.form['texto']
        opcion1 = request.form['opcion1']
        opcion2 = request.form['opcion2']
        opcion3 = request.form['opcion3']
        opcion4 = request.form['opcion4']
        respuesta_correcta = int(request.form['respuesta_correcta'])
        db.execute('INSERT INTO Pregunta (texto, opcion1, opcion2, opcion3, opcion4, respuesta_correcta) VALUES (?, ?, ?, ?, ?, ?)',
                  (texto, opcion1, opcion2, opcion3, opcion4, respuesta_correcta))
        db.commit()
        flash('Pregunta agregada correctamente')
        return redirect(url_for('admin_panel'))
    
    preguntas = db.execute('SELECT * FROM Pregunta').fetchall()
    return render_template('admin.html', preguntas=preguntas)

@app.route('/editar_pregunta', methods=['POST'])
def editar_pregunta():
    user = current_user()
    if not user or not user['es_admin']:
        flash('Acceso denegado')
        return redirect(url_for('index'))
    
    db = get_db()
    pregunta_id = request.form['id']
    texto = request.form['texto']
    opcion1 = request.form['opcion1']
    opcion2 = request.form['opcion2']
    opcion3 = request.form['opcion3']
    opcion4 = request.form['opcion4']
    respuesta_correcta = int(request.form['respuesta_correcta'])
    
    db.execute('''UPDATE Pregunta SET 
                texto = ?, 
                opcion1 = ?, 
                opcion2 = ?, 
                opcion3 = ?, 
                opcion4 = ?, 
                respuesta_correcta = ? 
                WHERE id = ?''',
              (texto, opcion1, opcion2, opcion3, opcion4, respuesta_correcta, pregunta_id))
    db.commit()
    flash('Pregunta actualizada correctamente')
    return redirect(url_for('admin_panel'))

@app.route('/clasificacion')
def clasificacion():
    db = get_db()
    resultados = db.execute('''
        SELECT Usuario.email, COUNT(Resultado.id) AS total_respuestas, SUM(Resultado.es_correcta) AS respuestas_correctas
        FROM Usuario
        LEFT JOIN Resultado ON Usuario.id = Resultado.usuario_id
        GROUP BY Usuario.id
        ORDER BY respuestas_correctas DESC
    ''').fetchall()
    return render_template('clasificacion.html', resultados=resultados)

# Modificar la función current_user para que esté disponible en las plantillas
@app.context_processor
def inject_user():
    return dict(current_user=current_user())

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
