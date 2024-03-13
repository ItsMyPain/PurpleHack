FROM cnstark/pytorch:2.0.1-py3.10.11-cuda11.8.0-ubuntu22.04

WORKDIR /llama

RUN apt-get update && apt-get upgrade -y
RUN python3 -m pip install --upgrade pip
COPY requirements.txt /llama
RUN python3 -m pip install -r requirements.txt
RUN pip install -i https://pypi.org/simple/ bitsandbytes

COPY . /llama

EXPOSE 8888
