CREATE TABLE IF NOT EXISTS aggregated_data.hourly_aggregate (
    city VARCHAR(255),
    date DATE,
    hour INT,
    temperature_avg FLOAT,
    pressure_avg FLOAT
);

INSERT INTO aggregated_data.hourly_aggregate (city, date, hour, temperature_avg, pressure_avg)
SELECT
    city,
    date,
    hour,
    AVG(temperature_c) OVER (PARTITION BY city, date ORDER BY hour ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS temperature_avg,
    AVG(pressure_mm) OVER (PARTITION BY city, date ORDER BY hour ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS pressure_avg
FROM
    raw_data.weather_data;
