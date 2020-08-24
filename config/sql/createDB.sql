DROP TABLE IF EXISTS qubook;
CREATE TABLE IF NOT EXISTS qubook (
  name varchar(64) not null,
  writer varchar(64) not null,
  type varchar(32) not null,
  size int(10) not null,
  intime date not null,
  dl varchar(256) default '',

  PRIMARY KEY (name,writer),
  KEY name (name) USING BTREE,
  KEY writer (writer) USING BTREE,
  KEY type (type) USING BTREE,
  KEY size (size) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin