FROM cnstark/pytorch:2.0.1-py3.10.11-cuda11.8.0-ubuntu22.04

WORKDIR /embedding

RUN apt-get update && apt-get upgrade -y
RUN python3 -m pip install --upgrade pip
COPY requirements.txt /embedding
RUN python3 -m pip install -r requirements.txt

COPY . /embedding

EXPOSE 8889

#CMD ["python3", "server.py"]