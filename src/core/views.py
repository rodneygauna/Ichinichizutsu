'''
    website/users/views.py
'''

from flask import render_template, Blueprint
from flask_login import login_required


core = Blueprint('core', __name__)


@core.route('/', methods=['GET'])
def index():
    '''Route: Index page'''
    return render_template('index.html', title='Ichi-Nichi Zutsu')


@core.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    '''Route: Todo page'''
    return render_template('todos.html', title='Ichi-Nichi Zutsu')
