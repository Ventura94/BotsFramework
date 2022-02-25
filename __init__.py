#!/usr/bin/env python
"""MT5BotFramework command-line utility for administrative tasks."""

import sys


def main():
    """Run administrative tasks."""
    try:
        from MT5BotFramework.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import MT5BotFramework. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
