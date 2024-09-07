create table user(
    userid bigint(20) not null,
    password varchar(20) not null,
    secpassword varchar(20) default '123456',
    nick varchar(20) not null,
    phonenum varchar(11) not null,
    sex char(1) default '1',
    idcard char(18) default null,
    status int(4) default 0,
    createtime datetime not null,
    lastlogintime datetime not null,
    primary key (userid)
) engine = InnoDB default charset = utf8;

insert into user(userid, password, secpassword, nick, sex, idcard, status, createtime, lastlogintime)
values(15214663233, '')


create table package(
    userid bigint(20) not null,
    money int(4) default 0,
    coin int(4) default 0,
    prop_1001 int(4) default 0,
    prop_1002 int(4) default 0,
    prop_1003 int(4) default 0,
    prop_1006 int(4) default 0,
    prop_1007 int(4) default 0,
    freshtime datetime not null,
    primary key (userid)
) engine = InnoDB default charset = utf8;