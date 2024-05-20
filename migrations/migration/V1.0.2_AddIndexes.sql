-- не изменилось
-- create index if not exists index_username
--        on history_donate (username);
-- drop index index_username;

-- стало лучше работать
create index index_subject
on methodologists (subject)
-- drop index index_subject

-- не изменилось
-- create index if not exists index_name
-- on regions (name);
-- drop index  index_name;

-- не изменилось
-- create index if not exists index_teacher_id
-- on regions (teacher_id);
-- drop index  index_teacher_id;

-- не изменилось
-- create index if not exists index_teacher_id
-- on teachers (teacher_id);
-- drop index  index_teacher_id;

