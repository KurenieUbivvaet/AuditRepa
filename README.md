Проект отправки аудита
======================

Порядок запуска проектов
------------------------
 
1. Первым запускается проект AuditModule
2. Вторым запускается api_getway
*Важно запускать их из разных терминалов*

AuditModul настройка и запуск
-----------------------------

1. Необходимо перейти в каталог проекта:
`cd ./путь_до_проекта/AuditModul`

2. Потом нужно собрать Docker с помощью команды:
`sudo docker build -t audit_module .`
*далее необходимо будет ввести пароль администратора*

3. Запустить проект внутри контейнера:
`sudo docker run -p 50052:50052 audit_module`  

4. Осановить отладку можно с помощью сочитания клавиш `Ctrl+C`

api_getwey настройка и запуск
-----------------------------

1. Необходимо перейти в каталог проекта:
`cd ./путь_до_проекта/api_getway`

2. Потом нужно собрать Docker с помощью команды:
`sudo docker build -t api_getway .`
*далее необходимо будет ввести пароль администратора*

3. Запустить проект внутри контейнера:
`sudo docker run -p 5000:5000 api_getway`  

4. Осановить отладку можно с помощью сочитания клавиш `Ctrl+C`
