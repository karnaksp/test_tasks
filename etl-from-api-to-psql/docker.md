
Здесь `852c07c3682d` - ваш CONTAINER id, который можно посмотреть командой `docker ps`

```docker  
docker-compose up -d 
docker ps
# Копирвоание скриптов на создание
docker cp 'C:\Users\user\OneDrive\Документы\GitHub\internships\API Яндекс.Погоды\create_t.sql' 852c07c3682d:/tmp/
docker cp 'C:\Users\user\OneDrive\Документы\GitHub\internships\API Яндекс.Погоды\weather_data.csv' 852c07c3682d:/tmp/
docker cp 'C:\Users\user\OneDrive\Документы\GitHub\internships\API Яндекс.Погоды\load_data.sql' 852c07c3682d:/tmp/
# Запуск команд на копирвоание данных в БД
docker exec -i 852c07c3682d psql -U karnaksp -d test_api -a -f /tmp/create_t.sql
docker exec -i 852c07c3682d psql -U karnaksp -d test_api -a -f /tmp/load_data.sql
# Копирвоание скриптов на создание витрин
docker cp 'C:\Users\user\OneDrive\Документы\GitHub\internships\API Яндекс.Погоды\weather_moving.sql' 852c07c3682d:/tmp/
docker cp 'C:\Users\user\OneDrive\Документы\GitHub\internships\API Яндекс.Погоды\weather_rainy.sql' 852c07c3682d:/tmp/
# Запуск скриптов на создание витрин
docker exec -i 852c07c3682d psql -U karnaksp -d test_api -a -f /tmp/weather_moving.sql
docker exec -i 852c07c3682d psql -U karnaksp -d test_api -a -f /tmp/weather_rainy.sql
# Проверка
docker exec -i 852c07c3682d psql -U karnaksp -d test_api -c "SELECT * FROM aggregated_data.weather_aggregate limit 5;"

```
