from __future__ import absolute_import

from celery import celery
from harvester import Harvester

@celery.task
def start_harvesting(field, crop):
    harvester = Harvester(field, crop)
    harvester.start()