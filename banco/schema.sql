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
  `nome` VARCHAR(250) NOT NULL,
  `senha` VARCHAR(245) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`conta` (
  `id_conta` INT(5) NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(30) NOT NULL,
  `saldo` DECIMAL(9, 2),
  `tipo` VARCHAR(30) NOT NULL,
  `usuario` int(5) NOT NULL,
  `agencia` INT(5),
  PRIMARY KEY (`id_conta`),
  UNIQUE INDEX `id_conta_UNIQUE` (`id_conta` ASC),
  INDEX `fk_conta_usuario1_idx` (`usuario` ASC),
  INDEX `fk_conta_agencia1_idx` (`agencia` ASC),
  CONSTRAINT `fk_conta_usuario1` FOREIGN KEY (`usuario`) REFERENCES `banco_api`.`usuario` (`id_usuario`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_conta_agencia1` FOREIGN KEY (`agencia`) REFERENCES `banco_api`.`agencia` (`id_agencia`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
ALTER TABLE `banco_api`.`conta` AUTO_INCREMENT = 20000;
CREATE TABLE IF NOT EXISTS `banco_api`.`transacoes`(
  `id_transacao` INT(5) NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(145) NOT NULL,
  `id_conta` INT(5) NOT NULL,
  `valor` DECIMAL(9, 2) NOT NULL,
  `data_inicio` DATETIME NOT NULL,
  `data_fim` DATETIME,
  `tipo` VARCHAR(145),
  PRIMARY KEY (`id_transacao`),
  INDEX `fk_transacoes_conta1_idx` (`id_conta`),
  CONSTRAINT `fk_transacoes_conta1_idx` FOREIGN KEY (`id_conta`) REFERENCES `banco_api`.`conta` (`id_conta`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
CREATE TABLE IF NOT EXISTS `banco_api`.`agencia`(
  `id_agencia` INT(4) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(145) NOT NULL,
  PRIMARY KEY (`id_agencia`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
alter table `banco_api`.`agencia` AUTO_INCREMENT = 1000;
SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;