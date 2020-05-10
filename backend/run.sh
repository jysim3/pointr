#!/bin/sh
if test $# != 2
then
    echo "Execute as $0 '[POINTR_EMAIL_PASSWORD]' '[POINTR_SERVER_SECRET]'"
    exit 1
fi

export POINTR_EMAIL_PASSWORD="$1"
export POINTR_SERVER_SECRET="$2"
export FLASK_APP=app.py 
# export FLASK_DEBUG=1
python3 -m flask run
