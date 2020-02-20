# FOR SETTING UP THE PSQL SERVER
sudo service postgresql start
dropdb pointrDB
createdb pointrDB
psql pointrDB -f setup.sql
python3 init.py
