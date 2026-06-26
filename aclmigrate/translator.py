
"""
translator.py

Translate POSIX ACLs into NFSv4 ACLs.
"""

from models import NFS4ACLEntry


class ACLTranslator:

    def __init__(self):

        self.permission_map = {

            "r": "r",

            "w": "watTNcCy",

            "x": "x"

        }

    def translate(self, posix_acl):

        translated_acl = []

        lines = posix_acl.splitlines()

        for line in lines:

            line = line.strip()

            #
            # Ignore comments
            #
            if not line:

                continue

            if line.startswith("#"):

                continue

            #
            # Ignore default ACLs (Version 1)
            #
            if line.startswith("default:"):

                continue

            #
            # Split ACL entry
            #
            fields = line.split(":")

            if len(fields) != 3:

                continue

            acl_type = fields[0]

            name = fields[1]

            permissions = fields[2]

            #
            # Translate principal
            #

            if acl_type == "user":

                principal = "OWNER@" if name == "" else name

            elif acl_type == "group":

                principal = "GROUP@" if name == "" else name

            elif acl_type == "other":

                principal = "EVERYONE@"

            elif acl_type == "mask":

                #
                # Ignore mask for Version 1
                #
                continue

            else:

                continue

            #
            # Translate permissions
            #

            nfs4_permissions = ""

            for permission in permissions:

                if permission == "-":
                    continue

                nfs4_permissions += self.permission_map.get(
                    permission,
                    ""
                )

            translated_acl.append(

                NFS4ACLEntry(

                    ace_type="A",

                    principal=principal,

                    permissions=nfs4_permissions

                )

            )

        return translated_acl