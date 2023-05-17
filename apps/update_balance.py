from flask import Flask
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


app.run(host='0.0.0.0', port=81)
