#!/usr/bin/env python3
"""
CLI run script
"""
# Package imports
from pynetfuzz.arguments import parse_args
from pynetfuzz.run import run


def main():
    """ Commandline run method"""
    args = parse_args()
    run(args)

if __name__ == "__main__":
    main()
