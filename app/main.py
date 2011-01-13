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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import app.connection

class MainHandler(webapp.RequestHandler):
    def get(self):
        cfile = file('../config/config.yaml', 'r')
        config = yaml.load(cfile)
        cfile.close()
        logging.info("CONFIG: %s", config)
        sg = app.connection.connect(config['shotgun']['site'], config['shotgun']['script'])
        proj = sg.find_one('Project', [['name', 'is', config['shotgun']['project']]], fields=['id', 'name'])
        vers = sg.find('Version', [['project', 'is', {'type': 'Project', 'id': proj['id']}]], fields=['code', 'description'], limit=10)
        self.response.out.write(template.render('../tmpl/main.html', locals()))

class EditDescriptionsHandler(webapp.RequestHandler):
    def post(self):
        reqs = []
        for arg in self.request.arguments():
            reqs.append({
                'request_type': 'update',
                'entity_type': 'Version',
                'entity_id': int(arg),
                'data': {
                    'description': self.request.get(arg),
                }
            })
        cfile = file('../config/config.yaml', 'r')
        config = yaml.load(cfile)
        cfile.close()
        logging.info("CONFIG: %s", config)
        sg = app.connection.connect(config['shotgun']['site'], config['shotgun']['script'])
        sg.batch(reqs)
        self.response.out.write('Updated.<p/><a href="/">Home</a>')

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/edit_descriptions', EditDescriptionsHandler),
                                         ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
