# SPDX-License-Identifier: Apache-2.0
import logging

try:
    import click
    from rich.logging import RichHandler
except ImportError as e:
    raise SystemExit('The pypxml CLI requires the optional dependencies. Install it via `pip install pypxml[cli]`')

from pypxml import __version__

from .analytics import get_codec, get_regions, get_text
from .format import reformat
from .regularize import regularize_codec, regularize_regions


logging.basicConfig(
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler(markup=True)]
)
logger = logging.getLogger('pypxml')


@click.group(epilog='Developed at Centre for Philology and Digitality (ZPD), University of Würzburg')
@click.help_option('--help')
@click.version_option(__version__, '--version', prog_name='pypxml')
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
    A python library for reading, writing, and modifying PageXML files.
    """
    logging.getLogger().setLevel(level)


main.add_command(get_codec)
main.add_command(get_regions)
main.add_command(get_text)
main.add_command(reformat)
main.add_command(regularize_codec)
main.add_command(regularize_regions)
