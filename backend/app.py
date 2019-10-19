import Flask

app = Flask(__name__)

# use format /api/xxxx
app.route('/api/', methods=['POST'])
def x(h):
    return json.dumps({'code':200})

