# myapp/util/assets.py

from flask_assets import Bundle, Environment
from .. import app

bundles = {

    'todos_js': Bundle(
        'js/lib/jquery-2.1.4.min.js',
        'js/todos.js',
        output='gen/todos.js'),

    'todos_css': Bundle(
        'css/todos.css',
        output='gen/home.css'),

}

assets = Environment(app)

assets.register(bundles)