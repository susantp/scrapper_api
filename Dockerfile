FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools
ENV PYTHON_UNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_NAME "fast api"
ENV ADMIN_EMAIL "gracysusant@gmail.com"
ENV DB_URL "mysql+mysqlconnector://root:root@mysql:3306/fastapi"
ENV SCRAP_API_TOKEN "dd424a4ae2c60473bb07132def3b89a1"

COPY . /var/www/fastApi
#COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /var/www/fastApi/requirements.txt

#ENTRYPOINT ["/usr/local/bin/gunicorn", "app.main:app", "--preload", "-b 0.0.0.0:8000","-w 4", "-k uvicorn.workers.UvicornWorker"]
