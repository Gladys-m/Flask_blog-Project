from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user


posts = [
    {
        'Author':'Kingstone',
        'Title': 'The Wizard of Oz',
        'Content': 'Lopsum Gypsum'
    },
    {
        'Author':'Fahari',
        'Title': 'Nguvu ya roho',
        'Content': 'Lopsum Gypsum ipsam'
    }
]

@app.route("/")
def home():
    return render_template('Home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('About.html', title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account created!', 'success')
        return redirect(url_for('login'))
    return render_template('Register.html', title='register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Logged in Unsuccessful. Please check email or password', 'danger')
    return render_template('Login.html', title='login', form=form)
