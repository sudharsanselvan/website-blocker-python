from flask import Flask, render_template, flash, request, session, redirect, url_for
import mysql.connector
import datetime
import webbrowser

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['DEBUG'] = True


# ----------------- ROUTES -----------------

@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/BlockWebsite")
def BlockWebsite():
    return render_template('BlockWebsite.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    conn.close()
    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            conn.close()
            return render_template('AdminHome.html', data=data)
        else:
            error = 'Invalid credentials'
            return render_template('index.html', error=error)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['psw']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name1, gender1, age, email, pnumber, address, uname, password)
        )
        conn.commit()
        conn.close()

        return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = username

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE username=%s AND Password=%s", (username, password))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)
        else:
            session['uid'] = data[0]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb WHERE username=%s AND Password=%s", (username, password))
            data = cur.fetchall()
            conn.close()
            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    pid = session.get('uname')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE username=%s", (pid,))
    data = cur.fetchall()
    conn.close()
    return render_template('UserHome.html', data=data)


@app.route("/Search")
def Search():
    return render_template('Search.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        web = request.form['name']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM webtb WHERE website=%s", (web,))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            webbrowser.open(web)
            return redirect(url_for("Search"))
        else:
            alert = 'Website Blocked!'
            return render_template('goback.html', data=alert)


@app.route("/UnBlockWebsite")
def UnBlockWebsite():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
    cur = conn.cursor()
    cur.execute("SELECT * FROM webtb")
    data = cur.fetchall()
    conn.close()
    return render_template('UnBlockWebsite.html', data=data)


@app.route("/block", methods=['GET', 'POST'])
def block():
    if request.method == 'POST':
        name = request.form['name']
        ip = "127.0.0.1"

        with open(r"C:\Windows\System32\drivers\etc\hosts", "r+") as host:
            content = host.read()
            if name in content:
                alert = f"{name} is already blocked"
                return render_template('goback.html', data=alert)
            else:
                host.write(f"\n{ip}       {name}\n")

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO webtb (website) VALUES (%s)", (name,))
        conn.commit()
        conn.close()

        alert = 'Website Blocked!'
        return render_template('goback.html', data=alert)


@app.route("/Unblock")
def Unblock():
    website = request.args.get('id')
    i = website

    with open(r"C:\Windows\System32\drivers\etc\hosts", "r+") as host:
        content = host.read()
        if i in content:
            new_content = content.replace(i, "")
            host.seek(0)
            host.truncate()
            host.write(new_content)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM webtb WHERE website=%s", (website,))
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1websiteblock')
            cur = conn.cursor()
            cur.execute("SELECT * FROM webtb")
            data = cur.fetchall()
            conn.close()

            return render_template('UnBlockWebsite.html', data=data)
        else:
            alert = f"{i} has not been blocked"
            return render_template('goback.html', data=alert)


# ----------------- MAIN -----------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
