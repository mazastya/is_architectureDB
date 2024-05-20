-- вывести кол-во учителей для каждого региона

EXPLAIN ANALYSE SELECT r.name, COUNT(t.teacher_id) AS teacher_count
FROM teachers t
JOIN regions r ON t.teacher_id = r.teacher_id
GROUP BY r.name;

-- вывести топ донатеров
EXPLAIN ANALYSE SELECT username, SUM(sum_donate) AS total_donated
FROM history_donate
GROUP BY username
ORDER BY total_donated DESC
LIMIT 3;

-- для каждого учителя вывести школу и методиста

EXPLAIN ANALYSE SELECT
    t.teacher_name,
    t.teacher_surname,
    t.teacher_lastname,
    s.name AS school_name,
    m.name AS methodist_name
FROM
    teachers t
LEFT JOIN
    schools s ON t.teacher_id = s.teacher_id
LEFT JOIN
    methodists_teachers mt ON t.teacher_id = mt.teacher_id
LEFT JOIN
    methodologists m ON mt.methodologist_id = m.methodologist_id;



-- вывести для каждого предмета кол-во методистов
EXPLAIN ANALYSE SELECT subject, COUNT(*) AS methodologist_count
FROM methodologists
GROUP BY subject;

-- вывести кандидатов которые не прошли отбор
EXPLAIN ANALYSE SELECT
    candidate_name,
    candidate_surname,
    candidate_lastname,
    desired_region,
    phone_number
FROM
    candidates
WHERE
    selection_passed IS FALSE;
