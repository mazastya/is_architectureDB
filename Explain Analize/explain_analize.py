import os
import re
import psycopg2
from datetime import datetime

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="name",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# SQL-запросы, полученные от преподавателя
queries = [
    # вывести кол-во учителей для каждого региона
    "SELECT r.name, COUNT(t.teacher_id) AS teacher_count FROM teachers t JOIN regions r ON t.teacher_id = r.teacher_id GROUP BY r.name;",
    # вывести топ донатеров
    "SELECT username, SUM(sum_donate) AS total_donated FROM history_donate GROUP BY username ORDER BY total_donated DESC LIMIT 3;",
    # для каждого учителя вывести школу и методиста
    "SELECT t.teacher_name, t.teacher_surname, t.teacher_lastname, s.name AS school_name, m.name AS methodist_name FROM teachers t LEFT JOIN schools s ON t.teacher_id = s.teacher_id LEFT JOIN methodists_teachers mt ON t.teacher_id = mt.teacher_id LEFT JOIN methodologists m ON mt.methodologist_id = m.methodologist_id;",
    # вывести для каждого предмета кол-во методистов
    "SELECT subject, COUNT(*) AS methodologist_count FROM methodologists GROUP BY subject;",
    # вывести кандидатов которые не прошли отбор
    "SELECT candidate_name, candidate_surname, candidate_lastname, desired_region, phone_number FROM candidates WHERE selection_passed = false;"
]

# Количество попыток для каждого запроса
num_attempts = int(os.environ.get("NUM_ATTEMPTS", "10"))

# Получение текущей даты и времени
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Создание папки для хранения результатов
results_dir = f"results_attempt_{num_attempts}_{current_datetime}"
os.makedirs(results_dir, exist_ok=True)

# Выполнение запросов и запись результатов в файл
def execute_query(query, num_attempts):
    costs_array = []
    total_cost = 0
    cost_pattern = re.compile(r"cost=(\d+\.\d+)\.\.(\d+\.\d+)")
    print(cost_pattern.findall(query))

    for _ in range(num_attempts):
        cur.execute(f"EXPLAIN ANALYZE {query}")
        row = cur.fetchone()[0]
        costs = cost_pattern.findall(row)

        if costs:
            for cost_range in costs:
                start_cost, end_cost = float(cost_range[0]), float(cost_range[1])
                avg_cost = (start_cost + end_cost) / 2
                total_cost += avg_cost
        costs_array.append(total_cost)
        print(f"Found cost {total_cost}")

    return costs_array

for query in queries:
    cost_arr = execute_query(query, num_attempts)
    query_short = query[:20]  # Получаем первые 20 символов запроса
    results = {
        "best_case": min(cost_arr),
        "average_case": sum(cost_arr) / len(cost_arr),
        "worst_case": max(cost_arr)
    }
    file_path = os.path.join(results_dir, f"results_{query_short}.txt")
    with open(file_path, "w") as file:
        file.write(str(results))

# Закрытие соединения с базой данных
cur.close()
conn.close()
