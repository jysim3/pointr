-- drop TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
    zid TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL,
    isArc BOOLEAN NOT NULL,
    commencementYear INTEGER,
    studentType TEXT,
    degreeType TEXT,
    isSuperAdmin BOOLEAN NOT NULL,
    activationStatus BOOLEAN NOT NULL,
    description TEXT,
    additionalInfomation JSONB,
    primary key(zid)
);
-- drop TABLE IF EXISTS events CASCADE;
CREATE TABLE IF NOT EXISTS events (
    eventID TEXT NOT NULL,
    name TEXT NOT NULL,
    eventdate date NOT NULL,
    --- NOTE: FIXME: Added in a starttime in events, this is used to ensure users cant sign in to events before/after the event
    --- NOTE: We could, however, also add in a "grace period" of which we allow people to sign up (i.e. 30 mins before/after)
    startTime TIMESTAMP,
    endTime TIMESTAMP,
	eventWeek TEXT NOT NULL,
    owner TEXT NOT NULL REFERENCES users(zid) ON DELETE CASCADE,
    qrCode boolean,
    description TEXT,
    isClosed BOOLEAN,
    additionalInfomation JSONB,
    primary key(eventID)
);
-- drop TABLE IF EXISTS participation CASCADE;
CREATE TABLE IF NOT EXISTS participation (
    points TEXT NOT NULL,
    isArcMember boolean NOT NULL,
    zid TEXT NOT NULL REFERENCES users(zid) ON DELETE CASCADE,
    eventID TEXT NOT NULL REFERENCES events(eventID) ON DELETE CASCADE,
    time timestamp NOT NULL,
    primary key (zid, eventID)
);
-- drop TABLE IF EXISTS society CASCADE;
CREATE TABLE IF NOT EXISTS society (
    societyID TEXT,
    description TEXT,
    societyName TEXT NOT NULL unique,
    isCollege BOOLEAN NOT NULL,
    additionalInfomation JSONB,
    primary key (societyID)
);
-- NOTE: Perhaps we can add an additional collegeSocs field here for more college specific fields
-- drop TABLE IF EXISTS host CASCADE;
CREATE TABLE IF NOT EXISTS host (
    location TEXT,
    society TEXT REFERENCES society(societyID) ON DELETE CASCADE,
    eventID TEXT NOT NULL REFERENCES events(eventID) ON DELETE CASCADE,
    primary key (society, eventID)
);
-- drop TABLE IF EXISTS socstaff CASCADE;
CREATE TABLE IF NOT EXISTS socstaff (
    society TEXT REFERENCES society(societyID) ON DELETE CASCADE,
    zid TEXT REFERENCES users(zid) ON DELETE CASCADE,
    role INTEGER NOT NULL,
    additionalInfomation JSONB,
    primary key (society, zid)
);
-- DROP TABLE IF EXISTS collegeUsers CASCADE;
CREATE TABLE IF NOT EXISTS collegeUsers (
    societyID TEXT REFERENCES society(societyID) ON DELETE CASCADE,
    zID TEXT REFERENCES users(zID) ON DELETE CASCADE,
    floorGroup TEXT NOT NULL,
    primary key (societyID, zID)
);

create or replace view hostedEvents 
as select events.eventID, name, eventdate, location, societyname, societyID, events.description from events 
join host on events.eventID = host.eventID join society on (society.societyID = host.society);

create or replace view userInSociety 
as select societyid, societyname, users.zID, role from society 
join socstaff on society.societyid = socstaff.society join users on socstaff.zid = users.zid;

create or replace view userParticipatedEvents 
as select hostedEvents.eventID, name, eventdate, location, hostedevents.societyname, societyid, zid, time from hostedEvents
join participation ON hostedEvents.eventID = participation.eventID;
