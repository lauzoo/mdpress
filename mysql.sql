CREATE TABLE posts (
	id varchar(64) NOT NULL ,
	user_id varchar(64) NOT NULL,
	name varchar(50) NOT NULL COMMENT 'Article Title' ,
	content varchar(10240) NOT NULL COMMENT 'Article Content' ,
	PRIMARY KEY (id)
);