volume 

docker run \
    -d \
    -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=1111 \
    -e POSTGRES_DB=djangocrud \
    --network project-net \
    --name=database \
    postgres:16-alpine

docker run \
    -d \
    -p 80:80 \
    --network project-net \
    -e HOSTNAME=172.18.0.1
    -v /socket:/app/static \
    crud:v3
