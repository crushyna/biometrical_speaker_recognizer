# Dockerfile - this is a comment. Delete me if you want.
FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV UWSGI_INI /app/app/uwsgi.ini
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 32
ENV NGINX_WORKER_PROCESSES auto
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]