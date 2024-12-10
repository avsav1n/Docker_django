# Запуск проекта
## Подготовка 
### Создание тома 
```bash
docker volume create socket
```
### Создание сети 
```bash
docker network create project-net
```
### Создание образов
```bash
docker build . -f ./Dockerfile-postgres -t postgres:v1
docker build . -f ./Dockerfile-nginx -t nginx:v1
docker build . -t django:v1
```
## Запуск контейнеров
### Запуск контейнера с базой данных postgresql
```bash
docker run -d --network project-net --name dbase postgres:v1
```
### Запуск контейнера с nginx сервером
```bash
docker run -d -p 80:80 --network project-net -v /socket:/socket nginx:v1
```
### Запуск контейнера с django проектом
```bash
docker run -d --network project-net -e HOST=dbase --name django -v /socket:/app/nginx django:v1
docker exec django python manage.py migrate
```
