from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_user, login_required, logout_user, current_user
from app import create_app
from app.forms import TodoForm, DeleteTodoForm
from app.mongodb_service import get_todos, put_todo, delete_todo

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

@app.route('/hello', methods=['GET','POST'])
@login_required
def hello_world():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form
    }
    
    if todo_form.validate_on_submit():
        put_todo(todo_form.description.data, username)
        flash('Tu tarea se creo con éxito')
        return redirect(url_for('hello_world'))
        
    return render_template('hello.html', **context)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(todo_id, user_id)
    
    return redirect(url_for('hello_world'))
    
if __name__ == '__main__':
    app.run()
    
# flask run
# set FLASK_APP=main.py
# set FLASK_DEBUG=1
# set $FLASK_ENV=development