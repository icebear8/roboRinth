ARG BASE_IMG_VERSION=3.10.1
FROM alpine:${BASE_IMG_VERSION}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# User definition
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Environment variables for the service
ENV SERVICE_ARGS="--host=localhost --port=1883"
ENV APP_DIR=/opt/mqttclient

RUN apk update && apk add --no-cache \
  python3 \
  && apk del --purge

RUN pip3 install paho-mqtt

# Create user
RUN addgroup -g ${GID} ${GROUP} \
  && adduser -u ${UID} -G ${GROUP} -D ${USER}

COPY ./simulator ${APP_DIR}/

RUN chown -R ${USER} ${APP_DIR}

USER ${USER}

ENTRYPOINT ["sh", "-c"]
CMD ["python3 ${APP_DIR}/simulator.py ${SERVICE_ARGS}"]
