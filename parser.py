#!/usr/bin/env python3

"""
parser.py

Reads POSIX ACL using getfacl.
"""

import subprocess
import re


class ACLParserError(Exception):
    pass


def get_acl(path):

    try:

        output = subprocess.check_output(
            [
                "getfacl",
                "--absolute-names",
                str(path)
            ],
            text=True
        )

    except subprocess.CalledProcessError as exc:
        raise ACLParserError(str(exc))

    acl = []

    regex = re.compile(
        r'^(user|group|mask|other|default):([^:]*):([rwx-]+)$'
    )

    for line in output.splitlines():

        if line.startswith("#"):
            continue

        if line.strip() == "":
            continue

        m = regex.match(line)

        if not m:
            continue

        acl.append(
            {
                "type": m.group(1),
                "name": m.group(2),
                "perm": m.group(3)
            }
        )

    return acl