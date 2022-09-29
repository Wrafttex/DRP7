FROM python:latesst

WORKDIR /src
COPY demo.py ./

CMD ["python", "./test.py"]