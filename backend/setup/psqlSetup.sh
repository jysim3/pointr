# IF POSTGRES NOT INSTALLED
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
sudo -u postgres createuser --superuser $USER
pip3 install psycopg2
pip3 install -r ../requirements.txt
