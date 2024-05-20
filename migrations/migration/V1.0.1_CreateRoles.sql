CREATE ROLE reader;
CREATE ROLE writer;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO writer;

CREATE USER analytic WITH PASSWORD 'analytic1';

GRANT SELECT ON teachers TO analytic;

CREATE ROLE restricted_group;

DO
$$
    DECLARE
        i         INT       := 3;
        users     VARCHAR[] := ARRAY ['user1', 'user2', 'user3'];
        passwords VARCHAR[] := ARRAY ['password1', 'password2', 'password3'];
    BEGIN
        FOR i IN ARRAY_LOWER(users, 1)..ARRAY_UPPER(users, 1)
            LOOP
                EXECUTE 'CREATE USER ' || users[i] || ' WITH PASSWORD ''' || passwords[i] || '''';
                EXECUTE 'GRANT restricted_group TO ' || users[i];
            END LOOP;
    END
$$;
