-- Schema for A.lux.

-- Basic configuration details
create table alux_info (
    id      integer primary key autoincrement not null,
    key     text,
    value   text
);

-- Songs Table
create table songs (
    id          integer primary key autoincrement not null,
    playlist    text,
    title       text,
    artist      text,
    genre       text,
    thing_from  text,
    image_url   text,
    hidden      integer,
    background  integer,
    playcount   integer
);

-- User table
create table users(
	id			integer primary key autoincrement not null,
	username		text,
	password		text,
    alux_id	        text,
    expiration      date
);
