# Dockerfile - this is a comment. Delete me if you want.
FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV UWSGI_INI /app/uwsgi.ini
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 32
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_MAX_UPLOAD 15m
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# CMD ["main.py"]