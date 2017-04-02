CREATE TABLE tid5_warehouse (
	w_id INTEGER PRIMARY KEY,
	w_name VARCHAR(50),
	w_street VARCHAR(50),
	w_city VARCHAR(50),
	w_country VARCHAR(50)
);
INSERT INTO tid5_warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (301, 'Schmedeman', 'Sunbrook', 'Singapore', 'Singapore');
INSERT INTO tid5_warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (281, 'Crescent Oaks', 'Loeprich', 'Singapore', 'Singapore');
INSERT INTO tid5_warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (22, 'Namekagon', 'Anniversary', 'Singapore', 'Singapore');
INSERT INTO tid5_warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (1004, 'Fairfield', 'Sachs', 'Singapore', 'Singapore');
INSERT INTO tid5_warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (3, 'Briar Crest', 'Kensington', 'Singapore', 'China');
CREATE TABLE tid5_item (
i_id INTEGER PRIMARY KEY,
i_im_id CHAR(8) UNIQUE NOT NULL,
i_name VARCHAR(50)  NOT NULL,
i_price NUMERIC(5, 2)  NOT NULL CHECK(i_price >0));
INSERT INTO tid5_item (i_id, i_im_id, i_name, i_price) VALUES (1, '35356226', 'Indapamide', 95.23);
INSERT INTO tid5_item (i_id, i_im_id, i_name, i_price) VALUES (2, '00851287', 'SYLATRON', 80.22);
INSERT INTO tid5_item (i_id, i_im_id, i_name, i_price) VALUES (3, '52549414', 'Meprobamate', 11.64);
INSERT INTO tid5_item (i_id, i_im_id, i_name, i_price) VALUES (4, '54868007', 'MECLIZINE HYDROCHLORIDE', 54.49);
INSERT INTO tid5_item (i_id, i_im_id, i_name, i_price) VALUES (5, '24658312', 'Doxycycline Hyclate', 28.99);
CREATE TABLE tid5_stock (
w_id INTEGER REFERENCES tid5_warehouse(w_id),
i_id INTEGER REFERENCES tid5_item(i_id),
s_qty SMALLINT CHECK(s_qty > 0),
PRIMARY KEY (w_id, i_id));
INSERT INTO tid5_stock VALUES (301, 1, 338);
INSERT INTO tid5_stock VALUES (301, 4, 938);
INSERT INTO tid5_stock VALUES (301, 5, 760);
CREATE TABLE tid5_warehouse1 (
	w_id INTEGER PRIMARY KEY,
	w_name VARCHAR(50),
	w_street VARCHAR(50),
	w_city VARCHAR(50),
	w_country VARCHAR(50)
);
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (1, 'DabZ', 'Green', 'Patemon', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (2, 'Skippad', 'Harper', 'Makale', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (1005, 'Eare', 'Dahle', 'Padangbatung', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (4, 'Topiczoom', 'John Wall', 'Pagaden', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (5, 'Wordpedia', 'Ridgeview', 'Sumberjati', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (6, 'Wordify', 'Toban', 'Banjar Serangan', 'Indonesia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (7, 'Blogpad', 'Monica', 'Nusajaya', 'Malaysia');
INSERT INTO tid5_warehouse1 (w_id, w_name, w_street, w_city, w_country) VALUES (8, 'Bluezoom', 'Atwood', 'Lunyuk Ode', 'Indonesia');
CREATE TABLE tid5_item1 (
i_id INTEGER PRIMARY KEY,
i_im_id CHAR(8) UNIQUE NOT NULL,
i_name VARCHAR(50)  NOT NULL,
i_price NUMERIC(5, 2)  NOT NULL CHECK(i_price >0));
INSERT INTO tid5_item1 (i_id, i_im_id, i_name, i_price) VALUES (13, '67345078', '4 in 1 Pressed Mineral SPF 15 Porcelain', 62.04);
INSERT INTO tid5_item1 (i_id, i_im_id, i_name, i_price) VALUES (14, '36987288', 'Virginia Live Oak', 36.96);
INSERT INTO tid5_item1(i_id, i_im_id, i_name, i_price) VALUES (15, '67510150', 'Night Time Cold/Flu Relief Cherry', 92.26);
INSERT INTO tid5_item1(i_id, i_im_id, i_name, i_price) VALUES (16, '53942326', 'Tartar Control Plus', 50.96);
INSERT INTO tid5_item1 (i_id, i_im_id, i_name, i_price) VALUES (17, '33992113', 'anti-dandruff', 18.73);
