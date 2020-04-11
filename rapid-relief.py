import sqlite3

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anything'

login_manager = LoginManager()
login_manager.init_app(app)

con = sqlite3.connect('customer.db')
con.execute("create table if not exists Customer (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")

@login_manager.user_loader
def load_user(id):
    con = sqlite3.connect('customer.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from Customer where id=?", [int(id)])
    user = cur.fetchone()
    return user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password2 = request.form['password2']
            
            if password == password2:
                with sqlite3.connect('customer.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT into Customer (username, email, password) values (?, ?, ?)", (username, email, password))
                    con.commit()
                flash("You are registered user")
                return redirect(url_for('login'))
            else:
                flash("password and repeat password should be same")
                return render_template('register.html')
        except:
            flash("Username and email should be unique")
            con.rollback()
            return render_template('register.html')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']

            con = sqlite3.connect('customer.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT password from Customer where username=?", username)
            row = cur.fetchone()

            if password == row['password']:
                session['logged_in'] = True
                login_user(username)
                flash("hello {}".format(username))
                return redirect(url_for('index'))
            else:
                flash("Invalid username and password")
                return render_template('login.html')
        except:
            flash("Invalid username and password")
            return render_template('login.html')
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)