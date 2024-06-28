Run the App:

source .env.example
/bin/python /home/user/python-django/src/manage.py runserver 8000

host:8000/
host:8000/up
host:8000/up/status


run tests:
export PYTHONPATH=$PYTHONPATH:/home/user/python-django/src


run docker container:

docker build -f ./Dockerfile -t django .

docker run --rm -p 8000:8000 \
  -e PYTHONDONTWRITEBYTECODE=true \
  -e SECRET_KEY=insecure_key_for_dev \
  -e DEBUG=true \
  -e ALLOWED_HOSTS="*" \
  -e WEB_CONCURRENCY=1 \
  -e WEB_RELOAD=true \
  django