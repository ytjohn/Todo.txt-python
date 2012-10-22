#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    PyCharm	
    ~~~~~~

    :copyright: (c) 2011 by ytjohn
    :license: BSD, see LICENSE for more details.
"""

# for help details:
# TODO: http://docs.python.org/library/textwrap.html#textwrap.wrap

version = "usecmd"
revision = "$Id$"

import os
import cmd
import  sys
from textwrap import TextWrapper
from todotxt import TodoDotTxt


concat = lambda str_list, sep='': sep.join([str(i) for i in str_list])
_path = lambda p: os.path.abspath(os.path.expanduser(p))
_pathc = lambda plist: _path(concat(plist))

try:
    from string import uppercase
except ImportError:
    # Python 3 again
    from string import ascii_uppercase as uppercase

priorities = uppercase[:24]

term_colors = {
    "black": "\033[0;30m", "red": "\033[0;31m",
    "green": "\033[0;32m", "brown": "\033[0;33m",
    "blue": "\033[0;34m", "purple": "\033[0;35m",
    "cyan": "\033[0;36m", "light grey": "\033[0;37m",
    "dark grey": "\033[1;30m", "light red": "\033[1;31m",
    "light green": "\033[1;32m", "yellow": "\033[1;33m",
    "light blue": "\033[1;34m", "light purple": "\033[1;35m",
    "light cyan": "\033[1;36m", "white": "\033[1;37m",
    "default": "\033[0m", "reverse": "\033[7m",
    "bold": "\033[1m",
    }

todo_dir = _path("~/.todo")
config = {
    "TODO_DIR": todo_dir,
    "TODOTXT_DEFAULT_ACTION": "list",
    "TODOTXT_CFG_FILE": _pathc([todo_dir, "/config"]),
    "TODO_FILE": _pathc([todo_dir, "/todo.txt"]),
    "DONE_FILE": _pathc([todo_dir, "/done.txt"]),
    "TMP_FILE": "",
    "REPORT_FILE": "",
    "USE_GIT": False,
    "PLAIN": False,
    "NO_PRI": False,
    "PRE_DATE": False,
    "INVERT": False,
    "HIDE_PROJ": False,
    "HIDE_CONT": False,
    "HIDE_DATE": False,
    "LEGACY": False,
    "ACTIONS": None,
    "TERM_COLORS": term_colors,
    "PRIORITIES": priorities,
    "VERSION": version,
    "REVISION": revision
}

todo = TodoDotTxt(config)

class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'todo> '
        self.concat = lambda str_list, sep='': sep.join([str(i) for i in
                                                         str_list])

    def do_add(self, arg):
        todo.add_todo(arg)
    do_a = do_add

    def help_add(self):
        usage = todo.add_todo.__usage__
        print usage

    help_a = help_add

    def do_addm(self, arg):
        todo.addm_todo(arg)

    def help_addm(self):
        usage = todo.addm_todo.__usage__
        print usage

    def do_del(self, arg):
        todo.delete_todo(arg)
    do_d = do_del

    def help_del(self):
        usage = todo.delete_todo.__usage__
        print usage
    help_d = help_del

    def do_append(self, arg):
        todo.append_todo(arg)
    do_app = do_append

    def help_append(self):
        usage = todo.append_todo.__usage__
        print usage
    help_app = help_append

    def do_pri(self, arg):
        todo.prioritize_todo(arg)
    do_p = do_pri

    def help_pri(self):
        usage = todo.prioritize_todo.__usage__
        print usage
    help_p = help_pri

    def do_depri(self, arg):
        todo.de_prioritize_todo(arg)
    do_dp = do_depri

    def help_depri(self):
        usage = todo.de_prioritize_todo.__usage__
        print usage

    help_dp = help_depri

    def do_prepend(self, arg):
       todo.prepend_todo(arg)
    do_pre = do_prepend

    def help_prepend(self):
        command = todo.prepend_todo.__command__
        lines = todo.prepend_todo.__usage__
        usage = self.concat(lines, '\n').expandtabs(3)
        wrapper = TextWrapper(subsequent_indent="\t\t")
        help = "%s\t%s" % (command, usage)
        print wrapper.fill(help)

        # print "%s\t\t%s" % (command, usage)
    #        for use in usage:
    #            print use

    help_pre = help_prepend

    def do_list(self, arg):
        todo.list_todo(arg)
    do_ls = do_list

    def help_list(self):
        usage = todo.list_todo.__usage__
        print usage
    help_ls = help_list

    def do_listall(self, arg):
        todo.list_all(arg)
    do_lsa = do_listall

    def help_listall(self):
        usage = todo.list_all.__usage__
        print usage
    help_lsa = help_listall

    def do_listdate(self, arg):
        todo.list_date(arg)
    do_lsd = do_listdate

    def help_listdate(self):
        usage = todo.list_date.__usage__
        print usage
    help_lsd = help_listdate

    def do_listproj(self, arg):
        todo.list_project(arg)
    do_lsp = do_listproj

    def help_listproj(self):
        usage = todo.list_project.__usage__
        print usage
    help_lsp = help_listproj

    def do_listcon(self, arg):
        todo.list_context(arg)
    do_lsc = do_listcon

    def help_listcon(self):
        usage = todo.list_context.__usage__
        print usage
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



# call main loop

if __name__ == '__main__':

    todo.config["TODO_PY"] = sys.argv[0]
    opts = todo.opt_setup()
    valid, args = opts.parse_args()
    todo.get_config(valid.config, valid.todo_dir)

    if not len(args) > 0:
        CLI().onecmd(config["TODOTXT_DEFAULT_ACTION"])

    if len(sys.argv) > 1:
        CLI().onecmd(' '.join(sys.argv[1:]))
    else:
        CLI().cmdloop()


##    opts = DoToDo.opt_setup()
#        opts = OptionParser("Usage: %prog [options] action [arg(s)]")
#        opts.add_option("-c", "--config", dest="config", default="",
#            type="string",
#            nargs=1,
#            help=self.concat(["Supply your own configuration file,",
#                              "must be an absolute path"])
#        )