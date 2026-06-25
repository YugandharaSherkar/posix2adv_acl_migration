#!/usr/bin/env python3

"""
validator.py

Validation routines for ACL migration.
"""

from pathlib import Path


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_paths(source, destination):
    """
    Validate source and destination paths.

    Returns:
        tuple(Path, Path)
    """

    src = Path(source)
    dst = Path(destination)

    if not src.exists():
        raise ValidationError(
            f"Source does not exist: {src}"
        )

    if not dst.exists():
        raise ValidationError(
            f"Destination does not exist: {dst}"
        )

    if src.is_file() != dst.is_file():
        raise ValidationError(
            "Source and destination types differ."
        )

    if src.is_dir() != dst.is_dir():
        raise ValidationError(
            "Directory/File mismatch."
        )

    return src, dst