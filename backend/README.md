# Backend Documentation


## EASIEST WAY TO START DEVELOPING BACKEND

1. Install Docker [here](https://docs.docker.com/engine/install/)
  * (For linux machine) Remember to follow through after the ["post-installation steps"](https://docs.docker.com/engine/install/linux-postinstall/)
2. Run `docker-compose up` and see the magic

Note: run `docker-compose up` in `./backend` for backend only

### How to use docker cheatsheet:

* We have docker containers _named_ `db` (the database) and `api` the backend.

* You can connect to either container using this:
`docker exec -it <container_name> bash`


* For example, to connect to database manually: 
```
your-machine~$ docker exec -it db bash
psql-container~$ psql -U postgres pointrDB 
password: password
```
* Check and change the credentials in docker-compose.yml

P.S. You can run __both__  the frontend and the backend if you run `docker-compose up` in the root directory


## Assumptions:
* PostgreSQL Installed On Your Machine (`sudo apt-get install postgresql`)
* Python3 >= 3.6 (`sudo apt-get install python3` for Debian-based distros)
* All dependencies listed in [`requirements.txt`](requirements.txt) installed (`pip3 install -r requirements.txt`)
* Run the `setup/psqlSetup.sh` script to install the other dependencies you might need (<b>IMPORTANT</b>)

## Before starting Flask
* Start the Postgres Server
```
sudo service postgresql start
```
* If running this project for the first time
```
createdb pointrDB
```

## Set up Environment Variables
Note: `cd` into the base backend directory first
Set up the environment variables
```
source ./login.sh [password used for pointr's email] [password for your local postgres account] [secret key for JWTs]
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
Note: `postgres` is the default postgresql account


## To run the Flask server
```
python3 run.py
```

## To migrate the database
```
. ./login.sh [POINTR_EMAIL_PASSWORD] [POINTR_SERVER_SECRET] [SQLPassword]
flask db init
flask db migrate
flask db upgrade
```
