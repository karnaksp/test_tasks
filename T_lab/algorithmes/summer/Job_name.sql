/*Чтобы определить должность (Jobtitles.name) со вторым по величине уровнем зарплаты, 
можно использовать следующий запрос:*/
SELECT jt.name
FROM Jobtitles jt
JOIN (
    SELECT jobtitle_id,
    DENSE_RANK() OVER (ORDER BY MAX(salary) DESC) as salary_rank
    FROM Staff
    GROUP BY jobtitle_id
) s ON jt.jobtitle_id = s.jobtitle_id
WHERE s.salary_rank = 2;
