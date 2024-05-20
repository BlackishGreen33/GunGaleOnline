"""Cmdline"""

import argparse
import sys

from gungaleonline.counter import count


def init_args() -> argparse.Namespace:
    """Init argument and parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--source", required=True, help="Source file used for count."
    )
    parser.add_argument(
        "-d", "--dest", required=True, help="Dest file used for count result"
    )
    return parser.parse_args(sys.argv[1:])


def main():
    """Execute"""
    args = init_args()
    count(args.source, args.dest)


if __name__ == "__main__":
    main()
