#!/bin/sh
sudo cp container.logs /etc/logrotate.d/container.logs
sudo logrotate -fv /etc/logrotate.d/container.logs
