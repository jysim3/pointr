/// <reference types="cypress" />
import moment from 'moment'

describe('Society', () => {
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
            cy.task('db:user', {
              zID: "z0000000",
              password: "00000000",
              activated: true,
              superadmin: false,
            })
            cy.task('db:user', {
              zID: "z5161631",
              password: "asdfjkl;",
              activated: true,
              superadmin: true,
            })
            cy.task('db:event', { 
              eventDetails: {
                id: "AAAAF"
              },
              socID: v.socID
            })
        })
    })
    beforeEach(()=> {
        cy.fixture('example.json').as('userData')
        cy.get("@userData").then(v => {
          cy.login({"zID": v.zID, "password": v.password})
        })
        cy.server()
        cy.route('/api/*').as('api')
    })
    it('Edit society page', function() {
        cy.visit(`/society/${this.userData.socID}`)
        cy.contains('Admin Tools').click()
        cy.contains('Edit').click()
        const k = Date.now()
        cy.get('textarea').type(k)
        cy.contains('Submit').click()
        cy.contains(k)
    })
    it('Make admin', function() {
        cy.visit(`/society/${this.userData.socID}`)
        cy.contains('Admin Tools').click()
        cy.get('input[name=zID]').type("z0000000")
        cy.contains('Make admin').click()
        cy.login({
          "zID": 'z0000000',
          "password": '00000000',
          "setStorage": false
        }).then(token => cy.request({
            method: 'GET', 
            url: `${Cypress.env('api_server')}/api/user/societies`,
            headers: {
                'Authorization': token
            }
        })).its('body').then(data => {
            expect(data).to.include.keys('data')
            expect(data.data).to.include.key('admins')
            expect(data.data.admins[0].id).to.eq(this.userData.socID)
        })
    })
})
