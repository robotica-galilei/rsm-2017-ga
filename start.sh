#!/bin/sh

pm2 start /root/rsm-2017-ga/server/nameserver.py --interpreter="python"
pm2 start /root/rsm-2017-ga/server/server.py --interpreter="python"
