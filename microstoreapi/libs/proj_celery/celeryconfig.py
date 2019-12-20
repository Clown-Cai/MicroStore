from datetime import timedelta
from celery.schedules import crontab


BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 指定导入的任务模块
CELERY_IMPORTS = (
    'adminer.task',
    'order.task',
    'product.task',
    'user.task',
)

# 定时任务
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'celery_proj.task1.add',
         'schedule': timedelta(seconds=2),       # 每 2 秒执行一次
         'args': (5, 8)                           # 任务函数参数
    },
}
