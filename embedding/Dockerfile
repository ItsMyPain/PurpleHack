FROM pytorch/pytorch:latest


RUN apt-get update && apt-get upgrade -y


RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 8889