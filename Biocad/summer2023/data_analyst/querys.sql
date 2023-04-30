""" 
Задание 1: Найдите фамилию и имя ученика с неуказанным отчеством в таблице Student, у
которого в расписании есть занятие с учителем Моисеевым Богданом Романовичем (Moiseev 
Bogdan Romanovich)
"""

SELECT DISTINCT s.first_name, s.last_name
FROM Schedule sch
INNER JOIN Teacher t ON sch.teacher = t.id
INNER JOIN Student_in_class sic ON sch.class = sic.class
INNER JOIN Student s ON sic.student = s.id
WHERE s.middle_name IS NULL
AND t.first_name = 'Bogdan'
AND t.last_name = 'Moiseev'
AND t.middle_name = 'Romanovich';

""" 
Задание 2: Найдите уроки, на которых у учителя Андрея Евсеева (Andrej Evseev) будет больше 
одного класса. В результате выведите дату, начало урока, конец урока, порядковый номер 
урока, количество классов на одном уроке.
"""

SELECT s.date, tp.start_pair, tp.end_pair, s.number_pair, COUNT(DISTINCT c.name) as classes_count
FROM Schedule s
JOIN Timepair tp ON s.number_pair = tp.id
JOIN Teacher t ON s.teacher = t.id
JOIN Subject su ON s.subject = su.id
JOIN Class c ON s.class = c.id
WHERE t.first_name = 'Andrej' AND t.last_name = 'Evseev'
GROUP BY s.date, s.number_pair
HAVING COUNT(DISTINCT c.name) > 1;

""" 
Задание 3: Посчитайте сколько в расписании уроков в сентябре 2019 у классов с буквой “A” в названии.
"""

SELECT COUNT(*) AS lesson_count
FROM Schedule s
JOIN Class c ON s.class = c.id
WHERE c.name LIKE '%A' AND s.date BETWEEN '2019-09-01' AND '2019-09-30';

""" 
Задание 4: Посчитайте сколько часов занимают занятия языками по расписанию. Сгруппируйте 
результат по предмету и классу. Округлите количество часов до одного знака после запятой.
"""

SELECT su.name AS subject_name, c.name AS class_name, ROUND(SUM(TIME_TO_SEC(TIMEDIFF(tp.end_pair, tp.start_pair)))/3600, 1) AS total_hours
FROM Schedule s
JOIN Timepair tp ON s.number_pair = tp.id
JOIN Subject su ON s.subject = su.id
JOIN Class c ON s.class = c.id
WHERE su.name IN ('Russian language', 'English language')
GROUP BY su.name, c.name;

"""
Задание 5: Выведите полный список учителей и студентов с указанием типа (student или 
teacher).
"""

SELECT 'student' AS type, CONCAT_WS(' ', first_name, middle_name , last_name) AS full_name 
FROM Student
UNION
SELECT 'teacher' AS type, CONCAT_WS(' ', first_name, middle_name , last_name) AS full_name 
FROM Teacher
ORDER BY type, full_name;
