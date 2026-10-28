from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'database.db'

# Функция для подключения к БД
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Позволяет обращаться к колонкам по имени
    return conn

# Инициализация базы данных (создание таблицы)
def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                date TEXT NOT NULL
            )
        ''')
        # Добавим тестовую запись
        conn.execute('''
            INSERT INTO posts (title, content, image, date) 
            VALUES (?, ?, ?, ?)
        ''', ('Запуск нового облачного сервиса', 'Мы рады сообщить о запуске нашего нового продукта...', 'post1.jpg', '28 Октября 2026'))
        conn.commit()
        conn.close()

# --- МАРШРУТЫ (Страницы сайта) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "Статья не найдена", 404
    return render_template('post.html', post=post)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.form['image'] # Название файла картинки
        date = "Сегодня" # Для простоты
        
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content, image, date) VALUES (?, ?, ?, ?)',
                     (title, content, image, date))
        conn.commit()
        conn.close()
        return redirect(url_for('blog'))
    
    return render_template('add_post.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)