FROM python:3.12-alpine as builder
WORKDIR /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /app/venv /app/venv
COPY . .
EXPOSE 80
ENV PSQLPASS=1111 PATH="/app/venv/bin:$PATH"
RUN python manage.py collectstatic
ENTRYPOINT [ "gunicorn", "-w", "3", "stocks_products.wsgi", "-b", "unix:/app/nginx/wsgi.socket" ]
