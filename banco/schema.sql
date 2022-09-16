SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `banco_api` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `banco_api`.`usuario` (
  `id_usuario` INT NOT NULL,
  `CPF` CHAR(11) NOT NULL,
  `nome_usuario` VARCHAR(250) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `genero` VARCHAR(210) NOT NULL,
  `endereco` VARCHAR(245) NOT NULL,
  `senha_usuario` CHAR(245) NOT NULL,
  `email` VARCHAR(245) NOT NULL,
  `id_banco` INT(3) NOT NULL,
  PRIMARY KEY (`id_usuario`, `id_banco`),
  INDEX `fk_usuario_banco_idx` (`id_banco` ASC),
  UNIQUE INDEX `CPF_UNIQUE` (`CPF` ASC),
  CONSTRAINT `fk_usuario_banco`
    FOREIGN KEY (`id_banco`)
    REFERENCES `banco_api`.`banco` (`id_banco`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `banco_api`.`banco` (
  `id_banco` INT(3) NOT NULL,
  `gerente_geral` INT(5) NOT NULL,
  `capital_monetario` DECIMAL(9,2) NOT NULL,
  PRIMARY KEY (`id_banco`),
  UNIQUE INDEX `agencia_UNIQUE` (`gerente_geral` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `banco_api`.`conta` (
  `id_numero_conta` VARCHAR(5) NOT NULL DEFAULT '00000',
  `conta_tipo` VARCHAR(10) NOT NULL,
  `conta_data_abertura` DATETIME NOT NULL,
  `conta_data_fechamento` DATETIME NOT NULL,
  `conta_saldo` DECIMAL(9,2) NOT NULL,
  `id_banco` INT(3) NOT NULL,
  `CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`id_numero_conta`, `id_banco`, `CPF`),
  UNIQUE INDEX `id_numero_conta_UNIQUE` (`id_numero_conta` ASC),
  INDEX `fk_conta_banco1_idx` (`id_banco` ASC),
  INDEX `fk_conta_usuario1_idx` (`CPF` ASC),
  CONSTRAINT `fk_conta_banco1`
    FOREIGN KEY (`id_banco`)
    REFERENCES `banco_api`.`banco` (`id_banco`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conta_usuario1`
    FOREIGN KEY (`CPF`)
    REFERENCES `banco_api`.`usuario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;