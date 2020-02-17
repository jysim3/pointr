# FOR SETTING UP THE PSQL SERVER
sudo service postgresql start
psql pointrDB -f setup.sql
python3 init.py