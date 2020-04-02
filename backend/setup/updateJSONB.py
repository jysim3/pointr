import sys
sys.path.append("../")
from util.utilFunctions import callQuery, makeConnection

@makeConnection
def updateTables(conn, curs):
    callQuery("ALTER TABLE users ALTER COLUMN additionalInfomation SET DATA TYPE jsonb USING additionalInfomation::jsonb;", conn, curs)
    callQuery("ALTER TABLE events ALTER COLUMN additionalInfomation SET DATA TYPE jsonb USING additionalInfomation::jsonb;", conn, curs)
    callQuery("ALTER TABLE society ALTER COLUMN additionalInfomation SET DATA TYPE jsonb USING additionalInfomation::jsonb;", conn, curs)
    callQuery("ALTER TABLE socstaff ALTER COLUMN additionalInfomation SET DATA TYPE jsonb USING additionalInfomation::jsonb;", conn, curs)
    conn.commit()
    conn.close()
    print("Upgrading completed, JSON columns migrated to JSONB")

def main():
    updateTables()

if __name__ == "__main__":
    main()