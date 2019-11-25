import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
import random
import datetime;
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_cors import CORS, cross_origin
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
def index():
    """Show portfolio of stocks"""

    return render_template("index.html")
    # return render_template("index.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


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
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/home")
@login_required
def land():
    user_id = session["user_id"]
    allusers = db.execute("select * from user where id=:user_id",user_id=user_id)
    admin = allusers[0]["is_admin"]
    if admin == "true":
        return render_template("admin2.html",allusers=allusers)
    return render_template("home.html", allusers=allusers)




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

        if not ro:
            flash("registration not successful")
            return render_template("register.html")
        flash("registration successful")
        return redirect("login.html")
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
        if not departure or not destination or not date or not  passenger or not time:
            flash("fill all required field")
            return render_template("booking.html")
        val = db.execute("select date from booking")
        val2 = db.execute("select time from booking")
        arr3 =[]
        arr4=[]
        for i in val:
            if str(i['date'])== str(date):
                arr3.append(i['date'])
        for i in val2:
            if str(i['time'])== str(time):
                arr4.append(i['time'])
        if len(arr3) > 50 and len(arr4) > 50:
            print(len(arr3),len(arr4))
            flash("flight booking unavailable")
            return render_template("booking.html")
 


        
       
        ro = db.execute("SELECT * FROM price WHERE departure=:departure and destination=:destination ",departure=departure,destination=destination)
        if not ro:
            flash("flight unavailable")
            return render_template("booking.html")
        prices =ro[0]['price']  * int(passenger)
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
    price = str(json_data["price"])
    print(name,status,message,trans,phone,price)
    if request.method == "POST":
        ro = db.execute("insert into trans (name,email,reference,user_id,status,ticket_id,message,phone,price) values(:name,:email,:reference,:user_id,:status,:ticket_id,:message,:phone,:price)",
        name=name, email=email, reference=reference, user_id=user_id, status=status, ticket_id=ticket_id,message=message,phone=phone,price=price)
        update = db.execute("update booking set status=:status where Id=:bookId", status=status,bookId=bookId)
        session["transId"] = ro
        transId = session["transId"]
        send_mail_to_user = db.execute("select * from trans where id=:transId",transId=transId)

        
        ticket_id2 = send_mail_to_user[0]["ticket_id"]
        name2 = send_mail_to_user[0]["name"]
        status2 = send_mail_to_user[0]["status"]
        message2 = send_mail_to_user[0]["message"]
        trans2 = send_mail_to_user[0]["reference"]
        price2 = send_mail_to_user[0]["price"]

       
        email = db.execute('select email from user where id=:user_id',user_id=user_id)
        emails = email[0]['email']
        sender_email = "airwaveairline@gmail.com"
        receiver_email = emails
        password = "decagon1234"

        message = MIMEMultipart("alternative")
        message["Subject"] = "flight booking successful"
        message["From"] = sender_email
        message["To"] = receiver_email
        html = f"""\
                <html>
                <body>
                    <h1>airwave reservation booking, {ticket_id2}</h1> <br>
                    <h2>Dear, {name2}</h2>
                    <p>Thank yo for making your booking with airwave airline below re the details of your itinerary:</p>
                    <p>status: {status2}</p>
                    <p>message: {message2}</p>
                    <p>ref: {trans2}</p>
                    <p>price: {price2}</p>

                    
                </body>
                </html>
                """
    
        # Turn these into plain/html MIMEText objects
        # part1 = MIMEText(text, "plain")
        part = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            
        
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

       
     


@app.route("/alluser")
# add to admin view
def alluser():
    allusers = db.execute("select * from user")
    return render_template("allusers.html",allusers=allusers)


@app.route("/alltrans")
# add to admin view
def trans():
    alltrans = db.execute("select * from trans")
    return render_template("alltrans.html",alltrans=alltrans)



@app.route("/allbookings")
def allbookings():
    row = db.execute("select * from booking")
    return render_template("allbooinkgs.html",row=row)



@app.route("/allprices")
def prices():
    row = db.execute("select * from price")
    return render_template("prices.html",row=row)


@app.route("/history")
# add to admin view
def history():
    user_id = session["user_id"]
    print(user_id)
    allusers = db.execute("select * from  booking where user_id=:user_id",user_id=user_id)
    if not allusers :
        flash("no booking history")
        return render_template('userhistory.html')
    return render_template("userhistory.html",allusers=allusers)

@app.route('/avaliableprice')
def available():
    row = db.execute("select * from price")
    return render_template("avaliableprice.html",row=row)

@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/update/<int:id>",methods=["POST"])
def updateuse(id):
    if request.method == "POST":
        price= request.form.get('update')
        print(id)
        ro = db.execute("update price set price=:price where id=:id",id=id,price=price)
        row = db.execute("select * from price")
        return render_template("prices.html",row=row)


@app.route('/delete/<int:id>',methods=["POST"])
def delt(id):
    print(id)
    if request.method == "POST":
        db.execute("delete  from price where id=:id",id=id)
        return redirect("/avaliableprice")



@app.route("/addprice", methods=["POST","GET"])
def addprice():
    destination =request.form.get("pdest")
    departure = request.form.get("pdepar")
    price =request.form.get("pprice")
    print(destination,departure,price)
    if request.method == "POST":
        db.execute("insert into price (destination,departure,price) values (:destination,:departure,:price)",destination=destination,departure=departure,price=price)
        return redirect("/allprices")
    return render_template('addprices.html')




if __name__ == "__main__":
    app.run()
