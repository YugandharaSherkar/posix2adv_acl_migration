#!/usr/bin/env python3

import argparse

from validator import validate_paths
from parser import get_acl


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        required=True
    )

    parser.add_argument(
        "--destination",
        required=True
    )

    args = parser.parse_args()

    src, dst = validate_paths(
        args.source,
        args.destination
    )

    acl = get_acl(src)

    print("Source :", src)
    print("Destination :", dst)

    print("\nPOSIX ACL\n")

    for item in acl:
        print(item)


if __name__ == "__main__":
    main()