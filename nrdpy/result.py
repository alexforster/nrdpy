# coding: UTF-8
# Copyright © 2017 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.

from __future__ import unicode_literals

try: basestring
except NameError: basestring = str

import os
import sys


class HostResult(object):

    Up = 0  # the host is up
    Down = 1  # the host is down
    Unreachable = 2  # our path to the host is down
    Unknown = 3  # the state of the host cannot be determined

    _state_strings = ['UP', 'DOWN', 'UNREACHABLE', 'UNKNOWN']

    def __init__(self, host=None, state=None, output=None, long_output=None):
        """ :type host: str|None
            :type state: int|None
            :type output: str|None
            :type long_output: str|None
        """

        self.__dict__ = {
            'host':        None,
            'state':       None,
            'output':      None,
            'long_output': None,
            'perf_data':   {}
        }

        if host is not None:
            if not isinstance(host, basestring):
                raise ValueError('host')
            self.host = host

        if state is not None:
            if not isinstance(state, basestring):
                raise ValueError('state')
            self.state = state

        if output is not None:
            if not isinstance(output, basestring):
                raise ValueError('output')
            self.output = output

        if long_output is not None:
            if not isinstance(long_output, basestring):
                raise ValueError('long_output')
            self.long_output = long_output

    def _get_host(self):

        return self.__dict__['host']

    def _set_host(self, value):

        if not isinstance(value, basestring) or len(value.splitlines()) > 1:
            raise ValueError('value')

        self.__dict__['host'] = value

    host = property(_get_host, _set_host)  # type: str

    def _get_state(self):

        return self.__dict__['state']

    def _get_state_string(self):

        return HostResult._state_strings[self.__dict__['state']]

    def _set_state(self, value):

        if not isinstance(value, int) or value < 0 | value > 3:
            raise ValueError('value')

        self.__dict__['state'] = value

    state = property(_get_state, _set_state)  # type: int

    state_string = property(_get_state_string)  # type: str

    def _get_output(self):

        return self.__dict__['output']

    def _set_output(self, value):

        if not isinstance(value, basestring) or len(value.splitlines()) > 1:
            raise ValueError('value')

        self.__dict__['output'] = value

    output = property(_get_output, _set_output)  # type: str

    def _get_long_output(self):

        return self.__dict__['long_output']

    def _set_long_output(self, value):

        if not isinstance(value, basestring):
            raise ValueError('value')

        self.__dict__['long_output'] = value

    long_output = property(_get_long_output, _set_long_output)  # type: str

    def add_perf_data(self, key, value, units='', warning=None, critical=None, minimum=None, maximum=None):
        """ :type key: str
            :type value: int|float
            :type units: str
            :type warning: int|float|None
            :type critical: int|float|None
            :type minimum: int|float|None
            :type maximum: int|float|None
            :rtype: None
        """

        if not isinstance(key, basestring):
            raise ValueError('key')

        if not isinstance(value, (int, float)):
            raise ValueError('value')

        if not isinstance(units, basestring):
            raise ValueError('units')

        if warning is not None and not isinstance(warning, (int, float)):
            raise ValueError('warning')

        if critical is not None and not isinstance(critical, (int, float)):
            raise ValueError('critical')

        if minimum is not None and not isinstance(minimum, (int, float)):
            raise ValueError('minimum')

        if maximum is not None and not isinstance(maximum, (int, float)):
            raise ValueError('maximum')

        self.__dict__['perf_data'][key] = '{}{}{}'.format(
            value,
            units,
            ';{};{};{};{}'.format(
                warning if warning is not None else '',
                critical if critical is not None else '',
                minimum if minimum is not None else '',
                maximum if maximum is not None else ''
            ) if any(v is not None for v in [warning, critical, minimum, maximum]) else ''
        )

    def formatted(self):
        """ :rtype: str
        """

        result = '{}'.format(HostResult._state_strings[self.__dict__['state']])

        if self.__dict__['output'] is not None:
            result += ': {}'.format(self.__dict__['output'])

        if len(self.__dict__['perf_data']) > 0:
            result += ' | {}'.format(' '.join('\'{}\'={}'.format(k, v) for k, v in self.__dict__['perf_data'].items()))

        if self.__dict__['long_output'] is not None:
            result += '\n{}'.format(self.__dict__['long_output'])

        return result


class ServiceResult(object):

    Ok = 0  # the service is operational
    Warning = 1  # the service is operational but possibly degraded
    Critical = 2  # the service is not operational
    Unknown = 3  # the state of the service cannot be determined

    _state_strings = ['OK', 'WARNING', 'CRITICAL', 'UNKNOWN']

    def __init__(self, host=None, service=None, state=None, output=None, long_output=None):
        """ :type host: str|None
            :type service: str|None
            :type state: int|None
            :type output: str|None
            :type long_output: str|None
        """

        self.__dict__ = {
            'host':        None,
            'service':     None,
            'state':       None,
            'output':      None,
            'long_output': None,
            'perf_data':   {}
        }

        if host is not None:
            if not isinstance(host, basestring):
                raise ValueError('host')
            self.host = host

        if service is not None:
            if not isinstance(service, basestring):
                raise ValueError('service')
            self.service = service

        if state is not None:
            if not isinstance(state, basestring):
                raise ValueError('state')
            self.state = state

        if output is not None:
            if not isinstance(output, basestring):
                raise ValueError('output')
            self.output = output

        if long_output is not None:
            if not isinstance(long_output, basestring):
                raise ValueError('long_output')
            self.long_output = long_output

    def _get_host(self):

        return self.__dict__['host']

    def _set_host(self, value):

        if not isinstance(value, basestring) or len(value.splitlines()) > 1:
            raise ValueError('value')

        self.__dict__['host'] = value

    host = property(_get_host, _set_host)  # type: str

    def _get_service(self):

        return self.__dict__['service']

    def _set_service(self, value):

        if not isinstance(value, basestring) or len(value.splitlines()) > 1:
            raise ValueError('value')

        self.__dict__['service'] = value

    service = property(_get_service, _set_service)  # type: str

    def _get_state(self):

        return self.__dict__['state']

    def _get_state_string(self):

        return HostResult._state_strings[self.__dict__['state']]

    def _set_state(self, value):

        if not isinstance(value, int) or value < 0 | value > 3:
            raise ValueError('value')

        self.__dict__['state'] = value

    state = property(_get_state, _set_state)  # type: int

    state_string = property(_get_state_string)  # type: str

    def _get_output(self):

        return self.__dict__['output']

    def _set_output(self, value):

        if not isinstance(value, basestring) or len(value.splitlines()) > 1:
            raise ValueError('value')

        self.__dict__['output'] = value

    output = property(_get_output, _set_output)  # type: str

    def _get_long_output(self):

        return self.__dict__['long_output']

    def _set_long_output(self, value):

        if not isinstance(value, basestring):
            raise ValueError('value')

        self.__dict__['long_output'] = value

    long_output = property(_get_long_output, _set_long_output)  # type: str

    def add_perf_data(self, key, value, units='', warning=None, critical=None, minimum=None, maximum=None):
        """ :type key: str
            :type value: int|float
            :type units: str
            :type warning: int|float|None
            :type critical: int|float|None
            :type minimum: int|float|None
            :type maximum: int|float|None
            :rtype: None
        """

        if not isinstance(key, basestring):
            raise ValueError('key')

        if not isinstance(value, (int, float)):
            raise ValueError('value')

        if not isinstance(units, basestring):
            raise ValueError('units')

        if warning is not None and not isinstance(warning, (int, float)):
            raise ValueError('warning')

        if critical is not None and not isinstance(critical, (int, float)):
            raise ValueError('critical')

        if minimum is not None and not isinstance(minimum, (int, float)):
            raise ValueError('minimum')

        if maximum is not None and not isinstance(maximum, (int, float)):
            raise ValueError('maximum')

        self.__dict__['perf_data'][key] = '{}{}{}'.format(
            value,
            units,
            ';{};{};{};{}'.format(
                warning if warning is not None else '',
                critical if critical is not None else '',
                minimum if minimum is not None else '',
                maximum if maximum is not None else ''
            ) if any(v is not None for v in [warning, critical, minimum, maximum]) else ''
        )

    def formatted(self):
        """ :rtype: str
        """

        result = '{}'.format(self.state_string)

        if self.__dict__['output'] is not None:
            result += ': {}'.format(self.__dict__['output'])

        if len(self.__dict__['perf_data']) > 0:
            result += ' | {}'.format(' '.join('\'{}\'={}'.format(k, v) for k, v in self.__dict__['perf_data'].items()))

        if self.__dict__['long_output'] is not None:
            result += '\n{}'.format(self.__dict__['long_output'])

        return result
