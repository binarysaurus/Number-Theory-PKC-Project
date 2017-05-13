from flask import Flask
from secrets import FLASKKEY

app = Flask(__name__)
app.config.from_object(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = FLASKKEY

import webapp.routes