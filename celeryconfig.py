from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-10-seconds': {
        'task': 'web.start_harvesting',
        'schedule': timedelta(seconds=10),
        'args': ('http://www.irwinwong.com/blog/how-the-fuji-x-series-made-me-feel-inadequate/', 'src="([^"]+)"')
    },
}

CELERY_TIMEZONE = 'UTC'
