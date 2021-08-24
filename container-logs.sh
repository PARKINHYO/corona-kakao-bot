#!/bin/sh
sudo cp container-logs.conf /etc/logrotate.d/container-logs.conf
sudo logrotate -fv /etc/logrotate.d/container-logs.conf
