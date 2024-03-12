FROM nvidia/cuda:12.3.2-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0


RUN python3 -m pip install --upgrade pip
RUN pip3 install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 8888