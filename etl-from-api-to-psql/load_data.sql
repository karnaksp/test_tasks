COPY raw_data.weather_data(city, date, hour, temperature_c, pressure_mm, is_rainy, condition)
FROM '/tmp/weather_data.csv' DELIMITER ',' CSV HEADER;
