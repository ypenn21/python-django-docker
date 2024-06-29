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


run docker container:

docker build -f ./Dockerfile -t django .

docker run --rm -p 8000:8000 \
  -e PYTHONDONTWRITEBYTECODE=true \
  -e SECRET_KEY=insecure_key_for_dev \
  -e ALLOWED_HOSTS=* \
  -e WEB_CONCURRENCY=1 \
  -e WEB_RELOAD=true \
  django

add the following environment variables to the run configurations in IDE;
PYTHONDONTWRITEBYTECODE=true;SECRET_KEY=insecure_key_for_dev;DEBUG=false;ALLOWED_HOSTS=*;WEB_CONCURRENCY=1;WEB_RELOAD=true

allow unauthenticated policy for cloudrun:
gcloud resource-manager org-policies set-policy policy.yaml --organization=$ORG_ID

