# TODO.TXT-CLI-python test script
# Copyright (C) 2011  Sigmavirus24, Jeff Stein
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

import unittest
import base
import todo
from todotxt import TodoDotTxt
t = TodoDotTxt(todo.config)

class PrependTest(base.BaseTest):

    def test_prepend(self):
        t.addm_todo("\n".join(self._test_lines_no_pri(self.num)))

        for i in range(1, self.num + 1):
            t.prepend_todo([str(i), "testing", "prepend"])

        self.assertNumLines(self.num, "testing\sprepend\sTest\s\d+")


if __name__ == "__main__":
    unittest.main()
