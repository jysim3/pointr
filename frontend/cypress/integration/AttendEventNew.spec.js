/// <reference types="cypress" />

describe('New User Attend Events', () => {
    const eventID = "AEX12"
    const fields = 'id, name, start, "end", description, "hasQR", "hasAccessCode",  "hasAdminSignin", status'
    beforeEach(() => {
        cy.exec(
        `echo DELETE FROM events ` +
        `where "id"='${eventID}' | psql pointrDB`
        )
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
    })
    it('Visit event and login', function() {
        cy.exec(
        `echo INSERT INTO EVENTS(${fields}) VALUES ` +
        `(${eventID}, 'testEvent', now(), now(), 'description', 'f', 't', 't',2); | psql pointrDB`
        )
        cy.visit('/event/' + eventID)
        cy.location('pathname').should('eq','/event/'+eventID)
        // cy.get('.btn').contains('Sign as').click()
    })
    it('404', function() {
        cy.visit('/event/' + eventID)
        cy.location('pathname').should('eq','/404')
    })
})