#Install python, set default workdir, install virtualenv
FROM alpine:latest

#Install python, set default workdir, install virtualenv
RUN apk add --no-cache python3-dev \
  && pip3 install --upgrade pip

WORKDIR /BR-BLACKBOX

COPY . /BR-BLACKBOX

RUN pip3 --no-cache-dir install virtualenv \
  && virtualenv venv

WORKDIR /BR-BLACKBOX/venv/Scripts

RUN activate.bat

WORKDIR /BR-BLACKBOX

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["flask", "run"]



# CMD ["python3", "src/__init__.py"]
#CMD ["flask run"]


#FROM python:3
#WORKDIR /
#RUN pip install virtualenv
#RUN virtualenv venv
#WORKDIR /venv/Scripts
#RUN activate.bat
#RUN ./activate

#WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#CMD [ "python", "./your-daemon-or-script.py" ]