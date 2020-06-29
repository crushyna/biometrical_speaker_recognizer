# Dockerfile - this is a comment. Delete me if you want.
FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY nginx_custom.conf /etc/nginx/conf.d/nginx_custom.conf
ENV UWSGI_INI /app/uwsgi.ini
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 8
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_MAX_UPLOAD 15m
ENV NGINX_WORKER_OPEN_FILES 2048
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# CMD ["main.py"]