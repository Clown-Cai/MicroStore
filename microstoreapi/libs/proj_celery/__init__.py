from celery import Celery


# 实例化celery对象
app = Celery('test')
app.config_from_object('proj_celery.celeryconfig')