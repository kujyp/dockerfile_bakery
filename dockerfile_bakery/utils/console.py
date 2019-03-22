from __future__ import print_function

import os
import time
import traceback


class AnsiEscape:
    """
    Black        0;30     Dark Gray     1;30
    Red          0;31     Light Red     1;31
    Green        0;32     Light Green   1;32
    Brown/Orange 0;33     Yellow        1;33
    Blue         0;34     Light Blue    1;34
    Purple       0;35     Light Purple  1;35
    Cyan         0;36     Light Cyan    1;36
    Light Gray   0;37     White         1;37
    """
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    LIGHTGRAY = '\033[0;37m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NOCOLOR = '\033[0m'


def _get_prefix():
    trcb = traceback.extract_stack()
    assert len(trcb) > 2
    currtime = time.strftime("%H:%M:%S")
    filename = os.path.basename(trcb[-3][0])
    assert filename != os.path.basename(__file__)
    # funcname = trcb[-3][2]
    prefix = "{}/{}".format(currtime, filename)
    return "{0:{1}}".format(prefix, 35)


def _print_with_color(color, msg):
    print("{}{}{}".format(color, msg, AnsiEscape.NOCOLOR))


def notice(msg):
    _print_with_color(AnsiEscape.YELLOW, "{} {}".format(_get_prefix(), msg))


def info(msg):
    print("{} {}".format(_get_prefix(), msg))


def detail(msg):
    _print_with_color(AnsiEscape.LIGHTGRAY, "{} {}".format(_get_prefix(), msg))


def warn(msg):
    _print_with_color(AnsiEscape.WARNING, "{} {}".format(_get_prefix(), msg))


def error(msg):
    _print_with_color(AnsiEscape.RED, "{} {}".format(_get_prefix(), msg))
