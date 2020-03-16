from flask import Flask
from flask_bootstrap import Bootstrap

from controller import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

app.register_blueprint(index_blueprint)
app.register_blueprint(activity_blueprint)
app.register_blueprint(device_management_blueprint)

bootstrap = Bootstrap(app)


