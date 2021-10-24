FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN python3 manage.py migrate
RUN python manage.py fillDB --db_size=small