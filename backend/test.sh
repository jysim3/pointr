#!/bin/sh

#!/bin/sh
if test $# != 3
then
    echo "Execute as $0 '[POINTR_EMAIL_PASSWORD]' '[POINTR_SERVER_SECRET]' '[SQLPassword]' "
    exit 1
fi

export POINTR_EMAIL_PASSWORD="$1"
export POINTR_SERVER_SECRET="$2"
export SQLPassword="$3"
export FLASK_APP=app.py 
# export FLASK_DEBUG=1
nose2 -v tests.test_societies tests.test_events