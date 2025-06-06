"""
# {{ cookiecutter.repository_name }}
"""
import mjaf
mjaf.logging.set_handlers(
    logger_name="{{ cookiecutter.project_name }}",
)

import argparse

from rich_argparse import RawDescriptionRichHelpFormatter, ArgumentDefaultsRichHelpFormatter
from rich.markdown import Markdown

from {{ cookiecutter.project_name }}._utils.constants import VERSION

import logging
log = logging.getLogger(__name__)


def parse_args():
    class CustomFormatter(RawDescriptionRichHelpFormatter, ArgumentDefaultsRichHelpFormatter):
        """This just combines the two formatters using multiple inheritance."""
        pass

    parser = argparse.ArgumentParser(
        description=Markdown(__doc__, style="argparse.text"),
        formatter_class=CustomFormatter,
    )
    

    parser.add_argument(
        '--log-level',
        action='store',
        choices=[
            'debug',
            'info',
            'warning',
            'error',
            'critical',
        ],
    )

    parser.add_argument(
        "--version", action="version", version=f"[argparse.prog]%(prog)s[/] version [i]{VERSION}[/]"
    )

    args = parser.parse_args()
    
    return args

    
def main():
    args = parse_args()


    mjaf.logging.set_handlers(
        logger_name="{{ cookiecutter.project_name }}",
        level=args.log_level.upper(),
    )



if __name__ == '__main__':
    main()
