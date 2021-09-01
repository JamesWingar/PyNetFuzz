#!/usr/bin/env python3
"""
CLI run script
"""
# Python library imports
from arguments import parse_args
# Package imports
from run import run


def main():
    """ Commandline run method"""
    args = parse_args()
    run(args)

if __name__ == "__main__":
    main()
