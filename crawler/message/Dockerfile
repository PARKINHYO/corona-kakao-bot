FROM python:buster
WORKDIR /corona-kakao-bot
CMD mkdir assets

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /corona-kakao-bot
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    cron \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install google-chrome-stable -y \
    && rm -rf /var/lib/apt/lists/*

COPY crontab /etc/cron.d/crontab
COPY message.py /corona-kakao-bot/message.py
RUN chmod 0744 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]
