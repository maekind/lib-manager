CREATE TABLE IF NOT EXISTS temp (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
field1 VARCHAR(30) NOT NULL
); 

INSERT INTO temp(field1)
VALUES
	('My first task'),
	('It is the second task'),
	('This is the third task of the week');