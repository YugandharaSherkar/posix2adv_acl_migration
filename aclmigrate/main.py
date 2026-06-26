#!/usr/bin/env python3

"""
main.py

Main entry point for ACL migration.
"""

import argparse
from pathlib import Path

from PathMapper import PathMapper
from parser import ACLParser
from translator import ACLTranslator
from aclmigrate.duplicateold import DuplicateChecker
from applier import ACLApplier
from logger import logger


def parse_arguments():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Migrate POSIX ACLs to NFSv4 ACLs."
    )

    parser.add_argument(
        "--source-root",
        required=True,
        help="Source NFSv3 root directory"
    )

    parser.add_argument(
        "--destination-root",
        required=True,
        help="Destination NFSv4 root directory"
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    source_root = Path(args.source_root)
    destination_root = Path(args.destination_root)

    logger.info("Starting ACL migration")
    logger.info("Source      : %s", source_root)
    logger.info("Destination : %s", destination_root)

    acl_parser = ACLParser()
    translator = ACLTranslator()
    applier = ACLApplier()

    for source_path in source_root.rglob("*"):

        logger.info("Processing %s", source_path)

        try:

            destination_path = PathMapper.destination_path(
                source_path,
                source_root,
                destination_root
            )
            print(destination_path)
            if not destination_path.exists():
                logger.error(
                    "Destination not found: %s",
                    destination_path
                )
                continue

            #
            # Read POSIX ACL
            #
            posix_acl = acl_parser.get_acl(source_path)

            #
            # Translate ACL
            #
            translated_acl = translator.translate(posix_acl)

            #
            # Read existing NFSv4 ACL
            #
            existing_acl = applier.get_existing_acl(
                destination_path
            )

            #
            # Merge ACLs
            #
            merged_acl = DuplicateChecker.find_missing(
                translated_acl,
                existing_acl
            )

            #
            # Apply merged ACL
            #
            applier.apply(
                destination_path,
                merged_acl
            )

            logger.info(
                "Successfully migrated %s",
                source_path
            )

        except Exception as error:

            logger.exception(
                "Failed processing %s : %s",
                source_path,
                error
            )

            continue

    logger.info("Migration completed.")


if __name__ == "__main__":
    main()