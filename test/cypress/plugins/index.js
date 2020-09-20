/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

/**
 * @type {Cypress.PluginConfig}
 */
const db = require('./db.js')

module.exports = (on, config) => {
  require('cypress-terminal-report/src/installLogsPrinter')(on);
  on('task', {
    'db': db.db,
    'db:user': db.createUser,
    'db:event': db.createEvent,
    'db:soc': db.createSoc,
    'log': e => {
      console.log(e)
      return null
    }
  })
  // `on` is used to hook into various events Cypress emits
  // `config` is the resolved Cypress config
}
