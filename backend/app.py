from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restx import Api
import os
from apscheduler.schedulers.background import BackgroundScheduler
from util.general import tick
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app, version='1.0.1', title='Pointr backend',
    description='Backend for pointr.live',
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.environ.get('SQLPassword')}@localhost/pointrDB"
db = SQLAlchemy(app)

from namespaces.event import api as event
from namespaces.stats import api as stats
from namespaces.user import api as user
from namespaces.soc import api as soc
from namespaces.other import api as other
from namespaces.auth import api as auth
from namespacesRework.auth import api as authRework
from namespacesRework.event import api as eventRework
from namespacesRework.user import api as userRework
from namespacesRework.society import api as socRework

'''
api.add_namespace(event, path='/api/event')
api.add_namespace(stats, path='/api/stats')
api.add_namespace(user, path='/api/user')
api.add_namespace(soc, path='/api/soc')
api.add_namespace(other, path='/api/other')
api.add_namespace(auth, path='/api/auth')
'''
api.add_namespace(authRework, path='/api/rework/auth')
api.add_namespace(eventRework, path='/api/rework/event')
api.add_namespace(userRework, path='/api/rework/user')
api.add_namespace(socRework, path='/api/rework/society')

if (app.config['ENV'] == 'development'):
    @app.route('/assets/images/<path:path>')
    def send_images(path):
            return send_from_directory('../assets/images/', path)

    if (os.path.exists("../assets/images/") == False):
        os.mkdir("../assets")
        os.mkdir("../assets/images")

if (app.config['ENV'] == 'development'):
    app.config['UPLOAD_FOLDER'] = f"{os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))}/assets/images/"
elif (app.config['ENV'] in ['production','test']):
    app.config['UPLOAD_FOLDER'] = f"/var/www/static/assets/images/"
#app.config['UPLOAD_FOLDER'] = "../assets/images/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def updateAccessCodes():
    # Added a background scheduler to update access codes for all events that are currently running
    tick()

# scheduler = BackgroundScheduler(daemon=True)
# scheduler.add_job(updateAccessCodes, trigger='interval', seconds=20)
# scheduler.start()

CORS(app)
