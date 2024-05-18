DROP TABLE IF EXISTS reviews;

CREATE TABLE IF NOT EXISTS reviews (review_id INTEGER NOT NULL UNIQUE PRIMARY KEY, 
                                    name_ TEXT NOT NULL, 
                                    rating INTEGER NOT NULL, 
                                    location_ TEXT NOT NULL, 
                                    cuisine TEXT NOT NULL, 
                                    price TEXT NOT NULL, 
                                    review TEXT NOT NULL); 

DROP TABLE IF EXISTS recipes;

CREATE TABLE IF NOT EXISTS recipes (recipe_id INTEGER NOT NULL UNIQUE PRIMARY KEY, 
                                    title TEXT NOT NULL, 
                                    imagesource TEXT NOT NULL, 
                                    content TEXT NOT NULL);