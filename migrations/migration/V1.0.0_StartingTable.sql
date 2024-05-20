-- Database: educateForEvery

-- DROP DATABASE IF EXISTS "educateForEvery";

-- CREATE DATABASE "educateForEvery"
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'en_US.UTF-8'
--     LC_CTYPE = 'en_US.UTF-8'
--     LOCALE_PROVIDER = 'libc'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;

DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'team_role') THEN
            create type team_role as enum
                (
                    'none',
                    'admin',
                    'teacher',
                    'fundraiser',
                    'manager',
                    'curator',
                    'coordinator',
                    'methodist',
                    'developer'
                    );
        END IF;
    END
$$;


DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
            create type user_role as enum
                (
                    'none',
                    'user',
                    'donate_user',
                    'candidate'
                    );
        END IF;
    END
$$;


CREATE TABLE IF NOT EXISTS commands
(
    command_id bigint primary key generated always as identity,
    teacher    text      not null,
    school     text      not null,
    region     text      not null,
    role       team_role not null
);

CREATE TABLE IF NOT EXISTS methodologists
(
    methodologist_id bigint primary key generated always as identity,
    name             text not null,
    subject          text not null,
    teacher          text not null
);

CREATE TABLE IF NOT EXISTS curators
(
    curator_id bigint primary key generated always as identity,
    region     text not null,
    school     text not null,
    teacher    text not null
);

CREATE TABLE IF NOT EXISTS history_donate
(
    history_donate_id BIGSERIAL PRIMARY KEY,
    username          TEXT NOT NULL,
    time_donate       TIME,
    date_donate       DATE,
    sum_donate        BIGINT
);

CREATE TABLE IF NOT EXISTS users
(
    user_id        BIGSERIAL PRIMARY KEY,
    user_name      TEXT NOT NULL,
    user_surname   TEXT NOT NULL,
    user_lastname  TEXT,
    donate_history BIGINT,
    role           user_role,
    FOREIGN KEY (donate_history) REFERENCES history_donate (history_donate_id)
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id       bigint primary key generated always as identity,
    teacher_name     text    NOT NULL,
    teacher_surname  text    NOT NULL,
    teacher_lastname text,
    phone_number     varchar(20),
    subject          text    NOT NULL,
    region           text    NOT NULL,
    school           text    NOT NULL,
    graduate         boolean NOT NULL,
    curator_id       bigint,
    user_id          bigint,

    FOREIGN KEY (curator_id) REFERENCES curators (curator_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS schools
(
    school_id  bigint primary key generated always as identity,
    teacher_id bigint,
    foreign key (teacher_id) references teachers (teacher_id),
    name       text not null,
    region     text not null
);


CREATE TABLE IF NOT EXISTS regions
(
    region_id  bigint primary key generated always as identity,
    name       text not null,
    teacher_id bigint,
    command_id bigint,
    school     text not null,

    FOREIGN KEY (command_id) REFERENCES commands (command_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
);

CREATE TABLE IF NOT EXISTS candidates
(
    candidate_id       bigint primary key generated always as identity,
    candidate_name     text    not null,
    candidate_surname  text    not null,
    candidate_lastname text,
    desired_region     text    not null,
    phone_number       varchar(20),
    education_received text    not null,
    selection_passed   boolean not null,
    desired_subject    text    not null
);


-- many-to-many

CREATE TABLE IF NOT EXISTS teachers_schools
(
    teacher_id bigint,
    school_id  bigint,
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
    FOREIGN KEY (school_id) REFERENCES schools (school_id)
);

CREATE TABLE IF NOT EXISTS commands_curators
(
    command_id bigint,
    curator_id bigint,
    FOREIGN KEY (command_id) REFERENCES commands (command_id),
    FOREIGN KEY (curator_id) REFERENCES curators (curator_id)
);

CREATE TABLE IF NOT EXISTS methodists_teachers
(
    methodologist_id bigint,
    teacher_id       bigint,
    FOREIGN KEY (methodologist_id) REFERENCES methodologists (methodologist_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
);

CREATE TABLE IF NOT EXISTS regions_schools
(
    school_id bigint,
    region_id bigint,
    FOREIGN KEY (school_id) REFERENCES schools (school_id),
    FOREIGN KEY (region_id) REFERENCES regions (region_id)
);

CREATE TABLE IF NOT EXISTS history_donate_donate_users
(
    history_donate_id bigint,
    user_id           bigint,
    FOREIGN KEY (history_donate_id) REFERENCES history_donate (history_donate_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
