from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app, version='0.02', title='Pointr backend',
    description='Backend for pointr web servers',
)

from namespaces.event import api as event
from namespaces.stats import api as stats
from namespaces.user import api as user
from namespaces.auth import api as auth
from namespaces.soc import api as soc
from namespaces.other import api as other

api.add_namespace(event, path='/api/event')
api.add_namespace(stats, path='/api/stats')
api.add_namespace(user, path='/api/user')
api.add_namespace(auth, path='/api/auth')
api.add_namespace(soc, path='/api/soc')
api.add_namespace(other, path='/api/other')

CORS(app)

def main():
    app.run()

if __name__ == '__main__':
    main()
