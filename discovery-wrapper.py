#! /usr/bin/env python3
"""
This is a Bootstrap script for wrapper.py, in order to retain compatibility with earlier LibreNMS setups
"""


import os
import sys
import logging
from argparse import ArgumentParser

import LibreNMS
import LibreNMS.wrapper as wrapper

WRAPPER_TYPE = "discovery"
DEFAULT_WORKERS = 1

"""
    Take the amount of threads we want to run in parallel from the commandline
    if None are given or the argument was garbage, fall back to default
"""
usage = f"usage: %(prog)s [options] <amount_of_workers> (Default: {DEFAULT_WORKERS}(Do not set too high, or you will get an OOM)"

description = "Spawn multiple discovery.php processes in parallel."
parser = ArgumentParser(usage=usage, description=description)
parser.add_argument(dest="amount_of_workers", default=DEFAULT_WORKERS)
parser.add_argument(
    "-d",
    "--debug",
    dest="debug",
    action="store_true",
    default=False,
    help="Enable debug output. WARNING: Leaving this enabled will consume a lot of disk space.",
)
args = parser.parse_args()

config = LibreNMS.get_config_data(os.path.dirname(os.path.realpath(__file__)))
if not config:
    logger = logging.getLogger(__name__)
    logger.critical(f"Could not run {WRAPPER_TYPE} wrapper. Missing config")
    sys.exit(1)
log_dir = config["log_dir"]
log_file = os.path.join(log_dir, f"{WRAPPER_TYPE}_wrapper.log")
logger = LibreNMS.logger_get_logger(log_file, debug=args.debug)

try:
    amount_of_workers = int(args.amount_of_workers)
except (IndexError, ValueError):
    amount_of_workers = DEFAULT_WORKERS
    logger.warning(
        f"Bogus number of workers given. Using default number ({amount_of_workers}) of workers."
    )


wrapper.wrapper(
    WRAPPER_TYPE,
    amount_of_workers=amount_of_workers,
    config=config,
    log_dir=log_dir,
    _debug=args.debug,
)
