import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///management.db")



@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    fullname = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    gender = request.form.get("gender")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")

    print(fullname,password,confirmation)
    if request.method == "POST":
        if not fullname or not password or not confirmation or not gender or not email or not phone_number:
            return apology("you must provide all required field",403)
        if password != confirmation:
            return apology("password doesnt match")
        row = db.execute("SELECT * FROM user WHERE email = :email",email=request.form.get("email"))
        if row:
            return apology("email already exist taken")
        hashed = generate_password_hash(password)
        ro = db.execute("INSERT INTO user (fullname,password,email,phone_number,gender,is_admin) VALUES(:fullname, :hashed, :email, :phone_number, :gender,:admin)",
        fullname = fullname, hashed = hashed, email = email, phone_number = phone_number, gender = gender, admin ='false'  )
        if not ro:
            return apology('error inserting')
        return redirect("/")
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
