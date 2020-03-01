# FOR SETTING UP THE PSQL SERVER
sudo service postgresql start > /dev/null 2>&1
dropdb pointrDB > /dev/null 2>&1
createdb pointrDB 
psql pointrDB -f setup.sql > /dev/null
python3 init.py