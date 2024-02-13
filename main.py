from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_user, login_required, logout_user, current_user
from app import create_app
from app.forms import LoginForm
from app.mongodb_service import get_users, get_todos

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')

@app.route('/')
def index():
    # raise(Exception('500 error'))
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/hello', methods=['GET'])
@login_required
def hello_world():
    user_ip = session.get('user_ip')
    username = current_user.id
    
    context = {
        'user_ip': user_ip,
        'todos': get_todos(username),
        'username': username
    }
        
    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run()
    
# flask run
# set FLASK_APP=main.py
# set FLASK_DEBUG=1
# set $FLASK_ENV=development