from flask import render_template, session, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm

from . import auth
from app.mongodb_service import get_user, put_user
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc: 
            if check_password_hash(user_doc['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello_world'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('El usuario no existe')
            
        return redirect(url_for('index'))
    
    return render_template('login.html', **context)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        
        user_doc = get_user(username)
        
        if user_doc:
            flash('El usuario ya existe')
        else:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            put_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')
            return redirect(url_for('hello_world'))
        
    return render_template('signup.html', **context)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    
    return redirect(url_for('auth.login'))