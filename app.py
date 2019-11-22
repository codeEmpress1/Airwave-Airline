import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
import random
import datetime;
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, send_confirmation_email
from flask_cors import CORS, cross_origin


# Configure application
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# app = Flask(__name__)

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
            flash("must provide email", 403)
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", 403)
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("invalid username and/or password", 403)
            return render_template("index.html")

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
            flash("you must provide all required field",403)
            return render_template("register.html")
        if password != confirmation:
            flash("password doesnt match")
            return render_template("register.html")
           
        row = db.execute("SELECT * FROM user WHERE email = :email",email=request.form.get("email"))
        if row:
            flash("user all ready taken")
            return render_template("register.html")
            # return apology("email already exist taken")
        hashed = generate_password_hash(password)
        ro = db.execute("INSERT INTO user (fullname,password,email,phone_number,gender,is_admin) VALUES(:fullname, :hashed, :email, :phone_number, :gender,:admin)",
        fullname = fullname, hashed = hashed, email = email, phone_number = phone_number, gender = gender, admin ='false'  )
 --
        if not ro:
            flash("registration not successful")
            return render_template("register.html")
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/booking", methods=["GET", "POST"])
@login_required
def book():
    
    ticket_id = random.randint(1, 10000)
    departure = request.form.get("departure")
    destination = request.form.get("destination")
    date = request.form.get("date")
    time= request.form.get("time")
    status = "pending"
    # userId = session.get('user_id', 'user_id') 
    userId = session["user_id"] 
    usersrow=db.execute(f"Select * from user where id ='{userId}'")
    email=usersrow[0]["email"]
    fullname = usersrow[0]["fullname"]
    userId = session["user_id"]
    phone = usersrow[0]["phone_number"]
    # bookid = session["id"]

    # print(bookid)
    passenger = request.form.get("passenger")       
    if request.method == "POST":
        if not departure or not destination or not date or not  passenger:
            flash("fill all required field")
            return render_template("booking.html")
        
       
        
       
        ro = db.execute("SELECT * FROM price WHERE departure=:departure and destination=:destination ",departure=departure,destination=destination)
        prices =ro[0]['price']  * int(passenger)
        if not ro:
            return apology("flight unavalaible")
        row = db.execute("INSERT INTO booking (departure,destination,date,user_id,passenger,ticket_id,status,time,prices) VALUES(:departure, :destination, :date, :userId, :passenger, :ticket_id, :status, :time, :prices)",
        departure =departure, destination = destination, date = date, userId = userId, passenger = passenger,ticket_id =ticket_id, status=status, time=time, prices=prices)
        session["bookId"] =row
        session["pas"] = int(passenger)
        pa = session["pas"]
        bookId = session["bookId"] 
        display = db.execute("select * from booking where id=:bookId",bookId=bookId)
        return render_template("price.html",display=display,ro=ro,emails=email,fullname=fullname ,userId=userId, phone=phone,pa=pa)
    else:
        return render_template("booking.html")


@app.route('/create_transactions', methods=["POST"])
@cross_origin()
@login_required
def create_transaction():
    user_id = session["user_id"]
    bookId = session["bookId"]
    print(bookId)
        # request.get_json returns a dictionary
   
    json_data = request.get_json("data")
    print(json_data)
    ticket = db.execute("select ticket_id from booking where id=:bookId", bookId=bookId)
    ticket_id = ticket[0]['ticket_id']
    # print(ticket_id)
    name = str(json_data["name"])
    email = str(json_data["email"])

    
    reference = str(json_data["reference"])
    status = str(json_data["status"])
    message = str(json_data["message"])
    trans =  str(json_data["transaction"])
    phone = str(json_data["phone"])
    print(name,status,message,trans,phone)
    if request.method == "POST":
        ro = db.execute("insert into trans (name,email,reference,user_id,status,ticket_id,message,phone) values(:name,:email,:reference,:user_id,:status,:ticket_id,:message,:phone)",
        name=name, email=email, reference=reference, user_id=user_id, status=status, ticket_id=ticket_id,message=message,phone=phone)
        update = db.execute("update booking set status=:status where Id=:bookId", status=status,bookId=bookId)
        if not update:
            flash("transaction not completed")
            return render_template("price.html")
        
        return redirect("/booked")
    return render_template("booked.html")

    

@app.route('/booked')
@login_required
def booked():
   
    bookId = session["bookId"]
    if request.method == "GET":
        d = db.execute("select * from booking where id=:bookId",bookId=bookId)

        return render_template("booked.html", d=d)
   
    return render_template("booked.html")


if __name__ == "__main__":
    app.run()
