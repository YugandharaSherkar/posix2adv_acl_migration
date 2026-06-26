"""
duplicate.py

Merge translated NFSv4 ACLs with existing NFSv4 ACLs.
"""


class DuplicateChecker:

    @staticmethod
    def find_missing(
        translated_acl,
        existing_acl
    ):

        #
        # Store existing ACLs indexed by principal.
        #
        merged = {}

        #
        # Preserve all existing ACLs first.
        #
        for ace in existing_acl:

            merged[ace.principal] = ace

        #
        # Replace existing entries if the same
        # principal exists in translated ACL.
        #
        for ace in translated_acl:

            merged[ace.principal] = ace

        #
        # Return merged ACL list.
        #
        return list(merged.values())