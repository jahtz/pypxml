# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path
from typing import Literal

import click
from pypxml import PageXML

from .util import PROGRESSBAR, ClickUtil


logger = logging.getLogger(__name__)


@click.command('prettify', short_help='Prettify formatting of PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Directory to save the modified PAGE-XML files. If omitted, input files will be overwritten.',
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-s', '--schema', 'schema',
    help='Set the PAGE-XML schema version.',
    type=click.Choice(['2017', '2019']),
    default='2019',
    show_default=True
)
def prettify(
    files: list[Path],
    output: Path,
    schema: Literal['2017', '2019'] = '2019'
) -> None:
    """
    Prettify the formatting of PAGE-XML files.
    
    This includes reformatting the file (i.e., prettifying),
    and fixing the schema. Additional functionality may follow.
    
    FILES: List of PAGE-XML file paths to process.
    """
    ClickUtil.validate_directory(output)
    
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(files), status='')
        for fp in files:
            pb.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            PageXML.open(fp, raise_on_error=False).save(output.joinpath(fp.name) if output else fp, schema=schema)
            pb.advance(task)
        pb.update(task, status='Done')
