FROM python:3.7-alpine

WORKDIR /usr/src/parserapp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip 
COPY ./requirements.txt /usr/src/parserapp
RUN pip3 install -r requirements.txt

COPY . /usr/src/parserapp

EXPOSE 8000

COPY docker-entrypoint.sh /usr/src/parserapp

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/usr/src/parserapp/docker-entrypoint.sh"]

CMD ["gunicorn", "parserApp.wsgi:application", "--bind", "0.0.0.0:8000"]
