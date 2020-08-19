#!/bin/sh

if test -z "$POINTR_EMAIL_PASSWORD"; then
    echo "POINTR_EMAIL_PASSWORD not set up, run ./login.sh"
    return
fi

if test -z "$POINTR_SERVER_SECRET"; then
    echo "POINTR_SERVER_SECRET not set up, run ./login.sh"
    return
fi

if test -z "$SQLPassword"; then
    echo "SQLPassword not set up, run ./login.sh"
    return
fi

python3 -m nose2 --with-coverage -v tests.test_societies tests.test_events