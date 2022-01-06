FROM python:3.9-alpine3.15

COPY . /

RUN pip install -r requirements.txt

ENTRYPOINT ["/main.py"]
