FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel
RUN pip3 install gunicorn uvloop httptools

#COPY requirements.txt /app/requirements.txt

COPY . /fastapi
RUN pip3 install -r /fastapi/requirements.txt

WORKDIR /fastapi/
#ENTRYPOINT ["/usr/local/bin/gunicorn", "-b 0.0.0.0:8000", "-w 4","-k uvicorn.workers.UvicornWorker app.main:main", "--chdir /fastapi/"]
