#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PyCharm	
    ~~~~~~

    :copyright: (c) 2011 by ytjohn
    :license: BSD, see LICENSE for more details.
"""


import cmd
import string, sys
from optparse import OptionParser

class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'todo> '

    def do_add(self, arg):
        print "adding %s" % arg
    do_a = do_add

    def help_add(self):
        print         ['Adds todo ttem to +project @context #{yyyy-mm-dd}',
                       '+project, @context, #{yyyy-mm-dd} are optional']
    help_a = help_add

    def do_addm(self, arg):
        print "add multiples"

    def help_addm(self):
        print "adds multiple items"

    def do_del(self, arg):
        print "del item"
    do_d = do_del

    def help_del(self):
        print "del help"
    help_d = help_del

    def do_append(self, arg):
        print "append %s" % arg
    do_app = do_append

    def help_append(self):
        print "append"
    help_app = help_append

    def do_pri(self, arg):
        print "add priority"
    do_p = do_pri

    def help_pri(self):
        print "add priority"
    help_p = help_pri

    def do_depri(self, arg):
        print "remove priority from item"
    do_dp = do_depri

    def help_depri(self):
        print "remove priority from item"
    help_dp = help_depri

    def do_prepend(self, arg):
        print "prepend"
    do_pre = do_prepend

    def help_prepend(self, arg):
        print "prepend"
    help_pre = help_prepend

    def do_list(self, arg):
        print "list"
    do_ls = do_list

    def help_list(self):
        print "list"
    help_ls = help_list

    def do_listall(self, arg):
        print "listall %s" % arg
    do_lsa = do_listall

    def help_listall(self):
        print "listall"
    help_lsa = help_listall

    def do_listdate(self, arg):
        print "listdate %s" % arg
    do_lsd = do_listdate

    def help_listdate(self):
        print "listdate"
    help_lsd = help_listdate

    def do_listproj(self, arg):
        print "listproj %s" % arg
    do_lsp = do_listproj

    def help_listproj(self):
        print "listproj"
    help_lsp = help_listproj

    def do_listcon(self, arg):
        print "listcon %s" % arg
    do_lsc = do_listcon

    def help_listcon(self):
        print "listcon"
    help_lsc = help_listcon


    def do_quit(self, arg):
        """ quit """
        sys.exit(1)
    do_q = do_quit

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"
    help_q = help_quit

    def help_help(self):
        print "type help <topic>"

    def do_EOF(self, arg):
        sys.exit(1)







if __name__ == '__main__':
    if len(sys.argv) > 1:
        # CLI().prompt=''
        CLI().onecmd(' '.join(sys.argv[1:]))
    else:
        CLI().cmdloop()



