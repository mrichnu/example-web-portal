FROM python:3.4

RUN groupadd -r gunicorn && useradd -r -g gunicorn gunicorn

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

USER gunicorn

CMD ["/bin/bash", "/usr/src/app/cmd.sh"]