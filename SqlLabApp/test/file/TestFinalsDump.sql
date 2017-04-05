CREATE TABLE warehouse (
	wid INTEGER PRIMARY KEY,
	wname VARCHAR(50) NOT NULL,
	wlocation VARCHAR(50) NOT NULL
);

CREATE TABLE item (
	iid INTEGER PRIMARY KEY,
	iname VARCHAR(50)  NOT NULL,
	iprice NUMERIC(5, 2)  NOT NULL CHECK(iprice >0)
);

CREATE TABLE stock (
wid INTEGER REFERENCES warehouse(wid),
iid INTEGER REFERENCES item(iid),
qty SMALLINT CHECK(qty > 0),
PRIMARY KEY (wid, iid));

CREATE TABLE warehouse1 (
	wid INTEGER PRIMARY KEY,
	wname VARCHAR(50) NOT NULL,
	wlocation VARCHAR(50) NOT NULL
);

INSERT INTO warehouse (wid, wname, wlocation) VALUES (1, 'Jurong Warehouse', 'Singapore');
INSERT INTO warehouse (wid, wname, wlocation) VALUES (2, 'Tanglin Warehouse', 'Singapore');
INSERT INTO warehouse (wid, wname, wlocation) VALUES (3, 'Beijing Warehouse', 'China');
INSERT INTO warehouse (wid, wname, wlocation) VALUES (4, 'Shanghai Warehouse', 'China');
INSERT INTO warehouse (wid, wname, wlocation) VALUES (5, 'Fuzhou Warehouse', 'China');
INSERT INTO warehouse (wid, wname, wlocation) VALUES (6, 'Tokyo Warehouse', 'Japan');

INSERT INTO item (iid, iname, iprice) VALUES (1, 'panadol' , 10.23);
INSERT INTO item (iid, iname, iprice) VALUES (2, 'Mask' , 5.23);
INSERT INTO item (iid, iname, iprice) VALUES (3, 'Chicken' , 5.99);
INSERT INTO item (iid, iname, iprice) VALUES (4, 'pasta sauce' , 10.23);
INSERT INTO item (iid, iname, iprice) VALUES (5, 'instant noodles' , 8.88);

INSERT INTO stock VALUES (1, 5, 1000);
INSERT INTO stock VALUES (1, 4, 400);
INSERT INTO stock VALUES (1, 3, 400);
INSERT INTO stock VALUES (2, 3, 1200);
INSERT INTO stock VALUES (2, 4, 300);
INSERT INTO stock VALUES (2, 1, 338);
INSERT INTO stock VALUES (3, 1, 200);
INSERT INTO stock VALUES (3, 5, 2345);
INSERT INTO stock VALUES (4, 2, 111);
INSERT INTO stock VALUES (4, 3, 1355);
INSERT INTO stock VALUES (4, 1, 200);
INSERT INTO stock VALUES (4, 5, 2300);
INSERT INTO stock VALUES (4, 4, 100);
INSERT INTO stock VALUES (5, 2, 400);
INSERT INTO stock VALUES (6, 1, 199);
INSERT INTO stock VALUES (6, 2, 200);
INSERT INTO stock VALUES (6, 3, 390);


INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (1, 'A', 'Singapore');
INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (2, 'B', 'Korea');
INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (3, 'C', 'China');
INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (4, 'D', 'UK');
INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (5, 'E', 'China');
INSERT INTO warehouse1 (wid, wname, wlocation) VALUES (6, 'F', 'Japan');