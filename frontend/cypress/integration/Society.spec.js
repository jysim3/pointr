/// <reference types="cypress" />
import moment from 'moment'

describe('Society', () => {
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

        cy.exec(
            "echo INSERT INTO EVENTS(id, name, start, \"end\",description, \"hasQR\",\"hasAccessCode\", \"hasAdminSignin\", status) VALUES " +
            "('AAAAF', 'Monitored well-modulated support', TIMESTAMP '2019-07-04 04:57:44+10', TIMESTAMP '2020-12-27 07:32:48+11', 'in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh', 't', 't', 't', 2); | psql pointrDB")
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
    })
    it('Society Page', function() {
        cy.visit('/event/AAAAF')
    })
})
