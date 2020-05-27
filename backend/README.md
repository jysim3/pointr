# Backend Documentation

## Assumptions:
* PostgreSQL Installed On Your Machine (`sudo apt-get install postgresql`)
* Python3 >= 3.6 (`sudo apt-get install python3` for Debian-based distros)
* All dependencies listed in [`requirements.txt`](requirements.txt) installed (`pip3 install -r requirements.txt`)
* Run the `setup/psqlSetup.sh` script to install the other dependencies you might need

## Before starting Flask
* Start the Postgres Server
```
sudo service postgresql start
```
* If running this project for the first time
```
createdb pointrDB
```

## To run the Flask server
```
python3 run.py [password used for pointr's email][password for your local postgres account] [secret key for JWTs]
```
* If you don't know what your postgres account is, you could always do
```
psql [any local DB]
$ \du
```
* If you don't know what your postgres password is, you could always do
```
psql [any local DB]
$ ALTER USER postgres WITH PASSWORD 'somePassword';
```
Note that `postgres` is the default postgresql account
