from flask import Flask, request, render_template, session, redirect, url_for
from db import open_connection

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html", title="STutor")


@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    name = request.form['name']
    pwd = request.form['psw']
    user_type = request.form['user-type']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO stutor_table (name, email, password, user_type) VALUES(%s, %s, %s, %s)', (name, email, pwd, user_type))
    conn.commit()
    conn.close()

    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['psw']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM stutor_table WHERE email=%s AND password=%s',(email, pwd))
        account = cursor.fetchone()
    conn.commit()
    conn.close()
    if account:
        # session['loggedin'] = True
        # session['username'] = account[0]
        # session['user_type'] = account[3]
        user_type = account[3]
        if user_type == 'student':
            return render_template("student_home.html")
        elif user_type == 'tutor':
            return render_template("tutor_home.html")
    else:
        return "login failed"


@app.route("/login1")
def login1():    
    return render_template("login.html", title="login page")

@app.route("/register1")
def register1():    
    return render_template("signup.html", title="signup page")

@app.route("/tutor_home")
def tutor_home():
    return render_template("tutor_home.html", title="tutor home page")

@app.route("/student_home")
def student_home():
    return render_template("student_home.html", title="student page")


@app.route("/docs")
def docs():
    return render_template("page.html", title="docs page")


@app.route("/about")
def about():
    return render_template("page.html", title="about page")

# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
#    # Redirect to login page
#    return redirect('/login1')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
