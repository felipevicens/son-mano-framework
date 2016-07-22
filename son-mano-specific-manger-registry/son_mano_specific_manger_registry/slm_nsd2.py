"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""


import logging
import json
import time
import os
import threading

from sonmanobase import messaging
from sonmanobase.plugin import ManoBasePlugin

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("son-mano-fakeslm")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class fakesmlU(object):

    def __init__(self):

        self.name = 'fake-slm-update'
        self.version = '0.1-dev'
        self.description = 'description'

        LOG.info(
            "Starting SLM:..." )
        # create and initialize broker connection
        self.manoconn = messaging.ManoBrokerRequestResponseConnection(self.name)


        self.result = {'on-board':None, 'instantiation':None}
        # register to plugin manager
        self.publish_update_nsd()

        # jump to run
        self.run()

    def run(self):

        # go into infinity loop

        while True:
            time.sleep(1)

    def publish_update_nsd(self):

        message = {'name': 'ssm2',
                   'version': '0.1',
                   'uri': 'registry.sonata-nfv.eu:5000/ssm/ssm2'}

        self.manoconn.call_async(self._on_publish_update_nsd_response,
                                 'specific.manager.registry.ssm.update',
                                 json.dumps(message))

    def _on_publish_update_nsd_response(self, ch, method, props, response):

        response = json.loads(str(response))#, "utf-8"))
        if response['instantiation'] == 'OK' and response['on-board'] == 'OK':
            LOG.info("pull and instantiation done")
        else:
            LOG.error("SMR instantiation failed. Exit.")
            exit(1)

def main():
    fakesmlU()

if __name__ == '__main__':
    main()
