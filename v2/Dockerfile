FROM python:3.8

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE $PORT

CMD ["python", "manage.py", "runserver"]