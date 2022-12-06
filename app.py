from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL,MySQLdb
import bcrypt 

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan-2020"
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pkob'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config["UPLOAD_FOLDER"] = r'C:\Users\Padol\Desktop\pkob/'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
 
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
 
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")
 
@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':

      if 'file' not in request.files:
         return 'No file part'

      f = request.files['file']

      if f.filename == '':
         return 'No selected file'

      if f (f.filename):
         # f = request.files['file']
         filename = secure_filename(f.filename)
         f.save(app.config['UPLOAD_FOLDER'] + filename)
         return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)