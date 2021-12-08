import sqlite3
import requests

from flask import Flask,  redirect, render_template, request, session, Markup
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Nicole Chen CS50 Final

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#connects to the camps database
db = sqlite3.connect("camps.db", check_same_thread = False)
#creates a table called volunterResponses under the camps database
db.execute("CREATE TABLE IF NOT EXISTS 'volunteerResponses' ('volunteer_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'first' TEXT NOT NULL, 'last' TEXT NOT NULL, 'age' INTEGER NOT NULL, 'email' TEXT NOT NULL, 'interest' TEXT NOT NULL, 'experience' TEXT NOT NULL, 'notes' TEXT NOT NULL)")    
#creates a table called registration under the camps database 
db.execute("CREATE TABLE IF NOT EXISTS 'registration' ('registration_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'first' TEXT NOT NULL, 'last' TEXT NOT NULL, 'age' INTEGER NOT NULL, 'email' TEXT NOT NULL, 'phonenumber' TEXT NOT NULL, 'camp' INTEGER NOT NULL)")    
#creates a table called blogs under the the camps database 
db.execute("CREATE TABLE IF NOT EXISTS 'blogs' ('blog_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'title' TEXT NOT NULL, 'date' DATETIME NOT NULL, 'imagesource' TEXT NOT NULL, 'text' TEXT NOT NULL)")    
#creates a table called members in the camps database 
db.execute("CREATE TABLE IF NOT EXISTS 'members' ('member_id' INTEGER NOT NULL UNIQUE PRIMARY KEY, 'firstname' TEXT NOT NULL, 'lastname' TEXT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'admin' BOOLEAN NOT NULL)")    

#establishes mail connection 
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sendgrid.net',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'apikey',
    MAIL_PASSWORD = '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',
))
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

#home page 
@app.route("/")
def index():
    """Show camp homepage"""
    #returns the template index.html to send user to the home page 
    return render_template("index.html")

#about page
@app.route("/about")
def about():
    """Show about page"""
    #returns the template about.html to send user to the about page 
    return render_template("about.html")

#sessions and information page 
@app.route("/info", methods = ["GET", "POST"])
def info():
    """Sessions and Information"""
    #sets the color variable to red (will display message in red css)
    color = "red"
    #checks to see if request was through GET or POST
    if request.method == "GET":
        return render_template("info.html")
 
    #request is through POST
    else:  
        #checks to see if the inputted age is a valid integer  
        try:
            int(request.form.get("age"))
        except ValueError:
            #outputs an error message if the inputted age is invalid 
            message = "Input a Valid Age Please"
            return render_template("info.html", message = message, color = color)

        #collects first name, last name, age, email, phone number, and camp selection using request from the html form
        first = request.form.get("firstname")
        last = request.form.get("lastname")
        age = int(request.form.get("age"))
        email = request.form.get("email")
        number = request.form.get("phonenumber")
        camp1 = request.form.get("camp1")
        camp2 = request.form.get("camp2")
        #variable that holds what camps were signed up for 
        camps = 0

        #checks to see if user inputted required fields 
        if not first:
            message = "Please input a first name"
            return render_template("info.html", message = message, color = color)
        if not last:
            message = "Please input a last name"
            return render_template("info.html", message = message, color = color)
        if not age:
            message = "Please input an age"
            return render_template("info.html", message = message, color = color)
        if not email:
            message = "Please input an email"
            return render_template("info.html", message = message, color = color)
        if not number:
            message = "Please input a phonenumber"
            return render_template("info.html", message = message, color = color)
        if not camp1 and not camp2:
            message = "Please select a camp session"
            return render_template("info.html", message = message, color = color)

        #documents the camps signed up using integers - if the user signed up for both camps
        #camps will be 3. If the user signed up for session 2, camps will be 2. 
        #If the user signed up for session 1, camps will be 1.
        if (camp1 is not None) and (camp2 is not None):
            camps = 3
        elif (camp1 is None) and (camp2 is not None):
            camps = 2
        elif (camp2 is None) and (camp1 is not None):
            camps = 1

        #validates the email input
        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

        status = response.json()['status']

        #checks to see if the email provided is valid 
        if status == "valid":
            message = "Thank you for registering!"
            #inserts first name, last name, age, email, phone number, and camp registration into the registration database
            db.execute("INSERT INTO registration (first, last, age, email, phonenumber, camp) VALUES (?, ?, ?, ?, ?, ?)", 
                    (first, last, age, email, number, camps))
            db.commit()
            #index is a variable that represents the number of users who already have the registered first name
            #index will be added on to the username of the registered user if there are more than one registrant with the same first name
            index = 1
            #name is a substitute variable for first that will take on index if there are more than one registrant with the same first name
            name = first
            #do while loop
            while True:
                #selects all cases where username in members equals the inputted first name
                rows = db.execute("SELECT * FROM members WHERE username = ?", [name]).fetchall()
                #checks to see if the registrant's firstname are already used in the members database 
                #if there is no one else in registrant with the same first name, then the loop breaks 
                if rows == []:
                    break
                
                #however if there are others in registrant with the same first name, then index increments and is added on to name 
                index += 1
                #by adding on the new index to first to create name, the inserted username value will be different from registrants with the same first name
                name = first + str(index)
                
            #database command that inserts the first, last, username, password, and whether the user is an admin or not value into the members database
            #note: username is the first name of the registrant plus index if there are more than one registrant with the same first name
            #note: hash is the hashed last name of the registrant. This is a temporary password that can be changed by the user
            db.execute("INSERT INTO members (firstname, lastname, username, hash, admin) VALUES (?, ?, ?, ?, ?)", (first, last, name, generate_password_hash(last), False))
            db.commit()

            #constructs mail message to be sent from the dtccscamp@gmail.com account to the email provided in the input box
            msg = Message('DTC Computer Science Camp Registration', sender = 'dtccscamp@gmail.com', recipients = [email])
            #mail message includes the user's username and password to log in to access the resources page
            msg.body = "Hi! Thank you for registering for DTC Computer Science Camps! We will send out another email in the next coming weeks about more information for the camps. Your username is \"" + name + "\" and your password is \"" + last + "\" You can change your password by logging in first then clicking the change username/password option."
            mail.send(msg)
            color = "green"

        #if the email provided is not valid 
        else:
            #constructs below message 
            message = "There was a problem with your email. Please enter a valid email address"

        #returns the info.html page with the constructed message and specified color
        return render_template("info.html", message = message, color = color)

#contact page
@app.route("/contact", methods = ["GET", "POST"])
def contact():
    """Show contact page"""
    #sets the color variable to red (will display message in red css)
    color="red"
    #checks to see if the request was through GET or POST 
    if request.method == "GET":
        return render_template("contact.html")

    #since request was through POST 
    else:
        #gets the name, email, and message from the contact us form from html 
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        #checks to see if the user inputted a name, email, and message
        if name is None:
            m = "Please input a name"
            return render_template("contact.html", m = m, color = color)
        if email is None:
            m = "Please input an email"
            return render_template("contact.html", m = m, color = color)
        if message is None:
            m = "Please input a message"
            return render_template("contact.html", m = m, color = color)

        #validates the email input
        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

        status = response.json()['status']

        #checks to see if the email inputted is valid
        if status == "valid":
            #changes the css color to green
            color = "green"
            m = "Message Sent! We will be in contact with you shortly."

            #adds a mail message titled "Contact Us Message" that is sent from dtccscamp@gmail.com to dtccscamp@gmail.com 
            msg = Message('Contact Us Message', sender = 'dtccscamp@gmail.com', recipients = ['dtccscamp@gmail.com'])
            msg.body = name + " with an email of " + email + " sent you this message: \n" + message
            mail.send(msg)
        #if the email inputted is not valid
        else:
            m = "There was a problem with your email. Please input a valid email."

        return render_template("contact.html", m = m, color = color)

#blog page
@app.route("/blog")
def blog():
    """Show blog page"""
    #from the database, selects title, blog_id, date, imagesoure, and text from blogs table 
    #note: imagesource is the image file name included in the blog post (ie. nicole.jpg)
    blogs = db.execute("SELECT title, blog_id, date, imagesource, text FROM blogs").fetchall()
    #returns blogs to the blog.html so that the html page can access the database information 
    return render_template("blog.html", blogs = blogs)

#subblog page (aka. when users click a blog post to read, they come to the subblog page)
@app.route("/subblog")
def subblog():
    """Show blog page"""
    #gets the blog id from html (when the user clicks on the "Read Me" button from blog.html, the blog_id is passed)
    blogid = request.args.get("blogid")

    #checks to see if server received a blog_id
    if blogid is None:
        #redirects the page back to blog if it did not receive a blog_id
        return redirect("/blog")

    #retrieves title, date, blog text, and blog's image from the blog database with the given blog id 
    title = db.execute("SELECT title FROM blogs WHERE blog_id = ?", [blogid]).fetchone()[0]
    date = db.execute("SELECT date FROM blogs WHERE blog_id = ?", [blogid]).fetchone()[0]
    text = db.execute("SELECT text FROM blogs WHERE blog_id = ?", [blogid]).fetchone()[0]
    image = db.execute("SELECT imagesource FROM blogs WHERE blog_id = ?", [blogid]).fetchone()[0]

    #user is redirected to the subblog page that is filled with the title, date, text, and image source provided 
    #by the database. 
    #Note: the Markup function by text ensures that the text added to the database contains and utilizes HTML 
    #ex. there are parts in text that have html tags so that the webpage knows where to indent and add a new line
    return render_template("subblog.html", title = title,date = date,text = Markup(text),image = image)

#resources page that is only accessible if the user is logged in
@app.route("/resources", methods = ["GET", "POST"])
@login_required
def resources():
    """Show resources page"""
    #retrieves from the session's user id whether or not the user has administrative access or not 
    #this is because if the user has administrative access, then the resources page will show a blog form 
    #so that the admin can post to the blogs page
    admin = db.execute("SELECT admin FROM members WHERE member_id = ?", session["user_id"]).fetchone()[0]
    
    #checks to see if the request was through GET or POST
    if request.method == "GET":
        return render_template("resources.html", admin = admin)
    #the request was sent through POST
    else:
        #gets the title, date, image, and text from the blog post form from resources.html
        title = request.form.get("title")
        date = request.form.get("date")
        image = request.form.get("image")
        text = request.form.get("text")
        
        #sets the color css to red
        color = "red"

        #checks to see if user inputted a title, date, image source, and text or else outputs an error message
        if not title:
            message = "Please input a title."
            return render_template("resources.html", admin = admin, color = color, message = message)
        if not date:
            message = "Please input a date."
            return render_template("resources.html", admin = admin, color = color, message = message)
        if not image:
            message = "Please input an image source"
            return render_template("resources.html", admin = admin, color = color, message = message)
        if not text:
            message = "Please input blog text"
            return render_template("resources.html", admin = admin, color = color, message = message)

        #checks to see if the user is an admin or not to make sure that blog posts are only sent by administrators
        if not admin:
            message = "You are not an administrator and therefore do not have access to post blogs."
            return render_template("resources.html", admin = admin, color = color, message = message)
        
        #tries to insert blogs according to the inputted data
        try:
            db.execute("INSERT INTO blogs (title, date, imagesource, text) VALUES (?, ?, ?, ?)", (title, date, image, text))
            db.commit()
        except sqlite3.OperationalError:
            #redirects to the resources page if unsuccessful 
            return redirect("/resources")
        #redirects to the blog page if successful
        return redirect("/blog")

#password change page that requires the user to be logged in
@app.route("/change", methods = ["GET", "POST"])
@login_required
def change():
    """Show register page"""
    #sets the color css to red
    color = "red"

    #checks to see if the request was through GET or POST
    if request.method == "GET":
        return render_template("change.html")
    
    #the request was sent through POST 
    else: 

        #retrieves the newpassword, oldusername, and oldpassword inputted by the user in html
        newpassword = request.form.get("newpassword")
        oldusername = request.form.get("oldusername")
        oldpassword = request.form.get("oldpassword")

        #checks to see if the user inputted an oldusername, oldpassword, and newpassword
        if not oldusername:
            message = "Please input your old username. If you forgot your username, you will have to email us to reset it for extra security purposes."
            return render_template("change.html", color = color, message = message)
        if not oldpassword:
            message = "Please input your old password. If you forgot your password, you will have to email us to reset it for extra security purposes."
            return render_template("change.html", color = color, message = message)
        if not newpassword:
            message = "Please input your new password."
            return render_template("change.html", color = color, message = message)

        #selects from the database all columns where the username is the oldusername and the member_id matches with the current signed in member_id
        rows = db.execute("SELECT * FROM members WHERE username = ? AND member_id = ?", (oldusername, session["user_id"][0])).fetchall()
        
        #checks to see if there are instances where the oldusername is in the members database and the signed in user id matches with username id 
        #also checks to see if the oldpassword matches with the database-stored password
        if rows != [] and check_password_hash(rows[0][4], oldpassword):
            #generates a new hash according to the new password
            newhash = generate_password_hash(newpassword)
            #updates the members database with the new hashed password 
            db.execute("UPDATE members SET hash = ? WHERE member_id = ?", (newhash, session["user_id"][0]))
            db.commit()
            #clears session
            session.clear()
            return redirect("/")
        
        #if there are no instances where the old username is in the members database and the signed in user id matches with the username id 
        #or if there are no instances where the old password matches the stored database password
        else:
            #then output the message below in red
            message = "Username and/or Password Incorrect"
            return render_template("change.html", message = message, color = color)

#login page
@app.route("/login", methods = ["GET", "POST"])
def login():
    """Show signin page"""
    #checks to see if the request was through GET or POST 
    if request.method == "GET":
        return render_template("login.html")
    
    #request was through POST 
    else: 
        #sets css color to red     
        color = "red"
        #makes sure that the session is cleared 
        session.clear()
        #gets the username and password from the user input form in html
        username = request.form.get("username")
        password = request.form.get("password")

        #checks to see if the user inputted a username and password 
        if not username:
            message = "Please input an username"
            return render_template("login.html", message = message, color = color)
        if not password:
            message = "Please input a password"
            return render_template("login.html", message = message, color = color)
        #selects hash from members where the username is equal to the inputted username
        hash = db.execute("SELECT hash FROM members WHERE username = ?", [username]).fetchall()
        print(hash)
        print(check_password_hash(hash[0][0],password))
        #checks to there was a hash selected from members where the username was equal to the inputted username
        if hash == []:
            #no hash selected so the username was incorrect (there was no username)
            message="Username and/or Password Incorrect"
            return render_template("login.html", message = message, color = color)
        #checks to see if the inputted password matches the stored hashed password
        if not check_password_hash(hash[0][0],password):
            #don't match so password was incorrect 
            message = "Username and/or Password Incorrect"
            return render_template("login.html", message = message, color = color)
        else:
            #selects id from members where the username is equal to the inputted username
            id = db.execute("SELECT member_id FROM members WHERE username = ?", [username]).fetchone()
            #session's user id is set equal to the member id, ensuring that the user is logged in 
            session["user_id"] = id
            #redirects the user to the resources page 
            return redirect("/resources")

#logout page
@app.route("/logout")
def logout():
    """Log user out"""
    #clears session
    session.clear()
    #redirects program to main page
    return redirect("/")

#flyer page 
@app.route("/flyer")
def flyer():
    """Flyer"""
    return render_template("flyer.html")

#mentors page 
@app.route("/mentors")
def mentors():
    """Mentors"""
    return render_template("mentors.html")

#professionals page 
@app.route("/professionals")
def professionals():
    """Professionals"""
    return render_template("professionals.html")

#volunteers page
@app.route("/volunteers", methods = ["GET", "POST"]) 
def volunteers():
    """Volunteers"""
    #makes the color css red
    color = "red"
    #checks to see if request was taken via GET or POST 
    if request.method == "GET":
        return render_template("volunteers.html")
    #request was taken via POST 
    else:
        #tries to type cast the age element received from HTML as an integer 
        try:
            int(request.form.get("age"))
        except ValueError:
            message = "Please input a valid age"
            return render_template("volunteers.html", message = message, color = color)

        #gets the first name, last name, age, email, interest, experience, and notes from the volunteers html 
        first = request.form.get("firstname")
        last = request.form.get("lastname")
        age = int(request.form.get("age"))
        email = request.form.get("email")
        interest = request.form.get("interest")
        experience = request.form.get("experience")
        notes = request.form.get("notes")

        #checks to see if the user inputted a firstname, lastname, age, email, interest, and experience
        if not first:
            message = "Please input first name."
            return render_template("change.html", message = message, color = color)
        if not last:
            message = "Please input your last name."
            return render_template("change.html", message = message, color = color)
        if not age:
            message = "Please input your age."
            return render_template("change.html", message = message, color = color)
        if not email:
            message = "Please input your email."
            return render_template("change.html", message = message, color = color)
        if not interest:
            message = "Please input your interest."
            return render_template("change.html", message = message, color = color)
        if not experience:
            message = "Please input your experience."
            return render_template("change.html", message = message, color = color)
        
        #validates the email inputted 
        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

        status = response.json()['status']
        #checks to see if email is valid
        if status == "valid":
            message = "Thank you for submitting your application!"
            #inserts the inputted firstname, lastname, age, email, interest, experience, and notes into the volunteerResponses table
            db.execute("INSERT INTO volunteerResponses (first, last, age, email, interest, experience, notes) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (first, last, age, email, interest, experience, notes))
            db.commit()
            #sends a mail message to the volunteer confirming their application
            msg = Message('DTC Computer Science Camp Volunteer Application', sender = 'dtccscamp@gmail.com', recipients = [email])
            msg.body = "Hi! Thank you for submitting your volunteer application to DTC Computer Science Camps! We will send out another email in the next coming weeks with more information on your application and its next steps."
            mail.send(msg)
            color = "green"
        else:
            #if the email is not valid then send them this email 
            message = "There was a problem with your email. Please enter a valid email address"
            return render_template("info.html", message = message, color = color)
        
        return render_template("volunteers.html", message = message, color = color)


