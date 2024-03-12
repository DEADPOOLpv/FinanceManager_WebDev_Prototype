from fin_web import app
from flask import render_template, redirect, url_for, flash, request
from fin_web.models import User, Expenses
from fin_web.forms import RegisterForm, LoginForm
from fin_web import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route("/signup")
def signup():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('homes'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('login.html', form=form)

@app.route("/signin")
def signin():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



@app.route("/add")
def adding():
    return render_template('add.html')

"""
@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']
    
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO expenses VALUES (NULL,  % s, % s, % s, % s, % s, % s)', (session['id'] ,date, expensename, amount, paymode, category))
    mysql.connection.commit()
    print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
    
    return redirect("/display")
"""
