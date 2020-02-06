-- drop table if exists users;
create table users (
    zid text not null,
    name text not null,
    password text not null,
    primary key(zid)
);
-- drop table if exists events;
create table events (
    eventID text not null,
    name text not null,
    eventdate date not null,
    owner text not null references users(zid),
    qrCode boolean,
    description text,
    primary key(eventID)
);
-- drop table if exists participation;
create table participation (
    points text not null,
    isArcMember boolean not null,
    zid text not null references users(zid),
    eventID text not null references events(eventID),
    primary key (zid, eventID)
);
-- drop table if exists society;
create table society (
    societyID text,
    societyName text not null unique,
    primary key (societyID)
);
-- drop table if exists host;
create table host (
    location text,
    society text references society(societyID),
    eventID text not null references events(eventID),
    primary key (society, eventID)
);
-- drop table if exists socstaff;
create table socstaff (
    society text references society(societyID),
    zid text references users(zid),
    role text not null,
    primary key (society, zid)
);