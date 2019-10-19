module.exports = {
  apps : [{
    name: 'front end',
    script: './frontend/server.js',
    watch: true,
  },
  {
	  name: 'back end',
	  script: 'init.py',
	  cwd: './backend',
	  watch: true,
	  interpreter: "/usr/bin/python3"
  }
  ]

};
