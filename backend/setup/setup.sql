-- drop table if exists users cascade;
create table if not exists users (
    zid text not null,
    name text not null,
    password text not null,
    primary key(zid)
);
-- drop table if exists events cascade;
create table if not exists events (
    eventID text not null,
    name text not null,
    eventdate date not null,
	eventWeek text not null,
    owner text not null references users(zid),
    qrCode boolean,
    description text,
    primary key(eventID)
);
-- drop table if exists participation cascade;
create table if not exists participation (
    points text not null,
    isArcMember boolean not null,
    zid text not null references users(zid),
    eventID text not null references events(eventID),
    primary key (zid, eventID)
);
-- drop table if exists society cascade;
create table if not exists society (
    societyID text,
    societyName text not null unique,
    primary key (societyID)
);
-- drop table if exists host cascade;
create table if not exists host (
    location text,
    society text references society(societyID),
    eventID text not null references events(eventID),
    primary key (society, eventID)
);
-- drop table if exists socstaff cascade;
create table if not exists socstaff (
    society text references society(societyID),
    zid text references users(zid),
    role text not null,
    primary key (society, zid)
);
