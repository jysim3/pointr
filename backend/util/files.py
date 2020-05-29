from werkzeug.utils import secure_filename
from flask import request, abort
import os
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'bitmap', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# NOTE: File is the object received from the request, filename is the socID/zID or whatever else we want to call the file
def uploadImages(file, filename = None):
    from app import app
    if file.filename == '':
        return "Invalid File Name"

    # Generate a 256 bit UUID file name (2 128 bit uuids combined)
    filename = str(uuid.uuid4().hex) + str(uuid.uuid4().hex) + "."
    filename = filename + str(file.filename).rsplit('.', 1)[1].lower()

    try:
        file.save(app.config['UPLOAD_FOLDER'] + filename)
    except IOError:
        return "Upload Folder Not Initialised"
    except Exception as e:
        return str(e)

    # On Success, returns path and 0, check for tuple
    return f"/assets/images/{filename}", 0