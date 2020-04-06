from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restx import Api
import os

app = Flask(__name__)
api = Api(app, version='1.0.0', title='Pointr backend',
    description='Backend for pointr.live',
)

from namespaces.event import api as event
from namespaces.stats import api as stats
from namespaces.user import api as user
from namespaces.soc import api as soc
from namespaces.other import api as other
from namespaces.auth import api as auth

api.add_namespace(event, path='/api/event')
api.add_namespace(stats, path='/api/stats')
api.add_namespace(user, path='/api/user')
api.add_namespace(soc, path='/api/soc')
api.add_namespace(other, path='/api/other')
api.add_namespace(auth, path='/api/auth')

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
    app.config['UPLOAD_FOLDER'] = f"/var/www/assets/images/"
#app.config['UPLOAD_FOLDER'] = "../assets/images/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CORS(app)

def main():
    app.run()

if __name__ == '__main__':
    main()
