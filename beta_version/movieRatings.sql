-- CS 304 Homework 7
-- April 12, 2018
-- Authors: Katy Ma and Isabel D'Alessandro

ALTER TABLE movie
  ADD averageRating float(2,1);

CREATE TABLE IF NOT EXISTS movieRatings (
  userid INT(10) NOT NULL,
  movie_rating ENUM('1','2','3','4','5'),
  tt INT(10) NOT NULL
);
