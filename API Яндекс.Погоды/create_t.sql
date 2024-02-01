
CREATE SCHEMA raw_data;
CREATE SCHEMA aggregated_data;

CREATE TABLE IF NOT EXISTS raw_data.weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    date DATE,
    hour INT,
    temperature_c INT,
    pressure_mm INT,
    is_rainy INT,
    condition VARCHAR(255)
);