# syntax=docker/dockerfile:1
FROM python:3.7-buster
WORKDIR /code
ENV FLASK_APP=Hub/app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
# run ["python", "tests.py"]
CMD ["gunicorn", "--certfile", "certs/cert.pem", "--keyfile", "certs/key.pem", "-b", "0.0.0.0:5000", "app:app"]