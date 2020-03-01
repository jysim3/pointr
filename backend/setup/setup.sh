# FOR SETTING UP THE PSQL SERVER
sudo service postgresql start > /dev/null 2>&1
dropdb pointrDB 
createdb pointrDB 
psql pointrDB -f setup.sql 
python3 init.py