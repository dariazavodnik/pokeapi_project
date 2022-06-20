**Структура проекта**

**1. Pokemon API => Python**

utils/extract.py достает данные из API по всем необходимым параметрам, из урлов берутся только айдишники

utils/main.py реализует загрузку нужного типа данных в 2 потока

**2. Python => MWAA => S3**

utils/s3 вынесенные отдельно функции для записи данных в S3 бакет

dags - get_pokemon загружает данные по покемонам разово, check_generation следит за поколениями с ежедневным запуском

examples - примеры полученных json файлов, аналогичные лежат в бакете de-school-snowflake/snowpipe/Zavodnik/

**3. S3 => Snowflake**

to be continued...







  
