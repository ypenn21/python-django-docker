FROM python:3.12.4-alpine

LABEL maintainer="Yanni Peng"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apk update \
  && apk add --no-cache build-base curl postgresql-dev geos-dev \
  && addgroup -g "${GID}" python \
  && adduser -D -u "${UID}" -G python python \
  && mkdir -p /public_collected public \
  && mkdir -p ./bin \
  && chown python:python -R /public_collected /app

USER python

COPY --chown=python:python requirements*.txt ./

# Upgrade pip before installing requirements
RUN pip install --user --upgrade pip \
  && pip install --user --no-cache-dir -r requirements.txt

COPY --chown=python:python . .

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    DJANGO_SETTINGS_MODULE="config.settings" \
    PYTHONPATH="$PYTHONPATH:/app" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

WORKDIR /app/src

EXPOSE 8000
CMD ["gunicorn", "-c", "python:config.gunicorn", "config.wsgi"]
#CMD ["python", "manage.py", "runserver", "8000"]
