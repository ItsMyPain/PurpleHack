FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=ubuntu
ARG USERID=1000
RUN useradd --system --create-home --shell /bin/bash --uid $USERID $USERNAME \
 && mkdir /home/$USERNAME/.cache && chown -R $USERNAME /home/$USERNAME/.cache

RUN python3 -m pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt
RUN pip install -i https://pypi.org/simple/ bitsandbytes

USER $USERNAME
COPY --chown=$USERNAME . /home/$USERNAME
WORKDIR /home/$USERNAME

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 8888

#ENTRYPOINT ["python", "nlp.py"]