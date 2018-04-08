DROP database IF exists forum_log;
CREATE database forum_log;
use forum_log

CREATE TABLE IF NOT EXISTS action_log(
    ip BIGINT(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    object_id INTEGER,
    request VARCHAR(50) NOT NULL 
    /*--request_result, --request_arrival_time, --response_time,*/
);
