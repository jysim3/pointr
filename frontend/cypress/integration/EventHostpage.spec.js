
/// <reference types="cypress" />
import moment from 'moment'

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
            cy.exec(
                `echo delete from attend where "eventID"='AAAAF'; | psql pointrDB`
            )
            cy.exec(
                `echo delete from events where "id"='AAAAF'; | psql pointrDB`
            )
            cy.exec(
                "echo INSERT INTO EVENTS(id, name, start, \"end\",description, \"hasQR\",\"hasAccessCode\", \"hasAdminSignin\", status,  privacy) VALUES " +
                "('AAAAF', 'Monitored well-modulated support', TIMESTAMP '2020-12-27 04:57:44+10', TIMESTAMP '2020-12-27 07:32:48+11', 'in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh', 't', 't', 't', 2,0); | psql pointrDB"
            )
            
            cy.exec(
                "echo INSERT INTO hosted(\"eventID\",\"socID\") VALUES " +
                `('AAAAF','${v.socID}'); | psql pointrDB`)
            

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
    it('Check event attendance', function() {
        cy.visit('/society/'+this.userData.socID)
        cy.get('tr.link').click()
        let eventID = ''

        cy.location('pathname').then(v => {
            eventID = v.split('/')[2]
            for (let i = 0; i < 30; i++) {
                cy.exec(
                'echo insert into attend ("eventID", "zID", time, "additionalInfo") values ' +
                `('${eventID}','z${(i+'').padStart(7,"0")}', TIMESTAMP '2020-12-27 0${Math.floor(Math.random()*2)+5}:${Math.floor(Math.random()*60)}', '{}');| psql pointrDB`
                , {log: false})
            }
        })
        cy.contains("refresh").click()
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
    
    it('Attend Event', function() {
        let eventID = ''

        cy.location('pathname').then(v => {
            eventID = v.split('/')[2]
        })
        cy.contains('PIN: ').invoke('text').then(text => {
            return  text.split(" ")[2]
        }).then(pin => {
            console.log(pin)

            cy.request('POST','http://localhost:5000/api/auth/login', {
                "zID": 'z0000000',
                "password": '00000000'
            }).its('body').then(data => {
                expect(data).to.include.keys('data')
                expect(data.data).to.have.key('token')
                localStorage.setItem('token', data.data['token'])
            })
            cy.visit(`/event/${eventID}?code=${pin}`)
            cy.contains("Sign as").click()
            cy.should('contain','Success!')
            
        })

    })
})