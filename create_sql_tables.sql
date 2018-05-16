

DELETE FROM user WHERE email="test@gmail.com";
drop table if exists user;
create table user(
      firstname varchar(20) not null,
      lastname varchar(20) not null,
      email varchar(50) not null,
      userid int(10) primary key not null AUTO_INCREMENT,
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
      degreetype enum('none','highschool','associates','bachelors','masters','phd','other'),
      overallRating float(2,1),
      review text
)
ENGINE=InnoDB;

DELETE FROM student WHERE userid=1;
drop table if exists student;
create table student(
    userid int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    INDEX(userid),
    goal text
)
ENGINE=InnoDB;

drop table if exists mentor;
create table mentor(
    userid int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    INDEX(userid),
    description text,
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
  description text,
  type enum('full time','part time'),
  experience enum('none','less1','1','2','3','4','5plus'),
  favoritePart varchar(200),
  leastFavoritePart varchar(200),
  annualSalary int(15),
  task text,
  dailylife text,
  skill varchar(50),
  advice text,
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
  description text,
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
    questionID int(10) primary key not null AUTO_INCREMENT,
    questionText longtext not null,
    tag varchar(50),
    rating float(2,1),
    posted datetime
)
ENGINE=InnoDB;

drop table if exists answer;
create table answer(
    userid int(10) not null,
    questionID int(10) not null,
    foreign key (userid) references user(userid) on delete restrict,
    foreign key (questionID) references question(questionID) on delete restrict,
    INDEX(userid,questionID),
    answerID int(10) primary key not null AUTO_INCREMENT,
    answerText longtext not null,
    rating float(2,1),
    posted datetime
)
ENGINE=InnoDB;
