# Working with the frontend

First have [Node.js](https://nodejs.org/en/) installed. You can check this by `node -v`. 

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Run your tests
Note: remember to insert jwt secret to cypress.json
```
npm run test
```

# Windows WSL

If you are using WSL, you can use this hacky way to run tests

```
powershell.exe ./node_modules/.bin/cypress install
powershell.exe ./node_modules/.bin/cypress run
```