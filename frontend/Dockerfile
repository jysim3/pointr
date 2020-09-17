FROM node:lts-alpine

# RUN npm install -g @vue/cli-service-global@4.5.6
# make the 'app' folder the current working directory
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# copy both 'package.json' and 'package-lock.json' (if available)
COPY ./package*.json /app/

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

EXPOSE 8080

# build app for production with minification
ENTRYPOINT ["npm", "run"]
CMD ["serve"]
