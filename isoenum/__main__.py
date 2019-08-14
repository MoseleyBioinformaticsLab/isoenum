#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docopt

from . import cli
from . import __version__


def _remove_new_line_from_usage_patterns(docstr):
    """Removes new line from usage patterns in docopt CLI description.
    :param str docstr: docopt CLI description.
    :return: Reformatted docstring ready for docopt consumption.
    :rtype: :py:class:`str`
    """
    lines = []

    usage = False
    for line in docstr.split("\n"):
        if line.startswith("Usage:"):
            usage = True
        elif line.startswith("Options:"):
            lines.append("")
            usage = False

        if usage:
            if not line:
                continue
            else:
                lines.append(line)
        else:
            lines.append(line)

    return "\n".join(lines)


def main():
    docstr = _remove_new_line_from_usage_patterns(docstr=cli.__doc__)
    cli.cli(docopt.docopt(doc=docstr, version=__version__))


if __name__ == '__main__':
    main()
