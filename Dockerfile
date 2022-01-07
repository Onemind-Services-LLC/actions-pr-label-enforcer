FROM python:3.9-alpine3.15

RUN apk add gcc libffi-dev make musl-dev

COPY . /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
