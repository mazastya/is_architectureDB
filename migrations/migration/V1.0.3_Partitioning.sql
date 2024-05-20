-- партицирование по регионам
CREATE TABLE IF NOT EXISTS teachers_partitioned_by_region (
    teacher_id       bigint not null,
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
)
PARTITION BY LIST (region);

CREATE TABLE IF NOT EXISTS teachers_region_voronezh_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Воронежская область');

CREATE TABLE IF NOT EXISTS teachers_region_tambov_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Тамбовская область');

CREATE TABLE IF NOT EXISTS teachers_region_yamal_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Ямало-Ненецкий автономный округ');

CREATE TABLE IF NOT EXISTS teachers_region_moscow_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Московская область');

CREATE TABLE IF NOT EXISTS teachers_region_far_east_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Приморский край');

CREATE TABLE IF NOT EXISTS teachers_region_novgorod_area
PARTITION OF teachers_partitioned_by_region
FOR VALUES IN ('Новгородская область');

INSERT INTO teachers_partitioned_by_region SELECT * FROM teachers;


-- партицирование по предметам
CREATE TABLE IF NOT EXISTS teachers_partitioned_by_subject (
    teacher_id       bigint not null,
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
)
PARTITION BY LIST (subject);

CREATE TABLE IF NOT EXISTS teachers_subject_math
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Математика');

CREATE TABLE IF NOT EXISTS teachers_subject_russian
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Русский язык');

CREATE TABLE IF NOT EXISTS teachers_subject_literature
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Литература');

CREATE TABLE IF NOT EXISTS teachers_subject_physics
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Физика');

CREATE TABLE IF NOT EXISTS teachers_subject_chemistry
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Химия');

CREATE TABLE IF NOT EXISTS teachers_subject_history
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('История');

CREATE TABLE IF NOT EXISTS teachers_subject_geography
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('География');

CREATE TABLE IF NOT EXISTS teachers_subject_biology
PARTITION OF teachers_partitioned_by_subject
FOR VALUES IN ('Биология');

INSERT INTO teachers_partitioned_by_subject SELECT * FROM teachers;

