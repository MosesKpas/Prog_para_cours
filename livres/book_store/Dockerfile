FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBIFFERED 1
#mise à jour de l'installation des paquets 
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    python3-dev \
    gcc libpq-dev \
    default-libmysqlclient-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD [ "sh","-c","python3 manage.py migrate --no-input && python3 manage.py runserver 0.0.0.0:8000" ]