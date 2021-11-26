CREATE DATABASE STUTOR_DB;

USE STUTOR_DB;

CREATE TABLE STUTOR_TABLE(email varchar(30) primary key,
                        name varchar(20) NOT NULL,
                        password varchar(20) NOT NULL,
                        user_type varchar(10) NOT NULL);

CREATE TABLE STUDENT_PROFILE (subject_name varchar(30) NOT NULL,
                            edu_level varchar(30) DEFAULT NULL,
                            pay_per_hour INT,
                            email varchar(45) PRIMARY KEY
                            );

CREATE TABLE TUTOR_PROFILE(subject_name varchar(30)  NOT NULL,
                            edu_level varchar(30) DEFAULT NULL,
                            pay_per_hour INT,
                            email varchar(45) PRIMARY KEY
                            );