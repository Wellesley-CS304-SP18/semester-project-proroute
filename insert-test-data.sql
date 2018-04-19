
-- sample data to insert into mysql datatables

insert into user (firstname,lastname,username,email,userid,password,
picture,age,gender,homeState,homeCountry,Ethnicity) values ('Isabel',
'DAlessandro','idalessa','idalessa@wellesley.edu',1,
'$2b$12$uFOVoJbU0EjElr0Z0NSpme3FZVX/n4eCFyQkbBSLfH8ZZeH00VIoe',
load_file('/images/profilepic.png'),21,'female','MA','USA','white');

insert into user (firstname,lastname,username,email,userid,password) values
  ('Jenine','Smith','jsmith','jsmith@email.com',2,
    '$2b$12$rOEQYdEcHr7Vct323pbx1esDZE5qgNJH5jdyrm/2wWZNezDo6bjSC');

insert into education (userid,institution,instState,instCountry,major,major2,
overallRating,review) values (1,'Wellesley College','MA','USA','Neuroscience',
'Computer Science',5.0,'Wellesley is great!');

insert into student (userid) values (2);

insert into mentor (userid,description) values (1,'current senior in'+
  'neuroscience interested in pursuing neuroscience research. Experience in'+
  'lab research')

insert into job (userid,title,jobID,company,description,favoritePart,leastFavoritePart,
task,skill,advice,professionTag,startDate,endDate) values
(1,'Summer Research Assistant',1,'Stanford University','Worked in a Neuroscience
  laboratory conducting research into the molecular basis of mechanosensation
  in C.elegans','I learned new things and met a lot of smart, interesting people',
  'long hours in the lab','two-electrode voltage clamp recordings from Xenopus
  oocytes','data analysis','read primary research articles to expose yourself to research methods
  that are available to answer certain types of questions','research','2017-06','2017-08');

insert into profession (jobID,professionID,professionName,description,tags,coTags) values
  (1,1,'Research Scientist','conduct scientific research in a laboratory','science','academia');

insert into professionRating (jobID,professionID,overallRating,workEnvironment,
jobSecurity,advancement,skills,hours,stress,learn,benefits,realtionships,diffMental,
diffPhysical) values (1,1,5.0,4.0,3.0,4.0,5.0,3.0,4.0,5.0,4.0,5.0,4.0,1.0);

insert into question (userid,questionID,questionText,tag,rating,posted) values
  (2,1,'What is your favorite part about scientific research?','research',4.0,
  '2018-04-18 21:47:00');

insert into answer (userid,questionID,answerID,answerText,rating,posted) values
  (1,1,1,'I like being able to learn and discover new things,and contribute to the
    scientific community',2.0,'2018-04-18 21:48:00');
