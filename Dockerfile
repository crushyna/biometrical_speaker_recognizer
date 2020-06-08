# Dockerfile - this is a comment. Delete me if you want.
FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["-u", "main.py"]