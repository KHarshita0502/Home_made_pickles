from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "pickles_secret_key"

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://admin:admin123@homemade.nuswitz.mongodb.net/?appName=homemade")

db = client["pickles_project"]
users_collection = db["users"]
orders_collection = db["orders"]


@app.route('/')
def index():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html", username=session["user"])


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        return redirect("/login")

    return render_template("signup.html")


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route('/veg_pickles')
def veg_pickles():
    return render_template("veg_pickles.html")


@app.route('/non_veg_pickles')
def non_veg_pickles():
    return render_template("non_veg_pickles.html")


@app.route('/snacks')
def snacks():
    return render_template("snacks.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/checkout', methods=['GET','POST'])
def checkout():

    if request.method == 'POST':

        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        orders_collection.insert_one({
            "name": name,
            "address": address,
            "phone": phone
        })

        return redirect('/success')

    return render_template("checkout.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact_us.html")


if __name__ == "__main__":
    app.run(debug=True)