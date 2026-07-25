#!/bin/bash
scp -i "$1" -o StrictHostKeyChecking=no "C:\Users\wangc\.qclaw\workspace\aiops-hot\scripts\nginx-aiops-hot.conf" ubuntu@zbit.info:/tmp/aiops-hot.conf
ssh -i "$1" -o StrictHostKeyChecking=no ubuntu@zbit.info "sudo cp /tmp/aiops-hot.conf /etc/nginx/sites-available/aiops-hot.conf && sudo nginx -t && sudo systemctl reload nginx && curl --max-time 5 -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8888"
