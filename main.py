from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, User
from models import db, Class
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///introToSE.db'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        userName = request.form['userName']
        password = request.form['password']

        existing_user = User.query.filter(userName=userName, password=password).first()
        if existing_user == None:
            error = 'Incorrect Username/Password'
        else:
            flash("Logged in successfully!")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

        

def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
