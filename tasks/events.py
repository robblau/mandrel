#!/usr/bin/env python
#
# Copyright 2011 Robert Blau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import yaml
import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import app.connection

class EventHandler(webapp.RequestHandler):
    def get(self):
        cfile = file('../config/config.yaml', 'r')
        config = yaml.load(cfile)
        cfile.close()
        logging.info("CONFIG: %s", config)
        sg = app.connection.connect(config['shotgun']['site'], config['shotgun']['script'])
        # Grab interesting events
        events = sg.find('EventLogEntry', [
            ['sg_processed_by_mandrel', 'is', False],
            ['created_at', 'greater_than', datetime.datetime.now() - datetime.timedelta(days=2)]
        ])
        # Process events
        # Mark events processed
        sg.batch([{
            'request_type': 'update',
            'entity_type': 'EventLogEntry',
            'entity_id': event['id'],
            'data': { 'sg_processed_by_mandrel': True, }
           } for event in events])
        logging.info('Processed %s events.', len(events))
        self.response.out.write("Processed %s events." % len(events))

def main():
    application = webapp.WSGIApplication([('/tasks/events', EventHandler), ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

