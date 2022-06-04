USE rohoTECH;

CREATE TABLE departments(
    deptID INTEGER,
    Name varchar(50),
    PRIMARY KEY(deptID)
);

CREATE TABLE officials(
    rohoID integer primary key AUTO_INCREMENT,
    Name varchar(50) not null,
    Adhar_card_Number varchar(50) not null,
    government_id varchar(20) not null,
    Age int,
    Phone_number varchar(13),
    deptID integer,
    passwd varchar(20),
    foreign key (deptID) references departments(deptID)
);


CREATE TABLE reports(
    reportID integer primary key AUTO_INCREMENT,
    timest varchar(50),
    address varchar(200),
    reportname varchar(50),-- filename
    report_status varchar(15),
    deptID INTEGER,
    evidancename varchar(50),
    FOREIGN KEY(deptID) REFERENCES departments(deptID)
);

