import os
from flask import Flask, render_template, request, redirect
import pymysql
from werkzeug.utils import secure_filename

Upld_dir = 'static/uploads/'

manage = Flask(__name__)
manage.debug = True
manage.config['UPLOAD_FOLDER'] = Upld_dir

def connection():
    s = '127.0.0.1'
    d = 'masterlist' 
    u = 'root'
    p = ''
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn


@manage.route("/")
def main():
    mlists = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list")
    for row in cursor.fetchall():
        mlists.append({"id": row[0], "name": row[1], "age": row[2], "image": row[3]})
    conn.close()
    return render_template("list.html", mlists = mlists)


@manage.route("/add", methods = ['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html", mlist = {})
    if request.method == 'POST':

      
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(manage.config['UPLOAD_FOLDER'], filename))
        
        id = int(request.form["id"])
        name = request.form["name"]
        age = int(request.form["age"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO list (id, name, age, image) VALUES (%s, %s, %s, %s)", (id, name, age, filename))
        conn.commit()
        conn.close()
        return redirect('/')


@manage.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM list WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "age": row[2]})
        conn.close()
        return render_template("add.html", mlist = cr[0])

    if request.method == 'POST':
        name = str(request.form["name"])
        age = int(request.form["age"])
        cursor.execute("UPDATE list SET name = %s, age = %s WHERE id = %s", (name, age, id))
        conn.commit()
        conn.close()
        return redirect('/')

@manage.route('/delete/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM list WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')


if(__name__ == "__main__"):
    manage.run()