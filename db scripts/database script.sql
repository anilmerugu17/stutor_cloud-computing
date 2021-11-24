CREATE DATABASE STUTOR_DB;

USE STUTOR_DB;

CREATE TABLE STUTOR_TABLE(email varchar(30) primary key,
                        name varchar(20) NOT NULL,
                        password varchar(20) NOT NULL,
                        user_type varchar(10) NOT NULL);

CREATE TABLE STUDENT_PROFILE (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            subject_name varchar(30) NOT NULL,
                            edu_level varchar(30) DEFAULT NULL,
                            pay_per_hour INT,
                            email varchar(45) NOT NULL,
                            KEY `for1_idx` (email),
                            CONSTRAINT `for1` FOREIGN KEY (email) REFERENCES
                            STUTOR_TABLE(email) ON DELETE NO ACTION ON UPDATE NO ACTION);

CREATE TABLE TUTOR_PROFILE(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            subject_name varchar(30)  NOT NULL,
                            edu_level varchar(30) DEFAULT NULL,
                            pay_per_hour INT,
                            email varchar(45)  NOT NULL,
                            KEY `for2_idx` (email),
                            CONSTRAINT `for2` FOREIGN KEY (email) REFERENCES
                            STUTOR_TABLE(email) ON DELETE NO ACTION ON UPDATE NO ACTION);