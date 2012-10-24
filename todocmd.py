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
from optparse import OptionParser
import textwrap
from todotxt import TodoDotTxt
import logging

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
    "DEBUG": False, # set to True to enable debug logging
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
    "REVISION": revision,
    "SHELL": False,
    "SILENT": False,
}

for p in priorities:
    config["PRI_{0}".format(p)] = "default"
del(p, todo_dir)

todo = TodoDotTxt(config)


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'todo> '
        self.concat = lambda str_list, sep='': sep.join([str(i) for i in
                                                         str_list])

    def _format_usage(self, command, usage):
        """
        format a command and usage for outputting help
        """
        # assume commands are no larger than 20
        # initial indent is one space
        max_command = 20
        initial_indent = 1
        # todo: find a way to get each line from @usage on its own line
        initial = ''.ljust(initial_indent)
        indent = ''.ljust(max_command + initial_indent + 1)
        help = "%s%s" % (command.ljust(max_command), usage)
        output = textwrap.fill(help, initial_indent=initial,
                               subsequent_indent=indent)
#        print lines
#        output = self.concat(lines, 'c\nd')
        return output

    def _get_usage(self, arg):
        func = getattr(todo, arg)
        command = func.__command__
        lines = func.__usage__
        usage = self.concat(lines, "")
        return self._format_usage(command, usage)

    def do_add(self, arg):
        (status, output) = todo.add_todo(arg)
        if status == 'usage':
            self.help_add()
            return 1
        elif status == 'success':
            print output


    do_a = do_add

    def help_add(self, doprint=1):
        usage = self._get_usage('add_todo')
        if doprint:
            print usage
        return usage

    help_a = help_add

    def do_addm(self, arg):
        todo.addm_todo(arg)
        # since addm prints from within the function, no output needed

    def help_addm(self, doprint=1):
        usage = self._get_usage('addm_todo')
        if doprint:
            print usage
        return usage

    def do_do(self, arg):
        (status, output) = todo.do_todo(arg)
        if status == "usage":
            self.help_do()
        elif status == "success":
            for out in output:
                print out

    def help_do(self, doprint=1):
        usage = self._get_usage('do_todo')
        if doprint:
            print usage
        return usage

    def do_del(self, arg):
        (status, output) = todo.delete_todo(arg)
        if status == "usage":
            self.help_del()
        elif status == "success":
            for out in output:
                print out
        else:
            print "unknown %s" % status
            for out in output:
                print out

    do_rm = do_del

    def help_del(self, doprint=1):
        usage = self._get_usage('delete_todo')
        if doprint:
            print usage
        return usage
    help_rm = help_del

    def do_append(self, arg):
        (status, output) = todo.append_todo(arg)
        if status == "usage":
            self.help_append()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_app = do_append

    def help_append(self, doprint=1):
        usage = self._get_usage('append_todo')
        if doprint:
            print usage
        return usage
    help_app = help_append

    def do_pri(self, arg):
        (status, output) = todo.prioritize_todo(arg)
        if status == "usage":
            self.help_pri()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_p = do_pri

    def help_pri(self, doprint=1):
        usage = self._get_usage('prioritize_todo')
        if doprint:
            print usage
        return usage
    help_p = help_pri

    def do_depri(self, arg):
        todo.de_prioritize_todo(arg)
    do_dp = do_depri

    def help_depri(self, doprint=1):
        usage = self._get_usage('de_prioritize_todo')
        if doprint:
            print usage
        return usage

    help_dp = help_depri

    def do_prepend(self, arg):
        (status, output) = todo.prepend_todo(arg)
        if status == "usage":
            self.help_prepend()
        elif status == "success":
            print output
        #            for out in output:
        #                print out
        else:
            print "unknown %s" % status
            print output
        #            for out in output:
        #                print out
    do_pre = do_prepend

    def help_prepend(self, doprint=1):
        usage = self._get_usage('prepend_todo')
        if doprint:
            print usage
        return usage

        # print "%s\t\t%s" % (command, usage)
    #        for use in usage:
    #            print use

    help_pre = help_prepend

    def do_list(self, arg):
#        def list_todo(self, args=None, plain=False, no_priority=False):
        (status, output) = todo.list_todo(arg, todo.config["PLAIN"],
            todo.config["NO_PRI"])
        if status == "usage":
            self.help_list()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_ls = do_list
    do_l = do_list

    def help_list(self, doprint=1):
        usage = self._get_usage('list_todo')
        if doprint:
            print usage
        return usage

    help_ls = help_list
    help_l = help_list

    def do_listall(self, arg):
        (status, output) = todo.list_all()
        if status == "usage":
            self.help_listall()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_lsa = do_listall

    def help_listall(self, doprint=1):
        usage = self._get_usage('list_all')
        if doprint:
            print usage
        return usage
    help_lsa = help_listall

    def do_listdate(self, arg):
        (status, output) = todo.list_date()
        if status == "usage":
            self.help_listdate()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_lsd = do_listdate

    def help_listdate(self, doprint=1):
        usage = self._get_usage('list_date')
        if doprint:
            print usage
        return usage
    help_lsd = help_listdate

    def do_listproj(self, arg):
        (status, output) = todo.list_project()
        if status == "usage":
            self.help_listproj()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_lsp = do_listproj

    def help_listproj(self, doprint=1):
        usage = self._get_usage('list_project')
        if doprint:
            print usage
        return usage
    help_lsp = help_listproj

    def do_listcon(self, arg):
        (status, output) = todo.list_context()
        if status == "usage":
            self.help_listcon()
        elif status == "success":
            print output
        else:
            print "unknown %s" % status
            print output
    do_lsc = do_listcon

    def help_listcon(self, doprint=1):
        usage = self._get_usage('list_context')
        if doprint:
            print usage
        return usage
    help_lsc = help_listcon

    def do_quit(self, arg):
        """ quit """
        sys.exit(0)
    do_q = do_quit

    def help_quit(self, doprint=1):
        command = 'quit|q'
        usage = "terminates the application"
        help = self._format_usage(command, usage)
        if doprint:
            print help
        return help
    help_q = help_quit

    def help_help(self, doprint=1):
        command = 'help'
        usage = "type help <topic>"
        help = self._format_usage(command, usage)
        if doprint:
            print help
        return help

    def do_EOF(self):
        sys.exit(1)

    def do_debug(self, arg):
        """ Show or change debug status"""
        #TODO: desite efforts, doesn't change debug level of todotxt.py

        switch = str(arg).upper()
        if switch == "ON":
            enableDebug()
        elif switch == "OFF":
            disableDebug()

        if todo.config["DEBUG"]:
            print "DEBUG is ON."
        else:
            print "DEBUG is OFF."


    # create a helpall command
    def do_helpall(self):
        names = self.get_names()
        cmds_doc = []
        cmds_undoc = []
        help = {}
        usage = []
        for name in names:
            if name[:5] == 'help_':
                help[name[5:]] = 1
        names.sort()
        # There can be duplicates if routines overridden
        prevname = ''
        for name in names:
            if name[:3] == 'do_':
                if name == prevname:
                    continue
                prevname = name
                cmd = name[3:]
                if cmd in help:
                    # self.do_help(cmd)
                    # self.stdout.write("cmd: %s, " % cmd)
                    func = getattr(self, 'help_' + cmd)
                    thisUsage = func(0)
                    # print thisUsage
                    if thisUsage not in usage:
                        usage.append(thisUsage)
                    cmds_doc.append(cmd)
                    del help[cmd]
                elif getattr(self, name).__doc__:
                    cmds_doc.append(cmd)
                else:
                    cmds_undoc.append(cmd)
        self.stdout.write("%s\n" % str(self.doc_leader))

        usage.sort()
        for use in usage:
            print use
    do_ha = do_helpall

    def help_helpall(self, doprint=1):
        command = 'helpall|ha'
        usage = "lists help for all commands"
        help = self._format_usage(command, usage)
        if doprint:
            print help
        return help
    help_ha = help_helpall


def enableDebug(option=None, opt_str=None, val=None, parser=None):
    #todo: this doesn't actually change it for todocmd.py
    todo.enableDebug()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('todocmd.enableDebug: debug enabled')

def disableDebug(option=None, opt_str=None, val=None, parser=None):
    #todo: this doesn't actually change it for todocmd.py
    todo.disableDebug()
    logging.basicConfig(level=logging.INFO)
    logging.info('todocmd.disableDebug: debug disabled')

### command line options
def opt_setup():
    opts = OptionParser("Usage: %prog [options] action [arg(s)]")
    opts.add_option("-c", "--config", dest="config", default="",
                    type="string",
                    nargs=1,
                    help='Supply your own configuration file, '
                         'must be an absolute path',
                    )
    opts.add_option("-d", "--dir", dest="todo_dir", default="",
                    type="string",
                    nargs=1,
                    help="Directory you wish {prog} to use.".format(
                        prog=todo.config["TODO_PY"])
                    )
    opts.add_option("-p", "--plain-mode", action="callback",
                    callback=todo.toggle_opt,
                    help="Toggle coloring of items"
                    )
    opts.add_option("-P", "--no-priority", action="callback",
                    #todo: make -P work
                    callback=todo.toggle_opt,
                    help="Toggle display of priority labels"
                    )
    opts.add_option("-t", "--prepend-date", action="callback",
                    #todo: make -t work
                    callback=todo.toggle_opt,
                    help="Toggle whether the date is prepended to new items."
                    )
    opts.add_option("-s", "--shell", action="callback",
                    callback=todo.toggle_opt,
                    help="Use interactive shell"
                    )
    opts.add_option("-q", "--quiet", "--silent", action="callback",
                    callback=todo.toggle_opt,
                    help="If using interactive shell, disables prompt. Good "
                         "for scripting"
                    )
    opts.add_option("-V", "--version", action="callback",
                    callback=todo.version,
                    nargs=0,
                    help="Print version, license, and credits"
                    )
    opts.add_option("-D", "--debug", action="callback",
                    callback=enableDebug,
                    nargs=0,
                    help="Enables debug messages"
                    )
    opts.add_option("-i", "--invert-colors", action="callback",
                    callback=todo.toggle_opt,
                    help="Toggle coloring the text of items or background of"
                         " items."
                    )
    opts.add_option("-l", "--legacy", action="callback",
                    callback=todo.toggle_opt,
                    help="Toggle organization of items in the old manner."
                    )
    opts.add_option("-+", action="callback", callback=todo.toggle_opt,
                    help="Toggle display of +projects in-line with items."
                    )
    opts.add_option("-@", action="callback", callback=todo.toggle_opt,
                    help="Toggle display of @contexts in-line with items."
                    )
    opts.add_option("-#", action="callback", callback=todo.toggle_opt,
                    help="Toggle display of #{dates} in-line with items."
                    )
    return opts

# call main loop

if __name__ == '__main__':

    todo.config["TODO_PY"] = sys.argv[0]
    opts = opt_setup()
    valid, args = opts.parse_args()
    todo.get_config(valid.config, valid.todo_dir)

    # todo: get args working

    c = CLI()
    cmd = None

    if not len(args) > 0 and not todo.config["SILENT"]:
        cmd = config["TODOTXT_DEFAULT_ACTION"]
    else:
        cmd = ' '.join(args)

    if todo.config['SHELL']:
        if todo.config['SILENT']:
            c.prompt = ''
            c.cmdloop()
        else:
            c.onecmd(cmd)
            c.cmdloop(intro='todo interactive shell')

    else:
        c.onecmd(cmd)



#    print "test"
#    if len(sys.argv) > 1:
##        CLI().onecmd(' '.join(sys.argv[1:]))
#        CLI().onecmd(' '.join(args))
#    else:
#        CLI().cmdloop()


##    opts = DoToDo.opt_setup()
#        opts = OptionParser("Usage: %prog [options] action [arg(s)]")
#        opts.add_option("-c", "--config", dest="config", default="",
#            type="string",
#            nargs=1,
#            help=self.concat(["Supply your own configuration file,",
#                              "must be an absolute path"])
#        )
