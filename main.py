from flask import Flask, flash, render_template, request, redirect, url_for, session
from models import db, User, Class
import sqlite3
import random
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "INTRO_TO_SE_PROJECT_G4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///introToSE.db'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        userName = request.form['userName']
        password = request.form['password']

        existing_user = User.query.filter_by(userName=userName).first()
        if not existing_user or not check_password_hash(existing_user.password, password):
            error = 'Incorrect Username/Password'
        else:
            session['userId'] = existing_user.userId
            flash("Logged in successfully!")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():

    error = None

    if request.method == 'POST':

        while True:

            userId = random.randint(100000000, 999999999)
            exists = User.query.filter_by(userId=userId).first()
            if not exists:
                break

        userName = request.form['userName']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        isAdmin = 0

        userNameExists = User.query.filter_by(userName=userName).first()
        emailExists = User.query.filter_by(email=email).first()

        if not userNameExists and not emailExists:
            user = User(userId=userId, userName=userName, password=hashed_password, email=email, address=address,
                        city=city, state=state, zipCode=zipCode, isAdmin=isAdmin)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        
        elif userNameExists:
            error = 'Username already in use.'

        else:
            error = 'Account already exists with this email.'

    return render_template('createAccount.html', error=error)
        


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
