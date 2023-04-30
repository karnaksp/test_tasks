SELECT DISTINCT s.first_name, s.last_name
FROM Schedule sch
INNER JOIN Teacher t ON sch.teacher = t.id
INNER JOIN Student_in_class sic ON sch.class = sic.class
INNER JOIN Student s ON sic.student = s.id
WHERE s.middle_name IS NULL
AND t.first_name = 'Bogdan'
AND t.last_name = 'Moiseev'
AND t.middle_name = 'Romanovich';