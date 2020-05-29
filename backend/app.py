from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restx import Api
import os
from apscheduler.schedulers.background import BackgroundScheduler
from util.general import tick
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app, version='3.0.1', title='Pointr backend',
    description='Backend for pointr.live',
)

app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ.get('SQLPassword')}@localhost/pointrDB"
db = SQLAlchemy(app)

# FIXME: Change this to production when we relaunch pointr
app.config['ENV'] = 'development'

from namespaces.auth import api as auth
from namespaces.event import api as event
from namespaces.user import api as user
from namespaces.society import api as soc

api.add_namespace(auth, path='/api/auth')
api.add_namespace(event, path='/api/event')
api.add_namespace(user, path='/api/user')
api.add_namespace(soc, path='/api/society')

if (app.config['ENV'] == 'development'):
    @app.route('/assets/images/<path:path>')
    def send_images(path):
            return send_from_directory('../assets/images/', path)

if (app.config['ENV'] == 'development'):
    app.config['UPLOAD_FOLDER'] = f"{os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))}/assets/images/"
elif (app.config['ENV'] in ['production','test']):
    app.config['UPLOAD_FOLDER'] = "/var/www/static/assets/images/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if (os.path.exists(app.config['UPLOAD_FOLDER']) == False):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def updateAccessCodes():
    # Added a background scheduler to update access codes for all events that are currently running
    tick()

# scheduler = BackgroundScheduler(daemon=True)
# scheduler.add_job(updateAccessCodes, trigger='interval', seconds=20)
# scheduler.start()

CORS(app)
