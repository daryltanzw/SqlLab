CREATE TABLE warehouse (
	w_id INTEGER PRIMARY KEY,
	w_name VARCHAR(50),
	w_street VARCHAR(50),
	w_city VARCHAR(50),
	w_country VARCHAR(50)
);

INSERT INTO warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (301, 'Schmedeman', 'Sunbrook', 'Singapore', 'Singapore');
INSERT INTO warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (281, 'Crescent Oaks', 'Loeprich', 'Singapore', 'Singapore');
INSERT INTO warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (22, 'Namekagon', 'Anniversary', 'Singapore', 'Singapore');
INSERT INTO warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (1004, 'Fairfield', 'Sachs', 'Singapore', 'Singapore');
INSERT INTO warehouse (w_id, w_name, w_street, w_city, w_country) VALUES (3, 'Briar Crest', 'Kensington', 'Singapore', 'China');

CREATE TABLE item (
i_id INTEGER PRIMARY KEY,
i_im_id CHAR(8) UNIQUE NOT NULL,
i_name VARCHAR(50)  NOT NULL,
i_price NUMERIC(5, 2)  NOT NULL CHECK(i_price >0));

INSERT INTO item (i_id, i_im_id, i_name, i_price) VALUES (1, '35356226', 'Indapamide', 95.23);
INSERT INTO item (i_id, i_im_id, i_name, i_price) VALUES (2, '00851287', 'SYLATRON', 80.22);
INSERT INTO item (i_id, i_im_id, i_name, i_price) VALUES (3, '52549414', 'Meprobamate', 11.64);
INSERT INTO item (i_id, i_im_id, i_name, i_price) VALUES (4, '54868007', 'MECLIZINE HYDROCHLORIDE', 54.49);
INSERT INTO item (i_id, i_im_id, i_name, i_price) VALUES (5, '24658312', 'Doxycycline Hyclate', 28.99);

CREATE TABLE stock (
w_id INTEGER REFERENCES warehouse(w_id),
i_id INTEGER REFERENCES item(i_id),
s_qty SMALLINT CHECK(s_qty > 0),
PRIMARY KEY (w_id, i_id));

INSERT INTO stock VALUES (301, 1, 338);
INSERT INTO stock VALUES (301, 4, 938);
INSERT INTO stock VALUES (301, 5, 760);