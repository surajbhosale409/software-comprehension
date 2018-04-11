
create user 'www-data'@'localhost' identified by 'S';
grant all privileges on * . * to 'www-data'@'localhost';
create database forum;
create database forum_log;
