/// <reference types="cypress" />

import jwt from 'jsonwebtoken'
describe('Registering and login', () => {
    before(() => {
        cy.task('db', `delete from attend where "zID"='z5161631'; `)
        cy.task('db', `delete from staff where "zID"='z5161631'; `)
        cy.task('db', `delete from users where "zID"='z5161631'; `)
    })

    beforeEach(() => {
        cy.server()
        cy.fixture('example.json').as('userData')
        cy.route('/api/*').as('api')
    })
  it('Navigate to login/register', function() {
    cy.visit('/')
    cy.contains('Sign in').click()
    cy.url().should('contain', '/signin')
    cy.get('.loader-wrap').should('not.be.visible')

    cy.contains('Sign up here').click()
    cy.url().should('contain', '/signup')
    cy.contains('Join Pointr')

  })
  it('Register', function() {
    cy.visit('/signup')
    cy.get('input[name=zID]').type(this.userData.zID)
    cy.get('input[name=zID]').should('have.value', this.userData.zID)

    cy.get('input[name=firstName]').type(this.userData.firstName)
    cy.get('input[name=firstName]').should('have.value', this.userData.firstName)

    cy.get('input[name=lastName]').type(this.userData.lastName)
    cy.get('input[name=lastName]').should('have.value', this.userData.lastName)

    cy.get('input[name=password]').type(this.userData.password)
    cy.get('input[name=password]').should('have.value', this.userData.password)

    cy.get('input[name=repeatPassword]').type(this.userData.password)
    cy.get('input[name=repeatPassword]').should('have.value', this.userData.password)

    // cy.get('input[name=discord]').type(this.userData.discord)
    // cy.get('input[name=discord]').should('have.value', this.userData.discord)

    cy.get('.btn').contains('Sign Up').click()
    cy.url().should('contain','sendActivationEmail')

    expect(localStorage.getItem('token')).to.be.null
  })
  it('login requires activation', function() {
      cy.visit('/signin')
    cy.get('input[name=zID]').type(this.userData.zID)
    cy.get('input[name=zID]').should('have.value', this.userData.zID)

    cy.get('input[name=password]').type(this.userData.password)
    cy.get('input[name=password]').should('have.value', this.userData.password)

    cy.get('.btn').contains('Sign In').click()

    cy.url().should('contain','sendActivationEmail')
  })
  it('activating', function() {
    var token = jwt.sign({
        'zID':'z5161631',
        "permission": 0,
        "activation": 0,
        "type": "activation"
    }, Cypress.env('secret'));
    cy.log(token)
    cy.visit('/activate/' + token)
    cy.contains(this.userData.zID)
    cy.contains('Thanks for activating your account', {timeout: 10000})
  })
  it('login', function() {
      cy.visit('/signin')
    cy.get('input[name=zID]').type(this.userData.zID)
    cy.get('input[name=zID]').should('have.value', this.userData.zID)

    cy.get('input[name=password]').type(this.userData.password)
    cy.get('input[name=password]').should('have.value', this.userData.password)

    cy.get('.btn').contains('Sign In').click()

    cy.location().should(loc => {
        expect(loc.pathname).to.eq('/')
        expect(localStorage.getItem('token')).to.exist
    })

  })
  it('Continue after logging in', function() {
    localStorage.setItem('token','')
    cy.visit('/society/asdf')
    cy.location('pathname').should('include','signin')
    cy.get('input[name=zID]').type(this.userData.zID)
    cy.get('input[name=password]').type(this.userData.password)
    cy.get('.btn').contains('Sign In').click()
    cy.location('pathname').should('eq','/404')
  })
  it('Reseting password', function() {
    cy.visit('/forgotPassword')
    cy.get('input[name=zID]').type(this.userData.zID)
    cy.get('.btn').contains('Reset Password').click()
    cy.get('body').should('contain','Success')
    var token = jwt.sign({
        'zID':'z5161631',
        "permission": 0,
        "activation": 0,
        "type": "forgot"
    }, Cypress.env('secret'));
    cy.log(token)
    cy.visit('/reset/' + token)
    cy.get('input[name=password]').type('12345678')
    cy.get('input[name=repeatPassword]').type('12345678')
    cy.get('.btn').contains('Reset').click()
    cy.request('POST',`${Cypress.env('api_server')}/api/auth/login`, {
        "zID": this.userData.zID,
        "password": '12345678'
    }).its('body').then(data => {
        expect(data).to.include.keys('data')
        expect(data.data).to.have.key('token')
        localStorage.setItem('token', data.data['token'])
    })
    cy.visit('/reset/' + token)
    cy.get('input[name=password]').type(this.userData.password)
    cy.get('input[name=repeatPassword]').type(this.userData.password)
    cy.get('.btn').contains('Reset').click()
  })
})
