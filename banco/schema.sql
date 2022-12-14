SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS,
  UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS,
  FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE,
  SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE SCHEMA IF NOT EXISTS `banco_api` DEFAULT CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `cpf` CHAR(11) NOT NULL,
  `rg` char(10),
  `nome` VARCHAR(250),
  `senha` VARCHAR(245) NOT NULL,
  `data_nasc` DATE,
  `rua` VARCHAR(250),
  `bairro` VARCHAR(250),
  `cidade` VARCHAR(250),
  `complemento` VARCHAR(250),
  `uf` VARCHAR(250),
  `cep` INT(10),
  `numero` VARCHAR(250),
  `genero` VARCHAR(250),
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`conta` (
  `id_conta` INT(5) NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(30) NOT NULL,
  `saldo` DECIMAL(40, 2),
  `tipo` VARCHAR(30) NOT NULL,
  `usuario` int(5) NOT NULL,
  `agencia` INT(5),
  `abertura` DATETIME NOT NULL,
  `ultima_cobranca` DATETIME,
  PRIMARY KEY (`id_conta`),
  UNIQUE INDEX `id_conta_UNIQUE` (`id_conta` ASC),
  INDEX `fk_conta_usuario1_idx` (`usuario` ASC),
  INDEX `fk_conta_agencia1_idx` (`agencia` ASC),
  CONSTRAINT `fk_conta_usuario1` FOREIGN KEY (`usuario`) REFERENCES `banco_api`.`usuario` (`id_usuario`),
  CONSTRAINT `fk_conta_agencia1` FOREIGN KEY (`agencia`) REFERENCES `banco_api`.`agencia` (`id_agencia`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`transacoes`(
  `id_transacao` INT(5) NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(145) NOT NULL,
  `id_conta` INT(5) NOT NULL,
  `valor` DECIMAL(40, 2) NOT NULL,
  `data_inicio` DATETIME NOT NULL,
  `data_fim` DATETIME,
  `tipo` VARCHAR(145),
  `destino` INT(5),
  PRIMARY KEY (`id_transacao`),
  INDEX `fk_transacoes_conta1_idx` (`id_conta`) -- CONSTRAINT `fk_transacoes_conta1_idx` FOREIGN KEY (`id_conta`) REFERENCES `banco_api`.`conta` (`id_conta`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`agencia`(
  `id_agencia` INT(4) NOT NULL AUTO_INCREMENT,
  `gerente` INT(5),
  `nome` VARCHAR(145) NOT NULL,
  PRIMARY KEY (`id_agencia`),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC),
  UNIQUE INDEX `gerente_UNIQUE` (`gerente` ASC),
  CONSTRAINT `fk_agencia_conta1_idx` FOREIGN KEY (`gerente`) REFERENCES `banco_api`.`conta` (`id_conta`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`config`(
  `taxa_juros` DECIMAL(4, 2) DEFAULT 1.00,
  `taxa_rendimento` DECIMAL(4, 2) DEFAULT 1.00,
  `data` DATETIME NOT NULL
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;