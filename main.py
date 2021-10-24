from flask import Flask, request, render_template, session, redirect, url_for
from db import open_connection

app = Flask(__name__)

app.secret_key = '12345'

#for tutor list inside student pages comes from save in student profile
@app.route("/tutor_list", methods=['POST'])
def tutor_list():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM tutor_profile WHERE subject_name=%s',(subject_name))
        tutors = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("tutor_list.html", tutors = tutors)

#for student list inside tutor pages comes here from tutor profile
@app.route("/student_list", methods=['POST'])
def students_list():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM student_profile WHERE subject_name=%s',(subject_name))
        students = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("student_list.html", students = students)

#registrations route
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

#login route
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
        session['loggedin'] = True
        session['name'] = account[0]
        session['email'] = account[1]
        session['user_type'] = account[3]
        user_type = account[3]
        if user_type == 'student':
            return render_template("student_home.html")
        elif user_type == 'tutor':
            return render_template("tutor_home.html")
    else:
        return "login failed"


#tutor first edit profile page comes from register to here
@app.route("/tutor_home", methods=['POST'])
def tutor_home():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tutor_profile (subject_name, edu_level, pay_per_hour, email) VALUES(%s, %s, %s, %s)', (subject_name, edu_level, pay_per_hour, email))
    conn.commit()
    conn.close()

    return render_template("tutor_home.html", title="tutor home page")

#student first edit profile page comes from register to here 
@app.route("/student_home", methods=['POST'])
def student_home():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO student_profile (subject_name, edu_level, pay_per_hour,email) VALUES(%s, %s, %s, %s)', (subject_name, edu_level, pay_per_hour, email))
    conn.commit()
    conn.close()
    return render_template("student_home.html", title="student home page")


#index page, comes here when you enter the site
@app.route("/")
def homepage():
    return render_template("index.html", title="STutor")

#tutor login page comes here everytime tutor logs in
@app.route("/home_tutor")
def home_tutor():
    return render_template("index_tutor.html")
    
#student home page, comes here everytime student logs in. 
@app.route("/home_student")
def home_student():
    return render_template("index_student.html", title="Student home")

#goes to login page when clicked on top menu 
@app.route("/login1")
def login1():    
    return render_template("login.html", title="login page")

#goes to register page when clicked on top menu 
@app.route("/register1")
def register1():    
    return render_template("signup.html", title="signup page")

#logout route
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template("login.html")

# @app.route("/docs")
# def docs():
#     return render_template("page.html", title="docs page")


# @app.route("/about")
# def about():
#     return render_template("page.html", title="about page")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
