# TODO.TXT-CLI-python test script
# Copyright (C) 2011-2012  Sigmavirus24, Jeff Stein
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

# Common functions for test_*_todo.py
import datetime
import os
import re
import sys
import unittest

sys.path.insert(0, '..')

import todo
from todotxt import TodoDotTxt
t = TodoDotTxt(todo.config)

todotxt = todo.config["TODO_FILE"] = "test_todo.txt"
donetxt = todo.config["DONE_FILE"] = "test_done.txt"

class BaseTest(unittest.TestCase):
    num = 50

    def default_config(self):
        pass

    def setUp(self):
        todo.config["PRE_DATE"] = False
        todo.config["TODO_PY"] = "testing"
        todo.default_config = self.default_config
        sys.stdout = open(os.devnull, 'w')
        open(todotxt, "w+").close()
        open(donetxt, "w+").close()


    def tearDown(self):
        sys.stdout = sys.__stdout__
        if os.path.isfile(todotxt):
            os.unlink(todotxt)
        if os.path.isfile(donetxt):
            os.unlink(donetxt)


    def count_matches(self, regexp=None):
        count = 0
        for line in t.iter_todos():
            if regexp == None or re.match(regexp, line):
                count += 1
        return count


    def _test_lines_no_pri(self, num):
        return ["Test {0}".format(i) for i in range(0, num)]


    def _test_lines_pri(self, num):
        n = len(todo.priorities)
        p = todo.priorities
        return ["({0}) Test {1}".format(p[i % n], i) for i in range(0, num)]


    def _test_lines_date(self, num):
        l = self._test_lines_pri(num)
        m = []
        start_date = datetime.date.today()

        for d, l in zip((start_date + datetime.timedelta(n) for n in range(num)), l):
            m.append(todo.concat([l, " #{%s}" % d.isoformat()]))
        return m


    def _test_lines_project(self, num):
        projects = ["+foo", "+bar", "+bogus", "+github", "+school", "+work",
                "+inthemorning", "+agenda", "+noagenda"]
        n = len(projects)
        l = self._test_lines_pri(num)
        m = []
        for i in range(0, num):
            m.append(todo.concat([l[i], projects[i % n]], " "))
        return m


    def _test_lines_context(self, num):
        projects = ["@foo", "@bar", "@bogus", "@github", "@school", "@work",
                "@inthemorning", "@agenda", "@noagenda"]
        n = len(projects)
        l = self._test_lines_pri(num)
        m = []
        for i in range(0, num):
            m.append(todo.concat([l[i], projects[i % n]], " "))
        return m


    def assertNumLines(self, exp, regexp=None):
        c = self.count_matches(regexp)
        self.assertEqual(exp, c)


    def assertIsInstance(self, obj, cls, msg=None):
        if sys.version_info >= (2, 7):
            super(BaseTest, self).assertIsInstance(obj, cls, msg)
        else:
            self.assertTrue(isinstance(obj, cls))


    def assertIsNotNone(self, expr, msg=None):
        if sys.version_info >= (2, 7):
            super(BaseTest, self).assertIsNotNone(expr, msg)
        else:
            if not expr:
                self.fail(msg)

    def force_print(self, message):
        sys.stderr.write(''.join([message, '\n']))
        sys.stderr.flush()
