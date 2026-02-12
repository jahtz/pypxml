# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path
from typing import Literal

import click
from pypxml import PageXML

from . import util


logger = logging.getLogger(__name__)


@click.command('reformat', short_help='Reformat PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-s', '--schema', 'schema',
    help='Set the PAGE-XML version.',
    type=click.Choice(['2017', '2019']),
    default='2019',
    show_default=True
)
def reformat(files: list[Path], schema: Literal['2017', '2019']):
    """
    This tool reformats multiple PAGE-XML files.
    
    This includes reformatting the file (e.g. pretty printing),
    and fixing the schema. Additional functions may follow.
    
    FILES: List of PageXML file paths to process.
    """
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        for fp in files:
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            pagexml.save(fp, schema=schema)            
            progressbar.advance(task)
        progressbar.update(task, status='Done')
