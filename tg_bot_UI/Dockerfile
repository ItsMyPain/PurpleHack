FROM python:3.10-slim

WORKDIR /usr/src/app

RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "bot.py" ]