CREATE TABLE IF NOT EXISTS aggregated_data.weather_aggregate (
    city VARCHAR(255),
    date DATE,
    start_rain_hour INT,
    temperature_avg FLOAT,
    pressure_avg FLOAT
);

INSERT INTO aggregated_data.weather_aggregate (city, date, start_rain_hour, temperature_avg, pressure_avg)
SELECT
    city,
    date,
    MIN(hour) AS start_rain_hour,
FROM
    raw_data.weather_data
WHERE
    is_rainy = 1
GROUP BY
    city, date;

