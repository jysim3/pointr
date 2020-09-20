// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

import 'cypress-file-upload';
Cypress.Commands.add("login", ({zID, password, setStorage = true}) => {
  return cy.request('POST',`${Cypress.env('api_server')}/api/auth/login`, {
    "zID": zID,
    "password": password
  }).its('body').then(data => {
    expect(data).to.include.keys('data')
    expect(data.data).to.have.key('token')
    return data.data['token']
  }).then(function(token) {
    if (setStorage) {
      window.localStorage.setItem('token', token)
    }
    return token
  })
})
