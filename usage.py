# -*- coding: utf-8 -*-
"""
TODO.TXT-CLI-python
Copyright (C) 2011-2012  Sigmavirus24, ytjohn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

TLDR: This is licensed under the GPLv3. See LICENSE for more details.
"""


# enable debug logging while coding
import logging
# logging.basicConfig(level=logging.DEBUG)

class Usage(object):
    """
    Usage class in flux -
    changed syntax as follows:
        @usage('command name', ['help lines', 'as many as needed'])
    """

    def __init__(self, name, lines):
        self.name = name
        self.lines = lines
        self.usage = {}
        # concat = lambda str_list, sep='': sep.join([str(i) for i in
        # str_list])

    def __call__(self, *args, **kwargs):
        # print "%s: " % self.name
        # for line in self.lines:
        #    print "\t%s" % line
        logging.debug("calling function: %s" % __name__)

        def usage_decorator(self, func):
            """Function that actually sets the usage string."""
            logging.debug("real calling func: %s" % __package__)
            return func

        return __name__


