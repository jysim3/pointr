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
        })
    })
    beforeEach(function() {
        cy.fixture('example.json').as('userData')
        cy.fixture('coverphoto.jpg').as('photo')
        cy.get("@userData").then(function(v) {
          this.userData = v
          cy.login({"zID": v.zID, "password": v.password})
        })
    })
    it('Create Event', function() {
        cy.visit("/")
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
