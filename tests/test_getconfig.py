# TODO.TXT-CLI-python test script
# Copyright (C) 2011-2012  Sigmavirus24
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# TLDR: This is licensed under the GPLv3. See LICENSE for more details.

import todo
import base
import re
import os
from functools import partial
from todotxt import TodoDotTxt
import logging
t = TodoDotTxt(todo.config)

class TestConfig(base.BaseTest):

    def setUp(self):
        file_re = re.compile('(\w+\/\w+\.)config')
        # Just some nice magic:
        self.sub = partial(file_re.sub, '\g<1>plain')
        super(TestConfig, self).setUp()

    def tearDown(self):
        t.config = self.backup

    def config_assert(self, key, val):
        logging.info("\n")
        logging.info("asserted k: %s v: %s" % (key, val))
        logging.info("from config:%s assert:%s" % (t.config[key], val))


        self.assertEquals(t.config[key], val)

    def _validate_(self, filename):
        filename = self.sub(filename)
        with open(filename, 'r') as fd:
            for line in fd:
                if line.startswith('#') or line == '\n':
                    continue
                key, val = line.split()
                logging.info("k,v: %s,%s" % (key, val))
                if val == "False":
                    val = False
                elif val == "True":
                    val = True
                self.config_assert(key, val)

    def test_configs(self):
        self.backup = t.config.copy()
        self.environ = os.environ.copy()
        for f in os.listdir('tests/config/'):
            if f.endswith('config'):
                f = ''.join(['tests/config/', f])
                logging.info("f: %s" % f)
                t.get_config(config_name=f)
                logging.info("1: %s" % t.config)
                self._validate_(f)
                t.config = self.backup.copy()
                os.environ = self.environ.copy()

