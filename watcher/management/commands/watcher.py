from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class EventHandler(LoggingEventHandler):
    def dispatch(self, event):
        super(EventHandler, self).dispatch(event)
        call_command('collectstatic', interactive=False)


class Command(BaseCommand):
    help = 'Daemon to watch static files and collect them automatically'

    def handle(self, *args, **options):
        try:
            path = settings.BASE_DIR
        except AttributeError:
            path = '.'

        print("Watching: %s" % path)
        event_handler = EventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
