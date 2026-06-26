"""
parser.py

Reads POSIX ACL using getfacl.
"""

import subprocess


class ACLParser:

    def get_acl(self, path):

        result = subprocess.run(
            [
                "getfacl",
                "--absolute-names",
                str(path)
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout