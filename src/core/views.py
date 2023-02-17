'''
    website/users/views.py
'''

from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from src.core.forms import TodoForm
from src import db
from src.models import Todos


core = Blueprint('core', __name__)


@core.route('/', methods=['GET'])
def index():
    '''Route: Index page'''
    return render_template('index.html', title='Ichi-Nichi Zutsu')


@core.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    '''Route: Todo page'''
    if request.method == 'GET':
        todo_list = Todos.query.filter_by(user_id=current_user.id).all()
    return render_template('todos.html',
                           title='Ichi-Nichi Zutsu',
                           todo_list=todo_list)


@core.route('/todos/add', methods=['GET', 'POST'])
@login_required
def add_todo():
    '''Route: Add Todo page'''
    form = TodoForm()

    if form.validate_on_submit():
        todo = Todos(title=form.title.data,
                     description=form.description.data,
                     status=form.status.data,
                     user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('core.todos'))
    return render_template('add_todo.html',
                           title='Ichi-Nichi Zutsu',
                           form=form)
