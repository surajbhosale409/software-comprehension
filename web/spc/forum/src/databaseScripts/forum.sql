source forum_log.sql

DROP database IF exists forum;
CREATE database forum;
use forum;

DROP TABLE IF EXISTS user_details;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS comment_hierarchy;
DROP TABLE IF EXISTS templates;

CREATE TABLE IF NOT EXISTS user_details (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(15) NOT NULL,
    email VARCHAR(320) NOT NULL
);

CREATE TABLE IF NOT EXISTS comments(
    comment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    comment_text VARCHAR(1000) NOT NULL,
    commenting_user_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comment_hierarchy(
    comment_id INTEGER NOT NULL,
    parent_comment_id INTEGER
);

CREATE TABLE IF NOT EXISTS templates(
    template_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    template_path VARCHAR(255) NOT NULL
);

/* insert when user log-in OR when user start session it first checks ip for an user if it doesn't matches then it updates ip */
CREATE TABLE IF NOT EXISTS auxilary_action_log(
    user_id INTEGER NOT NULL UNIQUE,
    ip BIGINT(20) NOT NULL
);


/*--- Constraints on Table -----*/

ALTER TABLE comment_hierarchy
    ADD CONSTRAINT comment_id_fkey FOREIGN KEY (comment_id) References comments(comment_id) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE comment_hierarchy
    ADD CONSTRAINT parent_comment_id_fkey FOREIGN KEY (parent_comment_id) References comments(comment_id) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE comments 
    ADD CONSTRAINT commenting_user_id_fkey FOREIGN KEY (commenting_user_id) References user_details(user_id) ON DELETE RESTRICT ON UPDATE CASCADE;

delimiter |
/*
CREATE PROCEDURE insert_action_log(IN IP INTEGER, IN user_id INTEGER, IN objectId INTEGER, IN request VARCHAR(15))
    BEGIN
        insert into forum_log.action_log(ip ,user_id, object_id, request) values(IP, user_id, objectId, request);
    END;
*/
CREATE TRIGGER insert_comment_history after INSERT ON comments 
FOR EACH ROW
    BEGIN
        SET @ip =  (SELECT ip FROM auxilary_action_log WHERE user_id = NEW.commenting_user_id);
        insert into forum_log.action_log(ip ,user_id, object_id, request) values(@ip, NEW.commenting_user_id, 0, "INSERTING COMMENT");
    END;

CREATE TRIGGER update_comment_history after UPDATE ON comments
FOR EACH ROW
    BEGIN
        SET @ip =  (SELECT ip FROM auxilary_action_log WHERE user_id = NEW.commenting_user_id);
        insert into forum_log.action_log(ip ,user_id, object_id, request) values(@ip, NEW.commenting_user_id, 0, "UPDATING COMMENT");
    END;

CREATE TRIGGER delate_comment_history after DELETE ON comments
FOR EACH ROW
    BEGIN
        SET @ip =  (SELECT ip FROM auxilary_action_log WHERE user_id = OLD.commenting_user_id);
        insert into forum_log.action_log(ip ,user_id, object_id, request) values(@ip, OLD.commenting_user_id, 0, "DELETING COMMENT");
    END;


CREATE TRIGGER history after INSERT ON auxilary_action_log 
FOR EACH ROW
    BEGIN
        insert into forum_log.action_log(ip ,user_id, object_id, request) values(NEW.ip, NEW.user_id, 0, "INSERTING AUXILARY_ACTION_LOG");
        /*call insert_action_log(NEW.ip, NEW.user_id, 0, "INSERTING AUXILARY_ACTION_LOG");*/
    END;
  |
delimiter ;

INSERT INTO user_details(username, email) VALUES("bhandvishnu", "bhandvishnu@gmail.com");
INSERT INTO auxilary_action_log(user_id, ip) VALUES(1, inet_aton("196.1.114.35"));
