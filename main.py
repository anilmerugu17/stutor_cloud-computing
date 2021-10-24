from flask import Flask, request, render_template
from db import open_connection

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("signup.html", title="STutor")


@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    name = request.form['name']
    pwd = request.form['psw']
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO stutor_table (name, email, password) VALUES(%s, %s, %s)', (name, email, pwd))
    conn.commit()
    conn.close()

    return render_template("signup.html", name=name)


@app.route("/docs")
def docs():
    return render_template("page.html", title="docs page")


@app.route("/about")
def about():
    return render_template("page.html", title="about page")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
