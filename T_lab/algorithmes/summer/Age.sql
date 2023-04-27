/*Запрос текущего возраста сотрудника может выглядеть так:*/
SELECT name,
       (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM birthday)) as age
FROM Staff;