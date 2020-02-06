# IF POSTGRES NOT INSTALLED
# sudo apt-get install postgresql
# sudo apt-get install python-psycopg2
# sudo apt-get install libpq-dev

# FOR SETTING UP THE PSQL SERVER
sudo service postgresql start
dropdb pointrDB
createdb pointrDB
psql pointrDB -f setup.sql
python3 init.py