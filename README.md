Run the App:
```shell
python -V
pip install -r requirements.txt
source .env.example
python /home/user/python-django/src/manage.py runserver 8000

#endpoints to test:
#host:8000/
#host:8000/up
#host:8000/up/status
````

run tests:
```shell
export PYTHONPATH=$PYTHONPATH:/home/user/python-django/src
export DJANGO_SETTINGS_MODULE=config.settings
python tests/view_tests.py
````

run tests in intellji test configuration:
PYTHONUNBUFFERED=1;PYTHONDONTWRITEBYTECODE=true;WEB_CONCURRENCY=1;WEB_RELOAD=true;DEBUG=true;POSTGRES_HOST=0.0.0.0;POSTGRES_PASSWORD=pword;POSTGRES_PORT=5000;GOOGLE_CLOUD_PROJECT_ID=next24-genai-app

setup the following environment variables to the run configurations in vscode:
export PYTHONPATH=$PYTHONPATH:/home/user/python-django/src;DJANGO_SETTINGS_MODULE=config.settings
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=true
export WEB_CONCURRENCY=1 
export WEB_RELOAD=true
export DEBUG=true 
export POSTGRES_HOST=0.0.0.0 
export POSTGRES_PASSWORD=pword 
export POSTGRES_PORT=5000
export GOOGLE_CLOUD_PROJECT_ID=next24-genai-app


run docker container locally:
```shell
docker build -f ./Dockerfile -t django .

docker run --rm -p 8000:8000 \
  -e PYTHONDONTWRITEBYTECODE=true \
  -e WEB_CONCURRENCY=1 \
  -e WEB_RELOAD=true \
  django

docker run --rm -p 8000:8000 \
  -e PYTHONDONTWRITEBYTECODE=true \
  -e WEB_CONCURRENCY=1 \
  -e WEB_RELOAD=true \
  -e POSTGRES_HOST=0.0.0.0 \
  -e POSTGRES_PASSWORD='pword' \
  -e POSTGRES_PORT=5000 \
  -e GOOGLE_CLOUD_PROJECT_ID=next24-genai-app django:latest
 ```

Run container image build with Cloud Build (will pick up cloudbuild.yaml):
```shell
gcloud builds submit --machine-type E2-HIGHCPU-32

```

allow unauthenticated policy for cloudrun:
```shell
gcloud resource-manager org-policies set-policy policy.yaml --organization=$ORG_ID
```
```shell
gcloud run deploy django 
  --image us-central1-docker.pkg.dev/next24-genai-app/django/django-app:latest \
  --region us-central1 \
  --set-env-vars='PYTHONDONTWRITEBYTECODE=true,PYTHONUNBUFFERED=1,POSTGRES_HOST=0.0.0.0,POSTGRES_PASSWORD=pword,GOOGLE_CLOUD_PROJECT_ID=next24-genai-app' 
  --memory 2Gi \
  --allow-unauthenticated \
  --vpc-connector alloy-connector
```
For vertexai api to you need to authenticate to gcp via gcloud auth login or use sa key:

Using sa key e.g.
export GOOGLE_APPLICATION_CREDENTIALS=/home/user/python-django/sa.json

