from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['GOOGLEMAPS_API_KEY'] = 'AIzaSyB0fP7H2kxhbvroTlVi43VlYLJ90QiLdZo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kokokok'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route("/home")
def bla():
    return render_template("home.html")

@app.route("/store")
def store():
    return render_template("store.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, password=password).first()
            if user is not None:
                flash('Successful login!')
                return redirect(url_for('home'))
            else:
                flash('No such user!')
                #return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash(f'Successfully created user {new_user.username}')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


if __name__ == "__main__":
    app.run(debug=True)
    