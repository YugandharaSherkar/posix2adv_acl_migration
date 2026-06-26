"""
applier.py
"""

import subprocess
import tempfile
from models import NFS4ACLEntry

class ACLApplier:
    def get_existing_acl(
        self,
        destination_path
    ):

        result = subprocess.run(
            [
                "nfs4_getfacl",
                str(destination_path)
            ],
            capture_output=True,
            text=True,
            check=True
        )

        acl_entries = []

        for line in result.stdout.splitlines():

            line = line.strip()

        #
        # Ignore comments
        #
            if not line:
                continue

            if line.startswith("#"):
                continue

        #
        # Expected format:
        #
        # A::OWNER@:rwatTNcCy
        #

            fields = line.split(":")

            if len(fields) != 4:
                continue

            acl_entries.append(

                NFS4ACLEntry(

                    ace_type=fields[0],

                    flags=fields[1],

                    principal=fields[2],

                    permissions=fields[3]

                )

            )

        return acl_entries
    
    def apply(
        self,
        destination_path,
        acl_entries
    ):

        #
        # Create temporary ACL file
        #
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False
        ) as acl_file:

            for ace in acl_entries:

                line = (
                    f"{ace.ace_type}:"
                    f"{ace.flags}:"
                    f"{ace.principal}:"
                    f"{ace.permissions}"
                )

                acl_file.write(line + "\n")

            acl_filename = acl_file.name

        #
        # Apply ACL
        #
        subprocess.run(
            [
                "nfs4_setfacl",
                "-S",
                acl_filename,
                str(destination_path)
            ],
            check=True
        )