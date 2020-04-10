module.exports = {
  apps : [{
    name: 'front end',
    script: "./node_modules/@vue/cli-service/bin/vue-cli-service.js",
    args: "serve",
    cwd: './frontend',
    env: {
      "NODE_ENV": "test",
    },
  },
  {
    name: 'back end',
    script: 'app.py',
    cwd: './backend',
    watch: true,
    interpreter: "/usr/bin/python3",
    env: {
      "FLASK_APP": "app.py",
      "FLASK_ENV": "test",
    },
  }
  ]

};