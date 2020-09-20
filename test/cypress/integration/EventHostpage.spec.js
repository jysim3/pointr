
/// <reference types="cypress" />
import moment from 'moment'

describe('Event', () => {
    before(() => {

        cy.fixture('example.json').then(v => {
            cy.task('db:soc', {
              socID: v.socID,
              description: "Description of the society"
            })
            cy.task('db:user', {
              zID: "z5161631",
              password: "asdfjkl;",
              activated: true,
              superadmin: true,
            })
            cy.task('db',
            "insert into staff (\"zID\", \"socID\", rank) values " +
            `('z5161631', '${v.socID}', 1); `
            )
            cy.task('db:event', { 
              eventDetails: {
                id: "AAAAF"
              },
              socID: v.socID
            })
            cy.task('db',
                `delete from staff where "zID"='z0000000'; `
            )
        })
    })
    beforeEach(function() {
        cy.fixture('example.json').as('userData')
        cy.get("@userData").then(v => {
          this.userData = v
          cy.login({"zID": v.zID, "password": v.password})
        })
    })
    it('Check event attendance', function() {
        cy.visit('/society/'+this.userData.socID)
        cy.get('tr.link').click()
        let eventID = ''

        cy.location('pathname').then(v => {
            eventID = v.split('/')[2]
            for (let i = 0; i < 30; i++) {
                cy.task('db:user', {
                  zID: `z${(i+'').padStart(7,"0")}`,
                  password: "asdfjkl;",
                  activated: true,
                  superadmin: false,
                })
                cy.task('db',
                'insert into attend ("eventID", "zID", time, "additionalInfo") values ' +
                `('${eventID}','z${(i+'').padStart(7,"0")}', TIMESTAMP '2020-12-27 0${Math.floor(Math.random()*2)+5}:${Math.floor(Math.random()*60)}', '{}');`
                , {log: false})
            }
        })
        cy.wait(5000)
        cy.contains("refresh").click()
        cy.contains((15+'').padStart(7,"0"))
        cy.wait(5000)
        cy.contains("refresh").click()
        cy.contains((20+'').padStart(7,"0"))
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
    
    it('Attend Event', function() {
        cy.task('db:user', {
          "zID": 'z0000000',
          password: "00000000",
          activated: true,
          superadmin: false,
        })
        let eventID = ''

        cy.location('pathname').then(v => {
            eventID = v.split('/')[2]
        })
        cy.contains('PIN: ').invoke('text').then(text => {
            return  text.split(" ")[2]
        }).then(pin => {
            cy.request('POST',`${Cypress.env('api_server')}/api/auth/login`, {
                "zID": 'z0000000',
                "password": '00000000'
            }).its('body').then(data => {
                expect(data).to.include.keys('data')
                expect(data.data).to.have.key('token')
                localStorage.setItem('token', data.data['token'])
            })
            cy.visit(`/event/${eventID}?code=${pin}`)
            cy.contains("Sign as").click()
            cy.get('body').should('contain','Success!')
        })
    })
})
