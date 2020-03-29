#!/usr/bin/env python
import os
import sys

from config.environment import SETTINGS_MODULE


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
