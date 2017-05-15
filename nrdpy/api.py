# coding: UTF-8
# Copyright © 2017 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.

from __future__ import unicode_literals

try: basestring
except NameError: basestring = str

import os
import sys
import xml.dom.minidom

import requests
import requests.exceptions

from . import HostResult, ServiceResult


class NRDP(object):

    def __init__(self, endpoint, token, auth=None, cert=None):
        """ :type endpoint: str
            :type token: str
            :type auth: tuple|None
            :type cert: str|tuple|None
        """

        if not isinstance(endpoint, basestring):
            raise ValueError('endpoint')

        if not isinstance(token, basestring):
            raise ValueError('token')

        if auth is not None and not isinstance(auth, tuple):
            raise ValueError('auth')

        if cert is not None and not isinstance(cert, (str, tuple)):
            raise ValueError('cert')

        self._endpoint = endpoint
        self._token = token
        self._auth = auth
        self._cert = cert

    def submit(self, results):
        """ :type results: list[HostResult|ServiceResult]
            :rtype: bool
        """

        dom = xml.dom.minidom.getDOMImplementation()

        document = dom.createDocument(None, None, None)

        checkresults = document.createElement('checkresults')

        for result in results:

            if isinstance(result, HostResult):

                checkresult = document.createElement('checkresult')
                checkresult.setAttribute('type', 'host')
                checkresult.setAttribute('checktype', '1')

                hostname = document.createElement('hostname')
                hostname.appendChild(document.createTextNode(result.host))
                checkresult.appendChild(hostname)

                state = document.createElement('state')
                state.appendChild(document.createTextNode(str(result.state)))
                checkresult.appendChild(state)

                output = document.createElement('output')
                output.appendChild(document.createTextNode(result.formatted()))
                checkresult.appendChild(output)

                checkresults.appendChild(checkresult)

            elif isinstance(result, ServiceResult):

                checkresult = document.createElement('checkresult')
                checkresult.setAttribute('type', 'service')
                checkresult.setAttribute('checktype', '1')

                hostname = document.createElement('hostname')
                hostname.appendChild(document.createTextNode(result.host))
                checkresult.appendChild(hostname)

                servicename = document.createElement('servicename')
                servicename.appendChild(document.createTextNode(result.service))
                checkresult.appendChild(servicename)

                state = document.createElement('state')
                state.appendChild(document.createTextNode(str(result.state)))
                checkresult.appendChild(state)

                output = document.createElement('output')
                output.appendChild(document.createTextNode(result.formatted()))
                checkresult.appendChild(output)

                checkresults.appendChild(checkresult)

            else:

                raise ValueError('results')

        document.appendChild(checkresults)

        document = bytes(document.toprettyxml(encoding='UTF-8'))

        try:

            response = requests.post(
                self._endpoint,
                data={'cmd': 'submitcheck', 'token': self._token, 'XMLDATA': document},
                auth=self._auth,
                cert=self._cert,
                stream=False
            )

            return response.ok

        except requests.exceptions.RequestException:

            return False
