DROP TABLE IF EXISTS `_period` ;

CREATE TABLE IF NOT EXISTS `_period` (
  `pr_id` INT NOT NULL ,
  `pr_start` DATETIME NULL,
  `pr_end` DATETIME NULL,
  PRIMARY KEY (`pr_id`))
;


DROP TABLE IF EXISTS `_info` ;
CREATE TABLE IF NOT EXISTS `_info` (
  `in_id` INT NOT NULL,
  `in_nam` VARCHAR(45) NULL,
  `in_surn` VARCHAR(45) NULL,
  `in_identif` VARCHAR(45) NULL,
  PRIMARY KEY (`in_id`))
;

DROP TABLE IF EXISTS `_type` ;
CREATE TABLE IF NOT EXISTS `_type` (
  `tp_type` INT NOT NULL ,
  `tp_def` VARCHAR(45) NULL,
  PRIMARY KEY (`tp_type`))
;

DROP TABLE IF EXISTS `_security` ;
CREATE TABLE IF NOT EXISTS `_security` (
  `sg_id` INT NOT NULL,
  `sg_pass` VARCHAR(255) NULL,
  PRIMARY KEY (`sg_id`))
;

DROP TABLE IF EXISTS `_place` ;
CREATE TABLE IF NOT EXISTS `_place` (
  `pl_id` INT NOT NULL ,
  `pl_name` VARCHAR(250) NULL,
  `pl_cp` VARCHAR(45) NULL,
  `pl_pob` VARCHAR(45) NULL,
  `pl_road` VARCHAR(45) NULL,
  `pl_build` VARCHAR(45) NULL,
  `pl_floor` VARCHAR(45) NULL,
  `pl_door` VARCHAR(45) NULL,
  PRIMARY KEY (`pl_id`))
;

DROP TABLE IF EXISTS `_value` ;
CREATE TABLE IF NOT EXISTS `_value` (
  `vl_id` INT NOT NULL ,
  `vl_value` DOUBLE NULL,
  `vl_tax` DOUBLE NULL,
  `vl_retention` DOUBLE NULL,
  `vl_pos` INT NULL,
  PRIMARY KEY (`vl_id`))
;


DROP TABLE IF EXISTS `_contact` ;
CREATE TABLE IF NOT EXISTS `_contact` (
  `ct_id` INT NOT NULL ,
  `ct_tel` INT NULL,
  `ct_mail` VARCHAR(255) NULL,
  PRIMARY KEY (`ct_id`))
;


DROP TABLE IF EXISTS `_entity` ;
CREATE TABLE IF NOT EXISTS `_entity` (
  `id_entity` INT NOT NULL ,
  `_type` INT NOT NULL,
  `_period` INT NULL,
  `_info` INT NULL,
  `_security` INT NULL,
  `_place` INT NULL,
  `_value` INT NULL,
  `_contact` INT NULL,
  `_child` INT NULL,
  PRIMARY KEY (`id_entity`))
;


DROP TABLE IF EXISTS `extenceinfo` ;
CREATE TABLE IF NOT EXISTS `extenceinfo` (
  `_info` INT NOT NULL,
  `ei_text` LONGTEXT NULL)
;


DROP TABLE IF EXISTS `_cordinates` ;
CREATE TABLE IF NOT EXISTS `_cordinates` (
  `_place` INT NOT NULL,
  `x` DOUBLE NULL,
  `y` DOUBLE NULL,
  `z` DOUBLE NULL)
;


DROP TABLE IF EXISTS `v_type`;
DROP VIEW IF EXISTS `v_type` ;
CREATE VIEW `v_type` AS
SELECT id_entity, tp_def FROM _entity
left join _type on _type = tp_type ;

DROP TABLE IF EXISTS `v_log`;
DROP VIEW IF EXISTS `v_log` ;
CREATE VIEW `v_log` AS
SELECT in_nam as name, sg_pass as pass FROM  _entity
  left join _security on sg_id = _security
  left join _info on in_id = _info
  where in_nam is not null and sg_pass is not null
  ;



INSERT INTO _type
  ( tp_type, tp_def)
VALUES
  (1,'user'),
  (2,'person'),
  (3,'bill'),
  (4,'work_day'),
  (5,'company'),
  (6,'domiciliacion_bancaria'),
  (7,'object'),
  (8,'vertex'),
  (9,'face');
