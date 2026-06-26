"""
models.py

Data models for ACL migration.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PosixACLEntry:
    acl_type: str
    name: str
    permissions: str


@dataclass(frozen=True)
class NFS4ACLEntry:
    ace_type: str
    principal: str
    permissions: str
    flags: str = ""


@dataclass
class FileMigration:

    source_path: Path

    destination_path: Path

    owner: str = ""

    group: str = ""

    posix_acl: list[PosixACLEntry] = field(default_factory=list)

    translated_acl: list[NFS4ACLEntry] = field(default_factory=list)

    existing_acl: list[NFS4ACLEntry] = field(default_factory=list)

    missing_acl: list[NFS4ACLEntry] = field(default_factory=list)

    status: str = "PENDING"

    error: str | None = None