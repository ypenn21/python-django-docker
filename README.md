Run the App:

python -V
pip install -r requirements.txt
source .env.example
python /home/user/python-django/src/manage.py runserver 8000

host:8000/
host:8000/up
host:8000/up/status


run tests:
export PYTHONPATH=$PYTHONPATH:/home/user/python-django/src
export DJANGO_SETTINGS_MODULE=config.settings
python .tests/django_tests.py

run tests in intellji test configuration:
#add the following environment variables to the run configurations in IDE;
PYTHONPATH=$PYTHONPATH:/home/user/python-django/src;DJANGO_SETTINGS_MODULE=config.settings


run docker container:

docker build -f ./Dockerfile -t django .

docker run --rm -p 8000:8000 \
  -e PYTHONDONTWRITEBYTECODE=true \
  -e WEB_CONCURRENCY=1 \
  -e WEB_RELOAD=true \
  django

allow unauthenticated policy for cloudrun:
gcloud resource-manager org-policies set-policy policy.yaml --organization=$ORG_ID

