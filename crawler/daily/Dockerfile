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
    fonts-nanum* \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/* \
    && cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/ \
    && rm -rf /root/.cache/matplotlib


COPY crontab /etc/cron.d/crontab
COPY daily.py /corona-kakao-bot/daily.py
RUN chmod 0744 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]
