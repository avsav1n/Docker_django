FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV PSQLPASS=1111
EXPOSE 80
ENTRYPOINT [ "gunicorn", "-w", "3", "stocks_products.wsgi", "-b", "0.0.0.0:80" ]
