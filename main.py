from flask import Flask, flash, render_template, request, redirect, url_for, session
from models import db, User
import random
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.secret_key = "INTRO_TO_SE_PROJECT_G4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///introToSE.db'
db.init_app(app)



@app.route('/')
def home():
    if 'userID' in session:
        user = User.query.get(session['userID'])
        return render_template('home.html')
    return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user or not check_password_hash(existing_user.password, password):
            error = 'Incorrect Username/Password'
        else:
            session['userID'] = existing_user.userID
            flash("Logged in successfully!", 'success')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('userID', None)
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
        hashed_password = generate_password_hash(request.form['password'])
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
def viewAccount():
    error = None
    user = User.query.get(session['userID'])
     if request.method == 'POST':
         if request.form.get('confirm') == 'View':
             flash ('userID')
             return redirect(url_for('home'))
             

        
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
def editAccount():
    
    error = None
    user = User.query.get(session['userID'])

    if request.method == 'POST':
        if request.form.get('confirm') == 'Save Changes':
            if user.isAdmin:
                flash('Cannot edit admin account.', 'error')
                return redirect(url_for('home'))
            
            username = request.form['username']
            if username:
                user.username = username
            password = request.form['password']
            if password:
                user.password = generate_password_hash(password)
            email = request.form['email']
            if email:
                user.email = email
            address = request.form['address']
            if address:
                user.address = address
            city = request.form['city']
            if city:
                user.city = city
            state = request.form['state']
            if state:
                user.state = state
            zipCode = request.form['zipCode']
            if zipCode:
                user.zipCode= zipCode

            db.session.commit()
            flash('Saved changes.', 'info')
            return redirect(url_for('home'))
        
        else:
            flash('Discarding changes.')
            return redirect(url_for('home'))        

    return render_template('editAccount.html', error=error, user=user)

@app.route('/Viewcart', methods=['GET', 'POST'])

def create_tables():
    with app.app_context():
        db.create_all()
        if User.query.filter_by(userID=0).first() is None:
            user = User(userID=0, username='admin', password='admin', email='', address='',
            city='', state='', zipCode='', isAdmin=1)
            db.session.add(user)
            db.session.commit()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
