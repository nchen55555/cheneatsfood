import sqlite3
import requests

from flask import Flask,  redirect, render_template, request, session, Markup
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = sqlite3.connect("camps.db", check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS 'volunteerResponses' ('volunteer_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'first' TEXT NOT NULL, 'last' TEXT NOT NULL, 'age' INTEGER NOT NULL, 'interest' TEXT NOT NULL, 'experience' TEXT NOT NULL, 'notes' TEXT NOT NULL)")    
db.execute("CREATE TABLE IF NOT EXISTS 'registration' ('registration_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'first' TEXT NOT NULL, 'last' TEXT NOT NULL, 'age' INTEGER NOT NULL, 'email' TEXT NOT NULL, 'phonenumber' TEXT NOT NULL, 'camp' INTEGER NOT NULL)")    
db.execute("CREATE TABLE IF NOT EXISTS 'blogs' ('blog_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'title' TEXT NOT NULL, 'date' DATETIME NOT NULL, 'imagesource' TEXT NOT NULL, 'text' TEXT NOT NULL)")    
db.execute("CREATE TABLE IF NOT EXISTS 'members' ('member_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'firstname' TEXT NOT NULL, 'lastname' TEXT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'admin' BOOLEAN NOT NULL)")    

# Mail 
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dtccscamp@gmail.com'
app.config['MAIL_PASSWORD'] = 'DTCcsr0ck5!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    """Show camp homepage"""
    # TODO 
    return render_template("index.html")

@app.route("/about")
def about():
    """Show about page"""
    return render_template("about.html")

@app.route("/info", methods=["GET", "POST"])
def info():
    """Sessions and Information"""
    color = "red"
    message = ""
    if request.method == "GET":
        return render_template("info.html")
 
    else:
        
        try:
            int(request.form.get("age"))
        except ValueError:
            message = "Input a Valid Age Please"
            return render_template("info.html", message=message, color=color)

        first = request.form.get("firstname")
        last = request.form.get("lastname")
        age = int(request.form.get("age"))
        email = request.form.get("email")
        number = request.form.get("phonenumber")
        camp1 = request.form.get("camp1")
        camp2 = request.form.get("camp2")
        camps = 0

        if not request.form.get("firstname"):
            message = "Please input a first name"
            return render_template("info.html", message=message, color=color)
        if not request.form.get("lastname"):
            message = "Please input a last name"
            return render_template("info.html", message=message, color=color)
        if not request.form.get("age"):
            message = "Please input an age"
            return render_template("info.html", message=message, color=color)
        if not request.form.get("email"):
            message = "Please input an email"
            return render_template("info.html", message=message, color=color)
        if not request.form.get("phonenumber"):
            message = "Please input a phonenumber"
            return render_template("info.html", message=message, color=color)
        if not request.form.get("camp1") and not request.form.get("camp2"):
            message = "Please select a camp session"
            return render_template("info.html", message=message, color=color)

        if (camp1 is not None) and (camp2 is not None):
            camps = 3
        elif (camp1 is None) and (camp2 is not None):
            camps = 1
        elif (camp2 is None) and (camp1 is not None):
            camps = 2

        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

        status = response.json()['status']
        if status == "valid":
            message = "Thank you for registering!"
            db.execute("INSERT INTO registration (first, last, age, email, phonenumber, camp) VALUES (?, ?, ?, ?, ?, ?)", 
                    (first, last, age, email, number, camps))
            db.commit()
            index = 0
            name = first
            while True:
                rows = db.execute("SELECT * FROM members WHERE firstname = ? AND lastname = ?", (name, last)).fetchall()
                if rows == []:
                    break;
                index+=1
                name = first + str(index)
                
            
            db.execute("INSERT INTO members (firstname, lastname, username, hash, admin) VALUES (?, ?, ?, ?, ?)", (first, last, name, generate_password_hash(last), False))
            db.commit()
            msg = Message('DTC Computer Science Camp Registration', sender = 'dtccscamp@gmail.com', recipients = [email])
            msg.body = "Hi! Thank you for registering for DTC Computer Science Camps! We will send out another email in the next coming weeks about more information for the camps. Your username is \"" + name + "\" and your password is \"" + last + "\" You can change your password by logging in first then clicking the change username/password option."
            mail.send(msg)
            color = "green"

        else:
            message = "There was a problem with your email. Please enter a valid email address"

        return render_template("info.html", message=message, color=color)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Show contact page"""
    m = ""
    color="red"
    if request.method == "GET":
        return render_template("contact.html", m=m)
 
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        if name is None:
            m = "Please input a name"
            return render_template("contact.html", m=m, color=color)
        if email is None:
            m = "Please input an email"
            return render_template("contact.html", m=m, color=color)
        if message is None:
            m = "Please input a message"
            return render_template("contact.html", m=m, color=color)

        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

        status = response.json()['status']
        if status == "valid":
            color = "green"
            m = "Message Sent! We will be in contact with you shortly."

            msg = Message('Contact Us Message', sender = 'dtccscamp@gmail.com', recipients = [email])
            msg.body = name + " with an email of " + email + " sent you this message: \n" + message
            mail.send(msg)
            color = "green"
        else:
            m = "There was a problem with your email. Please input a valid email."
            color = "red"

        return render_template("contact.html", m=m, color=color)

@app.route("/blog")
def blog():
    """Show blog page"""
    blogs = db.execute("SELECT title, blog_id, date, imagesource, text FROM blogs").fetchall()
    return render_template("blog.html", blogs=blogs)

@app.route("/subblog")
def subblog():
    """Show blog page"""
    blogid = request.args.get("blogid")
    if blogid is None:
        return redirect("/blog")

    title = db.execute("SELECT title FROM blogs WHERE blog_id = ?", [blogid]) 
    title = title.fetchone()[0]
    date = db.execute("SELECT date FROM blogs WHERE blog_id = ?", [blogid])
    date = date.fetchone()[0]
    text = db.execute("SELECT text FROM blogs WHERE blog_id = ?", [blogid])
    text = text.fetchone()[0]
    image = db.execute("SELECT imagesource FROM blogs WHERE blog_id = ?", [blogid])
    image = image.fetchone()[0]

    return render_template("subblog.html", title=title,date=date,text=Markup(text),image=image)

@app.route("/resources", methods=["GET", "POST"])
@login_required
def resources():
    """Show resources page"""
    admin = db.execute("SELECT admin FROM members WHERE member_id = ?", session["user_id"]).fetchone()[0]
    if request.method == "GET":
        return render_template("resources.html", admin=admin)
    else:
        title = request.form.get("title")
        date = request.form.get("date")
        image = request.form.get("image")
        text = request.form.get("text")
        color = "red"

        if not title:
            message = "Please input a title."
            return render_template("resources.html", color=color, message=message)
        if not date:
            message = "Please input a date."
            return render_template("resources.html", color=color, message=message)
        if not image:
            message = "Please input an image source"
            return render_template("resources.html", color=color, message=message)
        if not text:
            message = "Please input blog text"
            return render_template("resources.html", color=color, message=message)
        if not admin:
            message = "You are not an administrator and therefore do not have access to post blogs."
            return render_template("resources.html", color=color, message=message)
        try:
            db.execute("INSERT INTO blogs (title, date, imagesource, text) VALUES (?, ?, ?, ?)", (title, date, image, text))
            db.commit()
        except sqlite3.OperationalError:
            return redirect("/resources")
        return redirect("/resources")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Show register page"""
    message = ""
    color = "red"
    if request.method == "GET":
        return render_template("change.html")
    else: 
        if not request.form.get("oldusername"):
            message = "Please input your old username. If you forgot your username, you will have to email us to reset it for extra security purposes."
            return render_template("change.html", color=color, message=message)
        if not request.form.get("oldpassword"):
            message = "Please input your old password. If you forgot your password, you will have to email us to reset it for extra security purposes."
            return render_template("change.html", color=color, message=message)
        if not request.form.get("newpassword"):
            message = "Please input your new password."
            return render_template("change.html", color=color, message=message)

        newpassword = request.form.get("newpassword")
        oldusername = request.form.get("oldusername")
        oldpassword = request.form.get("oldpassword")

        rows = db.execute("SELECT * FROM members WHERE username = ? AND member_id = ?", (oldusername, session["user_id"][0])).fetchall()
        if rows != [] and check_password_hash(rows[0][4], oldpassword):
            print(rows[0])
            newhash = generate_password_hash(newpassword)
            db.execute("UPDATE members SET hash = ? WHERE member_id = ?", (newhash, session["user_id"][0]))
            db.commit()
            session.clear()
            return redirect("/")
        else:
            message="Username and/or Password Incorrect"
            color="red"
            return render_template("change.html", message=message, color=color)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show signin page"""

    if request.method == "GET":
        return render_template("login.html")
    else:     
        message = ""
        color = "red"
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            message="Please input an username"
            return render_template("login.html", message=message, color=color)
        if not password:
            message="Please input a password"
            return render_template("login.html", message=message, color=color)
        else:
            hash = db.execute("SELECT hash FROM members WHERE username = ?", [username]).fetchall()
            if hash == []:
                message="Username and/or Password Incorrect"
                color="red"
                return render_template("login.html", message=message, color=color)
            if not check_password_hash(hash[0][0],password):
                message="Username and/or Password Incorrect"
                color="red"
                return render_template("login.html", message=message, color=color)
            else:
                id = db.execute("SELECT member_id FROM members WHERE username = ?", [username]).fetchone()
                session["user_id"] = id
                return redirect("/resources")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/flyer")
def flyer():
    """Flyer""" 
    return render_template("flyer.html")

@app.route("/mentors")
def mentors():
    """Mentors"""
    return render_template("mentors.html")

@app.route("/professionals")
def professionals():
    """Professionals"""
    return render_template("professionals.html")

@app.route("/volunteers", methods=["GET", "POST"]) 
def volunteers():
    """Volunteers"""
    message = ""
    color="red"
    if request.method == "GET":
        return render_template("volunteers.html", message=message)
 
    else:
        try:
            int(request.form.get("age"))
        except ValueError:
            message="Please input a valid age"
            return render_template("volunteers.html", message=message, color=color)

        first = request.form.get("firstname")
        last = request.form.get("lastname")
        age = int(request.form.get("age"))
        interest = request.form.get("interest")
        experience = request.form.get("experience")
        notes = request.form.get("notes")

        if not first:
            message = "Please input first name."
            return render_template("change.html", message=message, color=color)
        if not last:
            message = "Please input your last name."
            return render_template("change.html", message=message, color=color)
        if not age:
            message = "Please input your age."
            return render_template("change.html", message=message, color=color)
        if not interest:
            message = "Please input your interest."
            return render_template("change.html", message=message, color=color)
        if not experience:
            message = "Please input your experience."
            return render_template("change.html", message=message, color=color)
        
        message = "Thank you for submitting your application!"
        db.execute("INSERT INTO volunteerResponses (first, last, age, interest, experience, notes) VALUES (?, ?, ?, ?, ?, ?)", 
                   (first, last, age, interest, experience, notes))
        db.commit()
        return render_template("volunteers.html", message=message)


