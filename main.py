from flask import Flask, flash, render_template, request, redirect, url_for, session
from models import db, User, Cart, Orders, Inventory, OrderItems
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import random
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "INTRO_TO_SE_PROJECT_G4"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///introToSE.db"
db.init_app(app)

login = LoginManager(app)
login.init_app(app)
login.login_view = "login"
login.login_message = "Please log in to access this page."


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        items = Inventory.query.all()
        return render_template("home.html", user=current_user, items=items)
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":

        username = request.form["userName"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user or not check_password_hash(existing_user.password, password):
            error = "Incorrect Username/Password"
        else:
            login_user(existing_user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


@app.route("/createAccount", methods=["GET", "POST"])
def createAccount():

    error = None

    if request.method == "POST":

        while True:

            userID = random.randint(100000000, 999999999)
            exists = User.query.filter_by(userID=userID).first()
            if not exists:
                break

        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        if password != confirmPassword:
            error = "Passwords do not match."
            flash(error, "error")
            return render_template("createAccount.html", error=error)
        hashed_password = generate_password_hash(password)
        email = request.form["email"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zipCode = request.form["zipCode"]
        isAdmin = 0

        usernameExists = User.query.filter_by(username=username).first()
        emailExists = User.query.filter_by(email=email).first()

        if not usernameExists and not emailExists:
            user = User(userID=userID, username=username, password=hashed_password, email=email, address=address,
                        city=city, state=state, zipCode=zipCode, isAdmin=isAdmin)
            db.session.add(user)
            db.session.commit()
            flash("Successfully created account.", "success")
            return redirect(url_for("login"))

        elif usernameExists:
            error = "Username already in use."

        else:
            error = "Account already exists with this email."

    return render_template("createAccount.html", error=error)


@app.route("/viewAccount", methods=["GET", "POST"])
@login_required
def viewAccount():
    if current_user.is_authenticated:
        return render_template("viewAccount.html", user=current_user)
    else:
        return redirect(url_for("login"))


@app.route("/deleteAccount", methods=["POST"])
@login_required
def deleteAccount():
    print("Delete account route triggered.")
    print(
        f"Attempting to delete user: {current_user.username}, ID: {current_user.userID}, isAdmin: {current_user.isAdmin}")
    # Prevent deletion of the admin account
    if current_user.userID == 0:
        flash("Cannot delete admin account.", "error")
        return redirect(url_for("home"))

    # Delete the currently logged-in user"s account
    db.session.delete(current_user)
    db.session.commit()

    # Log out the user after deleting the account
    logout_user()
    flash("Your account has been successfully deleted.", "success")
    return redirect(url_for("home"))


@app.route("/editAccount", methods=["GET", "POST"])
@login_required
def editAccount():
    if request.method == "POST":
        # Update the currently logged-in user"s account details
        current_user.username = request.form["username"]
        current_user.email = request.form["email"]
        current_user.address = request.form["address"]
        current_user.city = request.form["city"]
        current_user.state = request.form["state"]
        current_user.zipCode = request.form["zipCode"]

        db.session.commit()
        flash("Account details updated successfully!", "success")
        return redirect(url_for("viewAccount"))

    # Render the edit account page with the current user"s details
    return render_template("editAccount.html", user=current_user)


@app.route("/addToCart", methods=["GET", "POST"])
@login_required
def addToCart():
    error = None

    if request.method == "POST":

        if current_user.isAdmin:
            flash("Admins cannot purchase items.", "error")
            return redirect(request.referrer or url_for("home"))

        itemID = request.form["itemID"]
        quantity = int(request.form["quantity"])
        userID = current_user.userID

        item = Inventory.query.filter_by(itemID=itemID).first()
        if not item:
            flash("There was an unexpected error. (Item does not exist)", "error")
            return redirect(request.referrer or url_for("home"))
        
        if item.stock < quantity:
            flash("Item out of stock.", "error")
            return redirect(request.referrer or url_for("home"))
        
        cartItem = Cart(userID = userID, itemID = itemID, quantity = quantity)

        db.session.add(cartItem)
        db.session.commit()

        flash("Item added to cart.", "success")
        return redirect(request.referrer or url_for("home"))

# ADMIN STUFF


@app.route("/adminDashboard", methods=["GET"])
@login_required
def adminDashboard():
    # Ensure only admins can access this page
    if not current_user.isAdmin:
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for("home"))

    # Get the search query from the request arguments
    search_query = request.args.get("search", "")

    # Query the database for users
    if search_query:
        users = User.query.filter(
            ((User.username.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%"))) &
            (User.isAdmin == False)  # Exclude admin accounts
        ).all()
    else:
        users = User.query.filter_by(isAdmin=False).all()

    return render_template("adminDashboard.html", users=users)


@app.route("/deleteUser/<int:user_id>", methods=["POST"])
@login_required
def deleteUser(user_id):
    # Ensure only admins can delete accounts
    if not current_user.isAdmin:
        flash("You do not have permission to perform this action.", "error")
        return redirect(url_for("home"))

    # Prevent deletion of the admin account
    if user_id == current_user.userID:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("adminDashboard"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("adminDashboard"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} has been deleted.", "success")
    return redirect(url_for("adminDashboard"))


@app.route("/viewCart", methods=["GET"])
@login_required
def viewCart():
    items = db.session.query(Cart, Inventory)\
        .join(Inventory, Cart.itemID == Inventory.itemID)\
        .filter(Cart.userID == current_user.userID)\
        .all()
    return render_template('viewCart.html', items=items)


@app.route('/addInventory', methods=['GET', 'POST'])
@login_required
def addInventory():
    if request.method == 'POST':
        try:
            title = request.form['title']
            sellerID = current_user.userID
            price = request.form['price']
            quantity = request.form['quantity']
            description = request.form["description"]

            # Handle image upload
            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image.filename != '':
                    # Ensure the upload folder exists
                    upload_folder = os.path.join(
                        app.root_path, 'static', 'products')
                    os.makedirs(upload_folder, exist_ok=True)

                    # Secure the filename and save the file
                    filename = secure_filename(image.filename)
                    image_path = f'products/{filename}'
                    image.save(os.path.join(upload_folder, filename))

            inventory_item = Inventory(
                title=title,
                sellerID=sellerID,
                price=price,
                stock=quantity,
                image=image_path,
                description = description
            )
            db.session.add(inventory_item)
            db.session.commit()
            flash('Item added to inventory successfully!', 'success')
            return redirect(url_for('inventory'))
        except Exception as e:
            flash(f'Error adding item: {str(e)}', 'error')
            return redirect(url_for('addInventory'))

    return render_template('addInventory.html')


@app.route('/viewProducts/', methods=['GET', 'POST'])
@login_required  # Add login required decorator
def viewInventory():
    userID = current_user.userID
    inventory = Inventory.query.filter_by(sellerID=userID).all()
    return render_template('viewProducts.html', products=inventory)


@app.route('/deleteInventory/<int:item_id>', methods=['POST'])
@login_required
def deleteInventory(item_id):
    item = Inventory.query.get_or_404(item_id)

    # Verify the current user owns this item or is an admin
    if item.sellerID != current_user.userID and not current_user.isAdmin:
        return redirect(url_for('viewInventory'))

    if item.image:
        image_path = os.path.join(app.root_path, 'static', item.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')

    if current_user.isAdmin:
        return render_template('sellerDashboard.html', products=Inventory.query.all())
    else:
        return render_template('viewProducts.html', products=Inventory.query.filter_by(sellerID=current_user.userID).all())


@app.route('/sellerDashboard', methods=['GET'])
@login_required
def sellerDashboard():
    # Join Inventory with User to get seller information
    products = db.session.query(Inventory, User.username)\
        .join(User, Inventory.sellerID == User.userID)\
        .all()
    return render_template('sellerDashboard.html', products=products)


def create_tables():
    with app.app_context():
        db.create_all()
        if User.query.filter_by(userID=0).first() is None:
            user = User(userID=0, username="admin", password=generate_password_hash("admin"), email="", address="",
                        city="", state="", zipCode="", isAdmin=1)
            db.session.add(user)
            db.session.commit()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
