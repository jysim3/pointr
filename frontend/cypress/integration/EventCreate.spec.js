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

        })
    })
    beforeEach(()=> {
        cy.fixture('example.json').as('userData')
        cy.fixture('coverphoto.jpg').as('photo')
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
    it('Create Event', function() {
        cy.visit('/')
        cy.contains('Create').click()
        cy.url().should('contain','/create')

        cy.contains('Event title').next().type('hello')
        cy.contains('Location').next().type('my mum')
        cy.contains('Description').next().type('I would like to say hi to everyone here so I created an event')
        cy.get('select').select(this.userData.socID)

        cy.contains('Start Date').next().type('2021-08-15')
        cy.contains('Start Time').next().type('00:23')
        cy.contains('End Time').next().type('01:23')

        cy.contains('End Date').next().should('have.value','2021-08-15')
        cy.contains('End Date').next().type('2021-08-16')
        cy.contains('Tags').next().type('Party')
        cy.contains('Public').click()
        cy.get('@photo').then(fileContent => {
            cy.get('input[type="file"]').attachFile({
                fileContent: fileContent.toString(),
                fileName: 'testPicture.png',
                mimeType: 'image/jpg'
            });
        });

        cy.route('http://localhost:5000/api/event').as('createEventApi')

        cy.contains('Create Event').click()
        cy.location('pathname').should('contain','/event/')
        cy.contains('hello')
        cy.contains('Aug 15, 2021 12:23 AM - Aug 16, 2021 1:23 AM')
        cy.contains('my mum')
        cy.contains('Public')
        cy.contains('I would like to say')
        cy.get('.container').find('img').should('have.attr', 'src').should('include','/assets/images/')
    })
    it('Edit events', function() {
        cy.contains('edit').click()
        cy.contains('Edit event')
        const k = Date.now()
        cy.get('textarea').type(k)
        cy.contains('Edit Event').click()
        cy.contains(k)
        cy.contains('hello')
        cy.contains('Aug 15, 2021 12:23 AM - Aug 16, 2021 1:23 AM')
        cy.contains('my mum')
        cy.contains('Public')
    })
})