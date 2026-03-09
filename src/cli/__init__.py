# SPDX-License-Identifier: Apache-2.0
from importlib.metadata import version
import logging

try:
    import click
    from rich.logging import RichHandler
except ImportError:
    raise SystemExit('The pypxml CLI requires optional dependencies. Install it via `$ uv tool install pypxml[cli]`')

from .analytics import get_codec, get_regions, get_text
from .regularize import regularize_codec, regularize_regions


logging.basicConfig(
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(markup=True)]
)
logger: logging.Logger = logging.getLogger('pypxml')


@click.group(epilog='Developed at Centre for Philology and Digitality (ZPD), University of Würzburg')
@click.help_option('--help')
@click.version_option(version('pypxml'), '--version', prog_name='pypxml')
@click.pass_context
@click.option(
     '--logging', 'level',
     help='Set logging level.', 
     type=click.Choice(['ERROR', 'WARNING', 'INFO']),
     default='ERROR',
     show_default=True
)
def main(ctx, level, **kwargs) -> None:
    """
    A modern, powerful,and extremly fast Python library for reading, writing, and modifying PAGE-XML files
    """
    logging.getLogger().setLevel(level)


# analytics
main.add_command(get_codec)
main.add_command(get_regions)
main.add_command(get_text)

# regularise
main.add_command(regularize_codec)
main.add_command(regularize_regions)
