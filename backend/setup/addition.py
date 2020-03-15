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


def main():
    changeSocStaff()

if __name__ == "__main__":
    main()
    
    
    
    