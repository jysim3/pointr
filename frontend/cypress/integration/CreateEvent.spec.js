/// <reference types="cypress" />

describe('Event', () => {
    before(() => {

        cy.exec(
     "echo insert into staff (\"zID\", \"socID\", rank) values " +
     "('z5161631', (select id from societies limit 1), 1); | psql pointrDB"
        )
    })
    beforeEach(()=> {
        cy.fixture('example.json').as('userData')
        cy.get("@userData").then(v => {
            cy.request('POST','http://localhost:5000/api/auth/login', {
                "zID": v.zID,
                "password": v.password
            }).its('body').then(data => {
                expect(data).to.include.keys('data')
                expect(data.data).to.have.key('token')
                localStorage.setItem('token', data.data['token'])
            })
        })
        cy.server()
        cy.route('/api/*').as('api')
        // localStorage.setItem('')
    })
    it('Attend Event', function() {
        cy.exec(
     "echo DELETE FROM attend where \"zID\"='z5161631'; | psql pointrDB"
        )
        cy.visit('/')
        cy.contains('Browse events')
        cy.get('.event-cards').last().click()
        cy.url().should('contain','/event')
        cy.contains('Sign attendance').should('be.visible')
        cy.get('.btn').contains(`Sign as (${this.userData.zID})`).click()
        cy.contains('Success')
    })
    it('Create Event', function() {
        cy.visit('/')
        cy.contains('Create').click()
        cy.url().should('contain','/create')

        cy.contains('Event title').next().type('hello')
        cy.contains('Location').next().type('my mum')
        cy.contains('Description').next().type('I would like to say hi to everyone here so I created an event')
        cy.get('option').invoke('val').then(v => {
        cy.exec(
     `echo DELETE FROM events where "socID"='${v}'; | psql pointrDB`
        )
            cy.get('select').select(v)
        })

        cy.contains('Start Date').next().type('2020-08-15')
        cy.contains('Start Time').next().type('00:23')
        cy.contains('End Time').next().type('01:23')

        cy.contains('End Date').next().should('have.value','2020-08-15')
        cy.contains('End Date').next().type('2020-08-16')

        cy.route('http://localhost:5000/api/event').as('createEventApi')

        cy.contains('Create Event').click()
        cy.location('pathname').should('contain','/event/')
        cy.contains('Welcome to hello')


    })
})