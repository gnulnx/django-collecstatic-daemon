from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command

import sys
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from logutils.colorize import ColorizingStreamHandler


class ColorHandler(ColorizingStreamHandler):
    def __init__(self, *args, **kwargs):
        super(ColorHandler, self).__init__(*args, **kwargs)
        self.level_map = {
            logging.DEBUG: (None, 'blue', False),
            logging.INFO: (None, 'green', False),
            logging.WARNING: (None, 'yellow', False),
            logging.ERROR: (None, 'red', False),
            logging.CRITICAL: ('red', 'white', True),
        }

CONFIG = {
    'version':1,
    'disable_existing_loggers': True,
    'handlers':{
        'console': {
            '()':ColorHandler,
            # 'info':'white',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)s line:%(lineno)-4d %(levelname)-8s %(message)s',
        },
    },
    'loggers': {
        '': {
            'level':'DEBUG',
            'handlers':['console'],
        },
    },
}

logging.config.dictConfig(CONFIG)
logger = logging.getLogger('')


class EventHandler(LoggingEventHandler):
    wait = False

    def dispatch(self, event):
        super(EventHandler, self).dispatch(event)
        if self.wait:
            return

        # Start a .5 second timer and then run colelctstatic.
        # This gives all of the events time to finish so we only
        # have to run collectstatic 1 time
        self.wait = True
        self.setTimeout(self.run_collectstatic, 0.5)

    def run_collectstatic(self):
        call_command('collectstatic', interactive=False)
        self.wait = False

    def setTimeout(self, func, seconds):
        timer = threading.Timer(seconds, func)
        timer.start()


class Command(BaseCommand):
    help = 'Daemon to watch static files and collect them automatically'

    def handle(self, *args, **options):
        try:
            path = settings.BASE_DIR
        except AttributeError:
            path = '.'

        logger.info("Watching: %s", path)
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
