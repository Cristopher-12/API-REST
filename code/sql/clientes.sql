DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR (50) NOT NULL,
    email VARCHAR (50) NOT NULL
);
INSERT INTO clientes (id_cliente,nombre,email) VALUES ("1","cristopher","cristopher@email.com");
INSERT INTO clientes (id_cliente,nombre,email) VALUES ("2","Sebastian","sebastian@email.com");
INSERT INTO clientes (id_cliente,nombre,email) VALUES ("3","Arturo","arturo@email.com");


.headers ON
SELECT * FROM clientes;