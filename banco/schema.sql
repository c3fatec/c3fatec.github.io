CREATE DATABASE IF NOT EXISTS banco;
CREATE TABLE IF NOT EXISTS banco.usuario (
  cpf CHAR(11) NOT NULL UNIQUE,
  nome VARCHAR(245) NOT NULL,
  senha VARCHAR(245) NOT NULL,
  data_nasc DATE NOT NULL
);
INSERT INTO banco.usuario (cpf, nome, senha, data_nasc)
VALUES (
    '11122233344',
    'gabriel',
    'sapo',
    '2001-12-22 00:00:00'
  );