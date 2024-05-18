import sqlite3

from flask import Flask, render_template, request, flash, redirect, Markup
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'cheneatsfood'
app.config['UPLOAD'] = './static'

#connects to the camps database
db = sqlite3.connect("food.db", check_same_thread = False)

with open('schema.sql') as f:
    db.executescript(f.read())

cur = db.cursor()


def get_db_connection():
    conn = sqlite3.connect('food.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    photos = conn.execute('SELECT * FROM cover').fetchall()
    return render_template("index.html", photos = photos)


@app.route("/cookbook")
def cookbook():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('cookbook.html', posts=posts)

@app.route("/recipe")
def recipe():
    """Show blog page"""
    recipeid = request.args.get("recipeid")

    if recipeid is None:
        return redirect("/cookbook")

    #retrieves title, date, blog text, and blog's image from the blog database with the given blog id 
    title = db.execute("SELECT title FROM recipes WHERE recipe_id = ?", [recipeid]).fetchone()[0]
    image = db.execute("SELECT imagesource FROM recipes WHERE recipe_id = ?", [recipeid]).fetchone()[0]
    content = db.execute("SELECT content FROM recipes WHERE recipe_id = ?", [recipeid]).fetchone()[0]

    return render_template("recipe.html", title = title, image = image, content = Markup(content))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/createrecipe/', methods=('GET', 'POST'))
def createrecipe():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        
        imagesource = request.files['file']  

        if not title:
            flash('Title is required!')
        elif not imagesource: 
            flash('Image is required!')
        elif not content:
            flash('Content is required!')
        else:
            if imagesource and allowed_file(imagesource.filename):
                filename = secure_filename(imagesource.filename)
                imagesource.save(os.path.join(app.config['UPLOAD'], filename))
                conn = get_db_connection()
                conn.execute('INSERT INTO recipes (title, imagesource, content) VALUES (?, ?, ?)',
                            (title, imagesource.filename, content))
                conn.commit()
                conn.close()
            return redirect('/')

    return render_template('createrecipe.html')

@app.route('/addphotos/', methods=('GET', 'POST'))
def gallery():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        
        imagesource = request.files['file']  

        if not imagesource: 
            flash('Image is required!')
        else:
            if imagesource and allowed_file(imagesource.filename):
                filename = secure_filename(imagesource.filename)
                imagesource.save(os.path.join(app.config['UPLOAD'], filename))
                conn = get_db_connection()
                conn.execute('INSERT INTO cover (imagesource) VALUES (?)',
                            (imagesource.filename, ))
                conn.commit()
                conn.close()
            return redirect('/')

    return render_template('addphotos.html')

@app.route('/createreview/', methods=('GET', 'POST'))
def createreview():
    return render_template('createreview.html')

@app.route('/reviews/')
def reviews():
    return render_template('reviews.html')