# -*- coding: utf-8 -*-
# Copyright 2012 Antoine Bertin <diaoulael@gmail.com>
#
# This file is part of pyextdirect.
#
# pyextdirect is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyextdirect is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyextdirect.  If not, see <http://www.gnu.org/licenses/>.
from configuration import merge_configurations
from collections import defaultdict
import inspect
import json


def create_api(bases, url, namespace):
    """Create the JS code for the API using a list of configuration :class:`Bases <pyextdirect.configuration.Base>`"""
    return 'Ext.app.REMOTING_API = %s;' % json.dumps(create_api_dict(bases, url, namespace))


def create_api_dict(bases, url, namespace):
    """Create an API dict

    :param bases: configuration bases
    :type bases: :class:`~pyextdirect.configuration.Base` or list of :class:`~pyextdirect.configuration.Base`
    :param string url: URL where the router can be reached
    :param string namespace: client namespace for this API

    """
    api = {'type': 'remoting', 'url': url, 'namespace': namespace, 'actions': defaultdict(list)}
    if not isinstance(bases, list):
        bases = [bases]
    configuration = merge_configurations([b.configuration for b in bases])
    for action, methods in configuration.iteritems():
        for method, element in methods.iteritems():
            if isinstance(element, tuple):
                func = getattr(element[0], element[1])
                attrs = len(inspect.getargspec(func)[0]) - 1
            else:
                func = element
                attrs = len(inspect.getargspec(func)[0])
            spec = {'name': method, 'len': attrs}
            if func.exposed_form:
                spec['formHandler'] = True
            api['actions'][action].append(spec)
    return api
