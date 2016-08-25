# -*- coding: utf-8 -*-

import datetime
import time
import sys

from Worker import Worker
from lib import Logger

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse

conf_file = './conf/Daemon.conf'

class ExecutorDaemon(BaseHTTPRequestHandler):

    def setUp(self):
        self.worker = Worker(conf_file)
        self.config = self.worker.config
        self.tasks = self.config.sections()
        self.last_tasks = {}

    def do_GET(self):
        self.setUp()
        if '/' == self.path:
            self.send_response(200)
            self.end_headers()
            message = self.index()
            self.wfile.write(message)
            self.wfile.write('\n')
            return

        task = self.path[1:]
        if not task in self.tasks:
            self.send_response(404)
            self.end_headers()
            return
        else:
            message = self.worker.run(task)
            if message is None:
                self.send_response(404)
            else:
                self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
            self.wfile.write('\n')
        return

    def index(self):
        content = ""
        content = '<ul class="list-group">'
        content = '</ul>'
        label = 'label-default'
        for task in self.tasks:
            title = self.config.get(task, "sinker.title")
            if 'mana' in task.lower():
                label = 'label-primary'
            elif 'native' in task.lower():
                label = 'label-success'
            elif 'ssp' in task.lower():
                label = 'label-default'
            content += '<li class="list-group-item">'
            content += ('<tab><a href="/' + task + '">' + title + '</a></tab>')
            content += ('<span class="label ' + label + ' label-pill pull-xs-right">' + task + '</span>')
            content += '</li>'
        return '<html><head><link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet"><style type="text/css">tab{padding-left: 1em;padding-right: 6em;}</style></head><body>' +  content + '</body></html>'


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 8087), ExecutorDaemon)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

