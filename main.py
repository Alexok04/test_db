import sqlite3
from flask import *

app = Flask(__name__)


def create_connection():
    conn = sqlite3.connect("my.db")
    conn.row_factory = sqlite3.Row

    return conn


def filling_db():
    conn = create_connection()
    curs = conn.cursor()

    curs.execute("DROP TABLE IF EXISTS cities")

    curs.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name_ VARCHAR(50), 
        population_ INTEGER, 
        description_ TEXT, 
        year_of_foundation DATE, 
        image_ VARCHAR(255)
    )
    """)
    curs.execute(
        "INSERT INTO cities (name_, population_, description_, year_of_foundation, image_) VALUES ('Одеса', 1000000, 'Перлина у моря', 1794, 'https://osama.com.ua/wp-content/uploads/2021/12/36.jpg')")
    curs.execute(
        "INSERT INTO cities (name_, population_, description_, year_of_foundation, image_) VALUES ('Київ', 3000000, 'Столиця України', 430, 'https://www.nta.ua/wp-content/uploads/2022/02/kyyiv.jpg')")

    curs.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER, username VARCHAR(50), login VARCHAR(50), password VARCHAR(50)) ")

    conn.commit()


@app.route("/")
def index():
    conn = create_connection()
    curs = conn.cursor()

    curs.execute("SELECT * FROM cities")
    sities = curs.fetchall()

    return render_template('index.html', sities=sities)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        conn = create_connection()
        curs = conn.cursor()

        username = request.form.get('username')
        login = request.form.get('login')
        password = request.form.get('password')

        curs.execute("INSERT INTO users (username) VALUES (?)", [username])

        curs.execute("INSERT INTO users (login) VALUES (?)", [login])

        curs.execute("INSERT INTO users (password) VALUES (?)", [password])

        conn.commit()

    return render_template('register.html')


@app.route("/users")
def user_view():
    conn = create_connection()
    curs = conn.cursor()

    curs.execute("SELECT * FROM users")
    users = curs.fetchall()

    return render_template('user.html', users=users)


app.run(debug=True)

