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
import pprint
import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import app.connection

class AmiHandler(webapp.RequestHandler):
    def post(self):
        args = dict([(arg, self.request.get(arg)) for arg in self.request.arguments()])
        site = "https://%(server_hostname)s" % args
        reqs = []
        for vId in [int(s) for s in args['selected_ids'].split(',')]:
            reqs.append({
                'request_type': 'update',
                'entity_type': args['entity_type'],
                'entity_id': vId,
                'data': {
                    'description': datetime.datetime.now().isoformat(),
                }
            })
        sg = app.connection.connect(site, 'mandrel')
        sg.set_session_uuid(args['session_uuid'])
        sg.batch(reqs)
        self.response.out.write(template.render('../tmpl/ami.html', locals()))

def main():
    application = webapp.WSGIApplication([('/ami', AmiHandler), ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

