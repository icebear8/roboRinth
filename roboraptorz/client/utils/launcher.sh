#!/bin/sh

npm run dev &
sleep 30

python3 ${APP_DIR}/mqttapp.py ${SERVICE_ARGS}
