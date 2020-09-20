
const { Client } = require('pg')
const SHA256 = require("crypto-js/sha256");
const client = new Client()
client.connect()

const db = async query => {
  try {
    await client.query(query)
    return null
  } catch (error) {
    return null
  }
}
const createEvent = async ({socID, eventDetails}) => {
  try {
    await createSoc({socID, description:"description lmao"})
    await client.query(`delete from hosted where "socID"='${socID}'; `)
    await client.query(`delete from attend where "eventID"='${eventDetails.id}'; `)
    await client.query(`delete from events where "id"='${eventDetails.id}'; `)
    await client.query(
            "INSERT INTO EVENTS(id, name, start, \"end\",description, \"hasQR\",\"hasAccessCode\", \"hasAdminSignin\", status, privacy) VALUES " +
            `('${eventDetails.id}', 'Monitored well-modulated support', TIMESTAMP '2019-12-27 00:57:44+11', TIMESTAMP '2020-12-27 07:32:48+11', 'in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh', 't', 't', 't', 2, 0); `
    )
    await client.query(
        "INSERT INTO hosted(\"eventID\",\"socID\") VALUES " +
        `('${eventDetails.id}','${socID}'); `
    )
    return null
  } catch (error) {
    return null
  }
}
const createSoc = async ({socID, description}) => {
  try {
    await client.query(`delete from hosted where "socID"='${v.socID}';`)
    await client.query(
      "INSERT INTO SOCIETIES(id, description, name, type) VALUES " +
      `('${v.socID}', '${description}', 'Test Soc', 0); `
    )
    return null
  } catch (error) {
    return null
  }
}
const createUser = async ({ zID, password, activated, superadmin, staff, isArc }) => {
  try {
    await client.query(`delete from attend where "zID"='${zID}'; `)
    await client.query(`delete from staff where "zID"='${zID}';`)
    await client.query(`delete from users where "zID"='${zID}'; `)
    await client.query(
      `INSERT INTO users("zID", "password", "firstName", "lastName", "isArc", "activated", "superadmin") VALUES \
      ('${zID}', '${SHA256(password)}', 'first', 'last', ${isArc ? "'t'" : "'f'"}, ${activated ? "'t'" : "'f'"}, ${superadmin ? "'t'" : "'f'"}); `
    )
    return null
  } catch (error) {
    return null
  }
}

module.exports = { 
  db, createUser, createEvent, createSoc
}
