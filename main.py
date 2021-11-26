from flask import Flask, request, render_template, session, redirect, url_for
from db import open_connection

app = Flask(__name__)

app.secret_key = '12345'


# index page, comes here when you enter the site
@app.route("/")
def homepage():
    return render_template("login.html", title="STutor")


# goes to login page when clicked on top menu
@app.route("/login1")
def login1():
    return render_template("login.html", title="login page")


# goes to register page when clicked on top menu
@app.route("/register1")
def register1():
    return render_template("signup.html", title="signup page")


# for tutor list inside student pages comes from save in student profile
@app.route("/tutor_list", methods=['POST'])
def tutor_list():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        cursor.execute(
            'INSERT INTO student_profile (subject_name, edu_level, pay_per_hour,email) VALUES(%s, %s, %s, %s)',
            (subject_name, edu_level, pay_per_hour, email))
    conn1.commit()
    conn1.close()
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM tutor_profile WHERE subject_name=%s AND edu_level=%s', (subject_name, edu_level))
        tutors = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("tutor_list.html", tutors=tutors)


# for student list inside tutor pages comes here from tutor profile
@app.route("/student_list", methods=['POST'])
def students_list():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        cursor.execute(
            'INSERT INTO tutor_profile (subject_name, edu_level, pay_per_hour, email) VALUES(%s, %s, %s, %s)',
            (subject_name, edu_level, pay_per_hour, email))
    conn1.commit()
    conn1.close()
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM student_profile WHERE subject_name=%s', subject_name)
        students = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("student_list.html", students=students)


# registrations route
@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    name = request.form['name']
    pwd = request.form['psw']
    user_type = request.form['user-type']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO stutor_table (name, email, password, user_type) VALUES(%s, %s, %s, %s)',
                       (name, email, pwd, user_type))
    conn.commit()
    conn.close()

    return render_template("login.html")


# logout route
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return render_template("login.html")


# login route
@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['psw']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM stutor_table WHERE email=%s AND password=%s', (email, pwd))
        account = cursor.fetchone()
    conn.commit()
    conn.close()
    if account:
        session['loggedin'] = True
        session['name'] = account[1]
        session['email'] = account[0]
        session['user_type'] = account[3]
        user_type = account[3]
        if user_type == 'student':
            conn1 = open_connection()
            with conn1.cursor() as cursor:
                cursor.execute('SELECT  T.subject_name, T.edu_level, T.pay_per_hour, T.email from tutor_profile T,'
                               ' student_profile S where S.email = %s and S.subject_name = T.subject_name '
                               'and S.edu_level = T.edu_level', session['email'])
                tutors = cursor.fetchall()
            conn1.commit()
            conn1.close()
            conn2 = open_connection()
            with conn2.cursor() as cursor:
                exists = cursor.execute('SELECT * FROM STUDENT_PROFILE WHERE email=%s', session['email'])
                if exists:
                    return render_template("tutor_list.html", tutors=tutors)
                else:
                    return render_template("student_home.html")
            conn2.commit()
            conn2.close()
        elif user_type == 'tutor':
            conn1 = open_connection()
            with conn1.cursor() as cursor:
                cursor.execute('SELECT  S.subject_name,S.edu_level,S.pay_per_hour,S.email from student_profile S,'
                               ' tutor_profile T where T.email = %s and T.subject_name = S.subject_name '
                               'and T.edu_level = S.edu_level', session['email'])
                students = cursor.fetchall()
            conn1.commit()
            conn1.close()
            conn2 = open_connection()
            with conn2.cursor() as cursor:
                exists = cursor.execute('SELECT * FROM TUTOR_PROFILE WHERE email=%s', session['email'])
                if exists:
                    return render_template("student_list.html", students=students)
                else:
                    return render_template("tutor_home.html")
                conn2.commit()
                conn2.close()
    else:
        return "login failed"


# tutor first edit profile page comes from register to here
@app.route("/tutor_home", methods=['POST'])
def tutor_home():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO tutor_profile (subject_name, edu_level, pay_per_hour, email) VALUES(%s, %s, %s, %s)',
            (subject_name, edu_level, pay_per_hour, email))
    conn.commit()
    conn.close()

    return render_template("tutor_home.html", title="tutor home page")


# student first edit profile page comes from register to here
@app.route("/student_home", methods=['POST'])
def student_home():
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO student_profile (subject_name, edu_level, pay_per_hour,email) VALUES(%s, %s, %s, %s)',
            (subject_name, edu_level, pay_per_hour, email))
    conn.commit()
    conn.close()
    return render_template("student_home.html", title="student home page")


# tutor login page comes here everytime tutor logs in
@app.route("/home_tutor")
def home_tutor():
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT  S.subject_name,S.edu_level,S.pay_per_hour,S.email from student_profile S,'
                       ' tutor_profile T where T.email = %s and T.subject_name = S.subject_name '
                       'and T.edu_level = S.edu_level', email)
        students = cursor.fetchall()
        conn.commit()
        conn.close()
        return render_template("student_list.html", students=students)


# student home page, comes here everytime student logs in.
@app.route("/home_student")
def home_student():
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT  T.subject_name, T.edu_level, T.pay_per_hour, T.email from tutor_profile T,'
                       ' student_profile S where S.email = %s and S.subject_name = T.subject_name '
                       'and S.edu_level = T.edu_level', email)
        tutors = cursor.fetchall()
        conn.commit()
        conn.close()
        return render_template("tutor_list.html", title="Student home", tutors=tutors)


# goes to student profile when clicked on profile page from student pages
@app.route("/student_profile")
def student_profile():
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT subject_name, edu_level, pay_per_hour FROM student_profile WHERE email=%s', email)
        student = cursor.fetchone()
    return render_template("student_profile.html", title="student profile page", student=student)


# goes to tutor profile when clicked on profile page from tutor pages
@app.route("/tutor_profile")
def tutor_profile():
    email = session['email']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT subject_name, edu_level, pay_per_hour FROM tutor_profile WHERE email=%s', email)
        tutor = cursor.fetchone()
    return render_template("tutor_profile.html", title="tutor profile page", tutor=tutor)


# From Student profile, when students edits his data and clicks on update my criteriaupdateStudentData
@app.route("/updateStudentData", methods=['POST'])
def update_student_profile():
    email = session['email']
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    conn = open_connection()
    with conn.cursor() as cursor:
        exists = cursor.execute('SELECT * FROM student_profile where email=%s', email)
        if exists:
            cursor.execute(
                'UPDATE student_profile set subject_name = %s, edu_level = %s, pay_per_hour = %s where email = '
                '%s', (subject_name, edu_level, pay_per_hour, email))
        else:
            cursor.execute(
                'INSERT INTO student_profile (subject_name, edu_level, pay_per_hour,email) VALUES(%s, %s, %s, %s)',
                (subject_name, edu_level, pay_per_hour, email))
        conn.commit()
        conn.close()
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        cursor.execute('SELECT * FROM tutor_profile WHERE subject_name=%s AND edu_level=%s', (subject_name, edu_level))
        tutors = cursor.fetchall()
    conn1.commit()
    conn1.close()
    return render_template("tutor_list.html", tutors=tutors)


# From Student profile, when students edits his data and clicks on update my criteriaupdateStudentData
@app.route("/updateTutorData", methods=['POST'])
def update_tutor_profile():
    email = session['email']
    subject_name = request.form['subject_name']
    edu_level = request.form['edu_level']
    pay_per_hour = request.form['pay_per_hour']
    conn = open_connection()
    with conn.cursor() as cursor:
        exists = cursor.execute('SELECT * FROM tutor_profile where email=%s', email)
        if exists:
            cursor.execute('UPDATE tutor_profile set subject_name = %s, edu_level = %s, pay_per_hour = %s where email = '
                               '%s', (subject_name, edu_level, pay_per_hour, email))
        else:
            cursor.execute(
                'INSERT INTO tutor_profile (subject_name, edu_level, pay_per_hour,email) VALUES(%s, %s, %s, %s)',
                (subject_name, edu_level, pay_per_hour, email))
        conn.commit()
        conn.close()
    conn1 = open_connection()
    with conn1.cursor() as cursor:
        cursor.execute('SELECT * FROM student_profile WHERE subject_name=%s AND edu_level=%s',
                       (subject_name, edu_level))
        students = cursor.fetchall()
    conn1.commit()
    conn1.close()
    return render_template("student_list.html", students=students)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
