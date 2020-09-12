import jwt from 'jsonwebtoken'
/// <reference types="cypress" />
import moment from 'moment'

describe('Attend Event with new user', () => {
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
            cy.exec( `echo delete from hosted where "socID"='${v.socID}'; | psql pointrDB`)
            cy.exec( `echo delete from attend where "eventID"='AAAAF'; | psql pointrDB`)
            cy.exec( `echo delete from events where "id"='AAAAF'; | psql pointrDB`)
            cy.exec(
                "echo INSERT INTO EVENTS(id, name, start, \"end\",description, \"hasQR\",\"hasAccessCode\", \"hasAdminSignin\", status,  privacy) VALUES " +
                "('AAAAF', 'Monitored well-modulated support', TIMESTAMP '2020-12-27 04:57:44+10', TIMESTAMP '2020-12-27 07:32:48+11', 'in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh', 't', 't', 't', 2,0); | psql pointrDB"
            )
            cy.exec( `echo delete from attend where "zID"='z0000010'; | psql pointrDB`)
            cy.exec( `echo delete from staff where "zID"='z0000010'; | psql pointrDB`)
            cy.exec( `echo delete from users where "zID"='z0000010'; | psql pointrDB`)
            cy.exec(
                "echo INSERT INTO hosted(\"eventID\",\"socID\") VALUES " +
                `('AAAAF','${v.socID}'); | psql pointrDB`
            )

        })
    })
    beforeEach(()=> {
        cy.fixture('example.json').as('userData')
        cy.fixture('coverphoto.jpg').as('photo')
        cy.server()
        cy.route('/api/*').as('api')
        // localStorage.setItem('')
    })
    it('New user is able to attend', function() {
        cy.get("@userData").then(v => {
            return cy.request('POST','http://localhost:5000/api/auth/login', {
                "zID": v.zID,
                "password": v.password
            }).its('body').then(data => {
                expect(data).to.include.keys('data');
                expect(data.data).to.have.key('token');
                return data.data['token'];
            }).then(token => cy.request({
                url: 'http://localhost:5000/api/event/attend/code?eventID=AAAAF',
                headers: {
                    'Authorization': token
                }
            })).its('body').then(data => {
                expect(data).to.include.keys('data');
                expect(data.data).to.include.keys('code');
                return data.data['code'];
            })
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
    it('activating', function() {
        cy.get("@userData").then(v => {
            return cy.request('POST','http://localhost:5000/api/auth/login', {
                    "zID": v.zID,
                    "password": v.password
                }).its('body').then(data => {
                    expect(data).to.include.keys('data');
                    expect(data.data).to.have.key('token');
                    return data.data['token'];
                }).then(token => cy.request({
                    url: 'http://localhost:5000/api/event/attend?eventID=AAAAF',
                    headers: {
                        'Authorization': token
                    }
                })).its('body').then(data => {
                    expect(data).to.include.keys('data');
                    expect(data.data).to.have.length(0)

                    return data.data
                })
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
        }).then(() => cy.get("@userData")).then(v => {
            cy.request('POST','http://localhost:5000/api/auth/login', {
                    "zID": v.zID,
                    "password": v.password
                }).its('body').then(data => {
                    expect(data).to.include.keys('data');
                    expect(data.data).to.have.key('token');
                    return data.data['token'];
                }).then(token => cy.request({
                    url: 'http://localhost:5000/api/event/attend?eventID=AAAAF',
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
})