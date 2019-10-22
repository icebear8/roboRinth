#!/bin/sh

npm run dev &
sleep 10

python3 ${APP_DIR}/mqttapp.py ${SERVICE_ARGS}
