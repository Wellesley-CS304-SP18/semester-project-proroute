
drop table if exists user;
create table user(
      firstname varchar(20) not null,
      lastname varchar(20) not null,
      username varchar(20) not null,
      email varchar(50) not null,
      userid int(10) primary key not null,
      password char(60) not null,
      picture blob,
      age int(3),
      gender enum('male','female','nonbinary','other'),
      homeState varchar(2),
      homeCountry varchar(50),
      Ethnicity varchar(50)

);

drop table if exists education;
create table education(
      userid int(10) not null,
      foreign key (userid) references user(userid) on delete restrict,
      INDEX(userid),
      institution varchar(100),
      instState varchar(2),
      instCountry varchar(100),
      major varchar(100),
      major2 varchar(100),
      overallRating float(2,1),
      review blob
)
ENGINE=InnoDB;

drop table if exists student;
create table student(
    userid int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    INDEX(userid),
    goal blob
)
ENGINE=InnoDB;

drop table if exists mentor;
create table mentor(
    userid int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    INDEX(userid),
    description blob,
    cv blob
)
ENGINE=InnoDB;

drop table if exists job;
create table job(
  userid int(10) not null,
  foreign key (userid) references user(userid) on delete restrict,
  INDEX(userid),
  title varchar(50) not null,
  jobID int(10) primary key not null,
  company varchar(100),
  description blob,
  favoritePart varchar(200),
  leastFavoritePart varchar(200),
  annualSalary int(15),
  task blob,
  skill varchar(50),
  advice blob,
  professionTag varchar(50),
  startDate date,
  endDate date
)
ENGINE=InnoDB;

drop table if exists profession;
create table profession(
  jobID int(10) not null,
  foreign key(jobID) references job(jobID) on update restrict,
  INDEX(jobID),
  professionID varchar(10) primary key not null,
  professionName varchar(100),
  description blob,
  tags varchar(50),
  coTags varchar(50)
)
ENGINE=InnoDB;

drop table if exists professionRating;
create table professionRating(
  jobID int(10) not null,
  professionID varchar(10) not null,
  foreign key(jobID) references job(jobID) on update restrict,
  foreign key(professionID) references profession(professionID) on update restrict,
  INDEX(jobID,professionID),
  overallRating float(2,1),
  workEnvironment float(2,1),
  jobSecurity float(2,1),
  advancement float(2,1),
  skills float(2,1),
  hours float(2,1),
  stress float(2,1),
  learn float(2,1),
  benefits float(2,1),
  realtionships float(2,1),
  diffMental float(2,1),
  diffPhysical float(2,1)
)
ENGINE=InnoDB;


drop table if exists question;
create table question(
    userid int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    INDEX(userid),
    questionID varchar(10) primary key not null,
    questionText blob not null,
    tag varchar(50),
    rating float(2,1),
    posted datetime
)
ENGINE=InnoDB;

drop table if exists answer;
create table answer(
    userid int(10) not null,
    questionID varchar(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    foreign key (questionID) references question(questionID) on delete restrict,
    INDEX(userid,questionID),
    answerID varchar(10) primary key not null,
    answerText blob not null,
    rating float(2,1),
    posted datetime
)
ENGINE=InnoDB;
