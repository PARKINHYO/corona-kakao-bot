FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /corona-kakao-bot
COPY ./requirements.txt /corona-kakao-bot
RUN pip install -r requirements.txt

