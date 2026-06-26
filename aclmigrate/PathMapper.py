"""
path mapper.py

maps path from nfs3 mount to nfs4 mount to verify if the path exists on nfs4 mount point
"""

from pathlib import Path

class PathMapper:

    @staticmethod
    def destination_path(
        source_file: Path,
        source_root: Path,
        destination_root: Path
    ) -> Path:

        relative = source_file.relative_to(source_root)

        return destination_root / relative