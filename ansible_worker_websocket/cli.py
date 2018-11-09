#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    ansible_worker_websocket [options] <url>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from gevent import monkey
monkey.patch_all(thread=False)

from docopt import docopt
import logging
import sys
from .client import WebsocketChannel
from .worker import AnsibleWorker
import gevent

logger = logging.getLogger('cli')


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    worker = AnsibleWorker()
    wc = WebsocketChannel(parsed_args['<url>'], worker.queue)
    worker.controller.outboxes['output'] = wc
    gevent.joinall([wc.thread, worker.thread])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
