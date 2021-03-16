drop database if exists orm_test;
create database orm_test default charset utf8 collate utf8_general_ci;
use orm_test;

DROP TABLE IF EXISTS `test_user`;
CREATE TABLE `test_user` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `class_id` INT(11) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `age` INT(11) DEFAULT 0,
    `addr` VARCHAR(1000),
    `tele` VARCHAR(50),
    `created_at` DATETIME,
    `updated_at` DATETIME,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`tele`)
) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `test_class`;
CREATE TABLE `test_class` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `created_at` DATETIME,
    `updated_at` DATETIME,
    PRIMARY KEY (`id`)
) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;