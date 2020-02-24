drop TABLE IF EXISTS users cascade;
CREATE TABLE IF NOT EXISTS users (
    zid TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    isArc BOOLEAN NOT NULL,
    activationLink TEXT,
    activationStatus BOOLEAN NOT NULL,
    primary key(zid)
);
drop TABLE IF EXISTS events cascade;
CREATE TABLE IF NOT EXISTS events (
    eventID TEXT NOT NULL,
    name TEXT NOT NULL,
    eventdate date NOT NULL,
    endTime time,
	eventWeek TEXT NOT NULL,
    owner TEXT NOT NULL REFERENCES users(zid),
    qrCode boolean,
    description TEXT,
 primary key(eventID)
);
drop TABLE IF EXISTS participation cascade;
CREATE TABLE IF NOT EXISTS participation (
    points TEXT NOT NULL,
    isArcMember boolean NOT NULL,
    zid TEXT NOT NULL REFERENCES users(zid),
    eventID TEXT NOT NULL REFERENCES events(eventID),
    time timestamp NOT NULL,
    primary key (zid, eventID)
);
drop TABLE IF EXISTS society cascade;
CREATE TABLE IF NOT EXISTS society (
    societyID TEXT,
    societyName TEXT NOT NULL unique,
    primary key (societyID)
);
drop TABLE IF EXISTS host cascade;
CREATE TABLE IF NOT EXISTS host (
    location TEXT,
    society TEXT REFERENCES society(societyID),
    eventID TEXT NOT NULL REFERENCES events(eventID),
    primary key (society, eventID)
);
drop TABLE IF EXISTS socstaff cascade;
CREATE TABLE IF NOT EXISTS socstaff (
    society TEXT REFERENCES society(societyID),
    zid TEXT REFERENCES users(zid),
    role INTEGER NOT NULL,
    primary key (society, zid)
);
drop TABLE IF EXISTS encrypt;
CREATE TABLE IF NOT EXISTS encrypt (
    password TEXT primary key
);

create or replace view hostedEvents as select events.eventID, name, eventdate, location, societyname from events join host on events.eventID = host.eventID join society on (society.societyID = host.society);
create or replace view userInSociety as select societyid, societyname, users.zID from society join socstaff on society.societyid = socstaff.society join users on socstaff.zid = users.zid;
create or replace view userParticipatedEvents as select eventID, name, eventdate, location, hostedevents.societyname, societyid, zid from hostedevents join userinsociety on hostedevents.societyname = userinsociety.societyname;
