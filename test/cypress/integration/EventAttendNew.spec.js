/// <reference types="cypress" />
import jwt from 'jsonwebtoken'
import moment from 'moment'

describe('Attend Event with new user', () => {
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
            cy.task('db', `delete from attend where "zID"='z0000010'; `)
            cy.task('db', `delete from staff where "zID"='z0000010'; `)
            cy.task('db', `delete from users where "zID"='z0000010'; `)
        })
    })
    beforeEach(()=> {
        cy.fixture('example.json').as('userData')
        cy.fixture('coverphoto.jpg').as('photo')
        cy.get("@userData").then(function(v) {
          this.userData = v
        })
    })
    it('New user is able to attend', function() {
        cy.login({
          "zID": this.userData.zID,
          "password": this.userData.password,
          "setStorage": false
        }).then(token => cy.request({
            url: `${Cypress.env('api_server')}/api/event/attend/code?eventID=AAAAF`,
            headers: {
                'Authorization': token
            }
        })).its('body').then(data => {
            expect(data).to.include.keys('data');
            expect(data.data).to.include.keys('code');
            return data.data['code'];
        }).then(code => {
            cy.visit('/event/AAAAF')
            const details = {
              code: code,
              zID: 'z0000010',
              firstName: 'first',
              lastName: 'last',
              password: 'asdfjkl;',
              repeatPassword: 'asdfjkl;',
            }
            for (const name in details) {
              cy.get(`input[name=${name}]`).type(details[name])
              cy.get(`input[name=${name}]`).should('have.value', details[name])
            }
            cy.get('.btn').contains('Sign as').click()
        })
    })
    it('Attendance only count if new user activates', function() {
        cy.login({
          "zID": this.userData.zID,
          "password": this.userData.password,
          "setStorage": false
            }).then(token => cy.request({
                url: `${Cypress.env('api_server')}/api/event/attend?eventID=AAAAF`,
                headers: {
                    'Authorization': token
                }
            })).its('body').then(data => {
                expect(data).to.include.keys('data');
                expect(data.data).to.have.length(0)

                return data.data
        }).then(() => {
          var token = jwt.sign({
              'zID':'z0000010',
              "permission": 0,
              "activation": 0,
              "type": "activation"
          }, Cypress.env('secret'));
          cy.log(token)
          cy.visit('/activate/' + token)
          cy.contains('Thanks for activating your account', {timeout: 10000})
        })
        cy.login({
          "zID": this.userData.zID,
          "password": this.userData.password,
          "setStorage": false
            }).then(token => cy.request({
                url: `${Cypress.env('api_server')}/api/event/attend?eventID=AAAAF`,
                headers: {
                    'Authorization': token
                }
            })).its('body').then(data => {
                expect(data).to.include.keys('data');
                expect(data.data).to.have.length(1)

                return data.data
            })

    })
    it('Old user is able to attend with login', function() {
        cy.task('db', `delete from attend where "zID"='z0000010'; `)
        cy.login({
          "zID": this.userData.zID,
          "password": this.userData.password,
          "setStorage": false
        }).then(token => cy.request({
            url: `${Cypress.env('api_server')}/api/event/attend/code?eventID=AAAAF`,
            headers: {
                'Authorization': token
            }
        })).its('body').then(data => {
            expect(data).to.include.keys('data');
            expect(data.data).to.include.keys('code');
            return data.data['code'];
        }).then(code => {
            cy.visit('/event/AAAAF')
            const details = {
                code: code,
                zID: 'z0000010',
                password: 'asdfjkl;',
            }
            cy.contains('Log').click()
            for (const name in details) {
                cy.get(`input[name=${name}]`).type(details[name])
                cy.get(`input[name=${name}]`).should('have.value', details[name])
            }
            cy.get('.btn').contains('Sign as').click()
        })
    })
    it('checking attendance', function() {
        cy.wait(2000)
        cy.login({
          "zID": this.userData.zID,
          "password": this.userData.password,
          "setStorage": false
          }).then(token => cy.request({
              url: `${Cypress.env('api_server')}/api/event/attend?eventID=AAAAF`,
              headers: {
                  'Authorization': token
              }
          })).its('body').then(data => {
              expect(data).to.include.keys('data');
              expect(data.data).to.have.length(1)

              return data.data
          })

    })
})
