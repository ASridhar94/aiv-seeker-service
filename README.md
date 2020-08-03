### AIV Seeker Service

#### Run locally

##### Run Django service
```shell script
python manage.py runserver
```

##### Start Celery worker
```shell script
celery -A aiv_seeker_service worker -l info
```
