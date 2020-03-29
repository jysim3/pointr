from werkzeug.utils import secure_filename
from flask import request, abort

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploadImages(file, filename = None):
    from app import app
    # TODO: If we make a decision on using images, add sql query down below
    if file.filename == '':
        return "Invalid File Name"

    # Some checks/sanitisation for the filename
    if not filename:
        if file and allowed_file(file.filename):
            filename = secure_filename(filename)
        else:
            return "Invalid file name"

    try:
        file.save(app.config['UPLOAD_FOLDER'] + filename)
    except IOError:
        return "Upload Folder Not Initialised"
    except Exception as e:
        return str(e)

    # On Success, returns path and 0, check for tuple
    return app.config['UPLOAD_FOLDER'] + filename, 0