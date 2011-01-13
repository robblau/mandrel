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
#
from google.appengine.ext import db

import lib.shotgun_api3

class ShotgunScript(db.Model):
    base_url = db.StringProperty(verbose_name='Base Url', required=True)
    script_name = db.StringProperty(verbose_name='Script Name', required=True)
    api_key = db.StringProperty(verbose_name='API Key', required=True)

def connect(url, script):
    query = ShotgunScript.all()
    query.filter("base_url =", url)
    query.filter("script_name =", script)
    matches = query.fetch(2)
    if len(matches) == 0:
        raise ValueError("Script not found: %s at %s" % (script, url))
    if len(matches) > 1:
        raise ValueError("Multiple scripts found: %s at %s" % (script, url))
    script = matches[0]
    return lib.shotgun_api3.Shotgun(script.base_url, script.script_name, script.api_key, convert_datetimes_to_utc=False)
