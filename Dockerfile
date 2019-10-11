# Simple Dockerfile can be expanded
FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["start.py"]