from __future__ import absolute_import

from celery import Celery

celery = Celery('web-crawler.celery',
                broker='amqp://',
                backend='amqp://',
                include=['web-crawler.tasks'])

if __name__ == '__main__':
    celery.start()