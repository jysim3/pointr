/// <reference types="cypress" />

describe('Event', () => {
    before(() => {

        cy.fixture('example.json').then(v => {

            const description = 'Description Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat'
            cy.exec(
            "echo INSERT INTO SOCIETIES(id, description, name, type) VALUES " +
            `('${v.socID}', '${description}', 'Test Soc', 0); | psql pointrDB`
            )

            cy.exec(
            "echo insert into staff (\"zID\", \"socID\", rank) values " +
            `('z5161631', '${v.socID}', 1); | psql pointrDB`
            )
            cy.exec(
                `echo delete from hosted where "socID"='${v.socID}'; | psql pointrDB`
            )

        })
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
        cy.wait(1000)
    })
    it('Create Event', function() {
        cy.visit('/')
        cy.contains('Create').click()
        cy.url().should('contain','/create')

        cy.contains('Event title').next().type('hello')
        cy.contains('Location').next().type('my mum')
        cy.contains('Description').next().type('I would like to say hi to everyone here so I created an event')
        cy.get('select').select(this.userData.socID)

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
    it('Check event attendance', function() {
        cy.visit('/society/'+this.userData.socID)
        cy.get('tr.link').click()
        let eventID = ''
        cy.location('pathname').then(v => {
            eventID = v.split('/')[2]
            for (let i = 0; i < 30; i++) {
                cy.exec(
                'echo insert into attend ("eventID", "zID", time, "additionalInfo") values ' +
                `('${eventID}','z${(i+'').padStart(7,"0")}', now(), '{}');| psql pointrDB`
                , {log: false})
            }
        })
        for (let i = 0; i < 30; i++) {
            cy.contains((i+'').padStart(7,"0"))
        }
    })
    it('Delete Attendance', function() {
        cy.contains('z0000000').parent().parent().contains('delete').click()
        cy.should('not.contain','z0000000')
    })
    it('Download csv functions', function() {
        cy.get('input[type=checkbox]').first().click()
        cy.get('table').should('not.contain','Name')
        cy.contains('Download csv').click()
    })
    
})