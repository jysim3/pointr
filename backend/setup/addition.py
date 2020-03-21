import sys
sys.path.append("../")
from util.utilFunctions import makeConnection
import psycopg2


@makeConnection
def changeSocStaff(conn, curs):
    try:
        curs.execute("SELECT * FROM socStaff;")
    except (Exception, psycopg2.DatabaseError):
        conn.close()
        return None

    results = curs.fetchall()

    # Drop the original table and add in the additional column
    try:
        curs.execute("DROP TABLE socStaff CASCADE;")
        curs.execute('''
        CREATE TABLE socStaff (
        society TEXT REFERENCES society(societyID) ON DELETE CASCADE,
        zid TEXT REFERENCES users(zid) ON DELETE CASCADE,
        role INTEGER NOT NULL,
        additionalInfomation JSON,
        primary key (society, zid)
        );''')
        conn.commit()
    except (Exception, psycopg2.DatabaseError):
        conn.close()
        return None

    for result in results:
        try:
            curs.execute("INSERT INTO socStaff(society, zid, role) VALUES ((%s), (%s), (%s));", (result[0], result[1], result[2],))
        except (Exception, psycopg2.DatabaseError):
            conn.close()
            return None
    conn.commit()
    return True

@makeConnection
def changeEvents(conn, curs):
    try:
        curs.execute("SELECT * FROM host;")
    except Exception as e:
        conn.close()
        exit(1)

    host = curs.fetchall()

    try:
        curs.execute("SELECT * FROM PARTICIPATION;")
    except Exception as e:
        conn.close()
        exit(1)

    participation = curs.fetchall()

    try:
        curs.execute("SELECT * FROM EVENTS;")
    except Exception as e:
        conn.close()
        exit(1)

    events = curs.fetchall()
    for i in events:
        curs.execute("DELETE FROM EVENTS WHERE EVENTID = (%s);", (i[0],))
    conn.commit()
    # Dropping th eoriginal table
    try:
        curs.execute("DROP TABLE EVENTS CASCADE;")
        curs.execute('''
        CREATE TABLE EVENTS (
            eventID TEXT NOT NULL,
            name TEXT NOT NULL,
            eventdate date NOT NULL,
            startTime TIMESTAMP,
            endTime TIMESTAMP,
            eventWeek TEXT NOT NULL,
            owner TEXT NOT NULL REFERENCES users(zid) ON DELETE CASCADE,
            qrCode boolean,
            description TEXT,
            additionalInfomation JSON,
            primary key(eventID)
        );
        ''')
        conn.commit()
    except Exception as e:
        print(e)
        conn.close()
        exit(1)

    from datetime import datetime
    for i in events:
        try:
            curs.execute("INSERT INTO EVENTS (eventID, name, eventDate, startTime, endTime, eventWeek, owner, qrCode, description) VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s));", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8],))
        except Exception as e:
            print(e)
            conn.close()
            exit(1)
    conn.commit()
    for i in host:
        curs.execute("INSERT INTO HOST (LOCATION, SOCIETY, EVENTID) VALUES ((%s), (%s), (%s));", (i[0], i[1], i[2],))
    for i in participation:
        curs.execute("INSERT INTO PARTICIPATION (POINTS, ISARCMEMBER, ZID, EVENTID, TIME) VALUES ((%s), (%s), (%s), (%s), (%s));", (i[0], i[1], i[2], i[3], i[4],))
    conn.commit()


    curs.execute('''create or replace view hostedEvents 
as select events.eventID, name, eventdate, location, societyname, societyID from events 
join host on events.eventID = host.eventID join society on (society.societyID = host.society);
    ''')

    curs.execute('''create or replace view userParticipatedEvents 
as select hostedEvents.eventID, name, eventdate, location, hostedevents.societyname, societyid, zid, time from hostedEvents
join participation ON (hostedEvents.eventID = participation.eventID);
    ''')
    conn.commit()


def main():
    #changeSocStaff()
    changeEvents()
    return 0

if __name__ == "__main__":
    main()
    
    
    
    