"""Automated tests module."""

import structlog

# The tests can be executed by standing in the project's root directory
# and running the following command in a terminal:
# python -m unittest -v

structlog.configure_once(logger_factory=structlog.ReturnLoggerFactory())
