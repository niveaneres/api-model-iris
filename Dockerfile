FROM python:3.11

RUN apt-get update 

RUN apt-get install ffmpeg libsm6 libxext6 git -y

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD ["python", "app.py"]