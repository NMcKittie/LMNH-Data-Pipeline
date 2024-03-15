
DROP DATABASE museum;

CREATE DATABASE museum;
\c museum


CREATE TABLE floor(
    floor_id SMALLINT UNIQUE NOT NULL,
    floor_num SMALLINT NOT NULL,
    floor_name VARCHAR(15) UNIQUE,
    PRIMARY KEY(floor_id)
);


CREATE TABLE department(
    dep_id SMALLINT UNIQUE GENERATED ALWAYS AS IDENTITY, 
    department_name VARCHAR(30) UNIQUE,
    PRIMARY KEY(dep_id)
);

CREATE TABLE exhibition(
    exhibition_id VARCHAR(6) UNIQUE NOT NULL,
    exhibition_name VARCHAR(30) NOT NULL,
    ex_description text,
    floor_id SMALLINT NOT NULL,
    dep_id SMALLINT NOT NULL,
    exhibit_start DATE NOT NULL,
    PRIMARY KEY(exhibition_id),
    CONSTRAINT fk_floor
        FOREIGN KEY(floor_id) 
            REFERENCES floor(floor_id),
    CONSTRAINT fk_dep
        FOREIGN KEY(dep_id) 
            REFERENCES department(dep_id)
);

CREATE TABLE rating_details(
    rating_id SMALLINT UNIQUE,
    rating_val SMALLINT NOT NULL,
    rating_description VARCHAR(10) NOT NULL GENERATED ALWAYS AS(
        CASE
            WHEN rating_val = 0 THEN 'Terrible'
            WHEN rating_val = 1 THEN 'Bad'
            WHEN rating_val = 2 THEN 'Neutral'
            WHEN rating_val = 3 THEN 'Good'
            WHEN rating_val = 4 THEN 'Amazing'
            ELSE 'Invalid'
        END
    ) STORED,
    PRIMARY KEY(rating_id)
);


CREATE TABLE type_details(
    type_details_id SMALLINT UNIQUE,
    type_val SMALLINT NOT NULL,
    type_name VARCHAR(10) GENERATED ALWAYS AS(
        CASE
            WHEN type_val = 0 THEN 'assistance'
            WHEN type_val = 1 THEN 'emergency'
            ELSE 'Invalid'
        END
    ) STORED,
    PRIMARY KEY(type_details_id)

);

CREATE TABLE rating(
    val_id SMALLINT UNIQUE GENERATED ALWAYS AS IDENTITY,
    rating_id SMALLINT,
    exhibition_id VARCHAR(6) NOT NULL,
    vote_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(val_id),
    CONSTRAINT fk_site
        FOREIGN KEY(exhibition_id) 
            REFERENCES exhibition(exhibition_id),
    CONSTRAINT fk_rating
        FOREIGN KEY(rating_id) 
            REFERENCES rating_details(rating_id)
);

CREATE TABLE type(
    type_id SMALLINT UNIQUE GENERATED ALWAYS AS IDENTITY,
    type_details_id SMALLINT,
    exhibition_id VARCHAR(6) NOT NULL,
    request_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(type_id),
    CONSTRAINT fk_site
        FOREIGN KEY(exhibition_id) 
            REFERENCES exhibition(exhibition_id),
    CONSTRAINT fk_type
        FOREIGN KEY(type_details_id) 
            REFERENCES type_details(type_details_id)
);


INSERT INTO rating_details (
    rating_id, rating_val
)
VALUES(0,0),(1,1),(2,2),(3,3),(4,4);

INSERT INTO type_details (
    type_details_id, type_val
)
VALUES(0,0),(1,1);

INSERT INTO floor (
    floor_id, floor_num, floor_name
)
VALUES(0,0,'Vault'),(1,1,'1'),(2,2,'2'),(3,3,'3'),(4,4,'Planetarium');


INSERT INTO department (
    department_name
)
VALUES('Technology'),('Astronomy'),('Zoology'),('Biology'), ('Paleontology'), ('Entomology'), ('Geology'), ('Ecology');

INSERT INTO exhibition (
    exhibition_id, exhibition_name, ex_description, floor_id, dep_id, exhibit_start
)
VALUES 
    ('EXH_03', 'Cetacean Sensations', 'Whales: from ancient myth to critically endangered', 1, 3, '2019-07-01'),
    ('EXH_02', 'The Crenshaw Collection', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife', 2, 3, '2021-03-03'),
    ('EXH_05', 'Thunder Lizards', 'How new research is making scientists rethink what dinosaurs really looked like', 1, 5, '2023-02-01'),
    ('EXH_01', 'Adaptation', 'How insect evolution has kept pace with an industrialised world', 0, 6, '2019-07-01'),
    ('EXH_00', 'Measureless to Man', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system', 1, 7, '2021-08-23'),
    ('EXH_04', 'Our Polluted World', 'A hard-hitting exploration of humanitys impact on the environment', 3, 8, '2021-05-12')

