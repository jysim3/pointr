FROM cypress/included:4.2.0


WORKDIR /e2e

RUN npm install -g npm
# copy both 'package.json' and 'package-lock.json' (if available)
COPY ./package*.json /e2e/

# install project dependencies
RUN npm install

WORKDIR /e2e
COPY . .

ENV PGHOST='db'
ENV PGUSER='postgres'
ENV PGDATABASE='pointrDB'
ENV PGPASSWORD='password'
ENV PGPORT=5432
