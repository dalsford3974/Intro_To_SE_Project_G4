from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, User
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///introToSE.db'
app.secret_key = 'test'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        userNameForm = request.form.get('userName')
        passwordForm = request.form.get('password')

        dataUser = db.session.execute(db.text("SELECT * FROM users WHERE password=:passwordForm AND userName=:userNameForm"),  {"passwordForm": passwordForm, "userNameForm": userNameForm}).fetchone()

        #dataPass = db.session.execute(db.text("SELECT * FROM users WHERE password=:passwordForm"), {"passwordForm": passwordForm}).fetchone()
        #dataTest = db.session.execute(db.text("SELECT * FROM users WHERE userName=:userNameForm"), {"userNameForm": userNameForm}).fetchone()

        #print(dataPass)
        #print(dataTest)

        #print(userNameForm)
        #print(passwordForm)

        #print(dataUser)

        if dataUser == None:
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
