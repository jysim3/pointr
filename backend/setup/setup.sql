drop TABLE IF EXISTS users cascade;
CREATE TABLE IF NOT EXISTS users (
    zid text NOT NULL,
    password text NOT NULL,
    primary key(zid)
);
drop TABLE IF EXISTS events cascade;
CREATE TABLE IF NOT EXISTS events (
    eventID text NOT NULL,
    name text NOT NULL,
    eventdate date NOT NULL,
	eventWeek text NOT NULL,
    owner text NOT NULL references users(zid),
    qrCode boolean,
    description text,
 primary key(eventID)
);
drop TABLE IF EXISTS participation cascade;
CREATE TABLE IF NOT EXISTS participation (
    points text NOT NULL,
    isArcMember boolean NOT NULL,
    zid text NOT NULL references users(zid),
    eventID text NOT NULL references events(eventID),
    primary key (zid, eventID)
);
drop TABLE IF EXISTS society cascade;
CREATE TABLE IF NOT EXISTS society (
    societyID text,
    societyName text NOT NULL unique,
    primary key (societyID)
);
drop TABLE IF EXISTS host cascade;
CREATE TABLE IF NOT EXISTS host (
    location text,
    society text references society(societyID),
    eventID text NOT NULL references events(eventID),
    primary key (society, eventID)
);
drop TABLE IF EXISTS socstaff cascade;
CREATE TABLE IF NOT EXISTS socstaff (
    society text references society(societyID),
    zid text references users(zid),
    role INTEGER NOT NULL,
    primary key (society, zid)
);
