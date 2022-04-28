FROM python:3.8-alpine

WORKDIR /app

#add venv
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add libffi-dev

RUN pip install pipenv


RUN python -m venv chat-env


COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "main.py"]