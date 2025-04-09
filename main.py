from flask import Flask, flash, render_template, request, redirect, url_for, session
from models import db, User, Cart, Orders, Inventory, OrderItems
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import random
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "INTRO_TO_SE_PROJECT_G4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///introToSE.db'
db.init_app(app)

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
login.login_message = "Please log in to access this page."


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', user=current_user)
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        username = request.form['userName']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user or not check_password_hash(existing_user.password, password):
            error = 'Incorrect Username/Password'
        else:
            login_user(existing_user)
            flash("Logged in successfully!", 'success')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():

    error = None

    if request.method == 'POST':

        while True:

            userID = random.randint(100000000, 999999999)
            exists = User.query.filter_by(userID=userID).first()
            if not exists:
                break

        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if password != confirmPassword:
            error = 'Passwords do not match.'
            flash(error, 'error')
            return render_template('createAccount.html', error=error)
        hashed_password = generate_password_hash(password)
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        isAdmin = 0

        usernameExists = User.query.filter_by(username=username).first()
        emailExists = User.query.filter_by(email=email).first()

        if not usernameExists and not emailExists:
            user = User(userID=userID, username=username, password=hashed_password, email=email, address=address,
                        city=city, state=state, zipCode=zipCode, isAdmin=isAdmin)
            db.session.add(user)
            db.session.commit()
            flash('Successfully created account.', 'success')
            return redirect(url_for('login'))

        elif usernameExists:
            error = 'Username already in use.'

        else:
            error = 'Account already exists with this email.'

    return render_template('createAccount.html', error=error)


@app.route('/viewAccount', methods=['GET', 'POST'])
@login_required
def viewAccount():
    if current_user.is_authenticated:
        return render_template('viewAccount.html', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/deleteAccount', methods=['GET', 'POST'])
def deleteAccount():

    error = None
    user = User.query.get(session['userID'])

    if request.method == 'POST':
        if request.form.get('confirm') == 'Yes':
            if user.isAdmin:
                flash('Cannot delete admin account.', 'error')
                return redirect(url_for('home'))
            db.session.delete(user)
            db.session.commit()
            session.pop('userID', None)

            flash('Successfully deleted your account', 'success')
            return redirect(url_for('home'))
        else:
            flash("Cancelling deletion.", 'info')
            return redirect(url_for('home'))

    return render_template('deleteAccount.html', error=error)


@app.route('/editAccount', methods=['GET', 'POST'])
@login_required
def editAccount():
    if request.method == 'POST':
        # Update the currently logged-in user's account details
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        current_user.address = request.form['address']
        current_user.city = request.form['city']
        current_user.state = request.form['state']
        current_user.zipCode = request.form['zipCode']

        db.session.commit()
        flash("Account details updated successfully!", "success")
        return redirect(url_for('viewAccount'))

    # Render the edit account page with the current user's details
    return render_template('editAccount.html', user=current_user)

@app.route('/AddToCart', methods=['GET', 'POST'])
def AddToCart():
    error = None
    cart = Cart.query.get(session['cartID'])
    if request.method == 'POST':
        if request.form.get('confirm') == 'Save Changes':
            if User.isAdmin:
                flash('Cannot purchase items', 'error')
                return redirect(url_for('home'))
            else:
                
                cart.quantity += quantity
                db.session.commit()
                flash('added to cart successfully')
                return redirect(url_for('cart.html'))

        else:
            return redirect(url_for('home'))


@app.route('/Viewcart', methods=['GET', 'POST'])
def create_tables():
    with app.app_context():
        db.create_all()
        if User.query.filter_by(userID=0).first() is None:
            user = User(userID=0, username='admin', password=generate_password_hash('admin'), email='', address='',
                        city='', state='', zipCode='', isAdmin=1)
            db.session.add(user)
            db.session.commit()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
