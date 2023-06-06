CREATE TABLE IF NOT EXISTS Hosts(
	hid integer PRIMARY KEY,
	name varchar(60),
	password varchar(120)
);

CREATE TABLE IF NOT EXISTS Listings(
	lid integer PRIMARY KEY,
	name varchar(240),
	area varchar(120),
	loc varchar(120),
	room_type varchar(120),
	price integer,
	hid integer REFERENCES Hosts(hid) ON DELETE CASCADE
);

CREATE TABLE Users(
	uid integer PRIMARY KEY,
	name varchar(60),
	email varchar(60),
	password varchar(120)
);

CREATE TABLE IF NOT EXISTS Rents(
	uid integer REFERENCES Users(uid),
	lid integer REFERENCES Listings(lid),
	PRIMARY KEY (uid, lid)
);

CREATE TABLE IF NOT EXISTS Owns(
	hid integer REFERENCES Hosts(hid),
	lid integer REFERENCES Listings(lid),
	PRIMARY KEY (hid, lid)
);

CREATE TABLE IF NOT EXISTS Transportation(
	vehicle varchar(60) PRIMARY KEY,
	price integer
);

CREATE TABLE IF NOT EXISTS Uses(
	vehicle varchar(60) REFERENCES Transportation(vehicle),
	uid integer REFERENCES Users(uid),
	PRIMARY KEY (vehicle, uid)
);

CREATE TABLE IF NOT EXISTS Attractions(
	name varchar(60),
	loc varchar(60),
	price integer,
	PRIMARY KEY (name, loc)
);

CREATE TABLE IF NOT EXISTS Visits(
	name varchar(60),
	loc varchar(60),
	uid integer,
	constraint pk_Visits primary key (name, loc, uid),
	constraint fk_Users foreign key (uid) REFERENCES Users(uid),
	constraint fk_Attractions foreign key (name, loc) REFERENCES Attractions(name, loc)
);