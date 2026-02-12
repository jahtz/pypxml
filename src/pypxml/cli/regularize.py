# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path

import click
from pypxml import PageXML, PageType

from . import util


logger = logging.getLogger(__name__)


@click.command('regularize-codec', short_help='Regularize character encodings in PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Directory to save the modified PageXML files. If omitted, input files will be overwritten.',
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-i', '--index', 'index',
    help='Use only TextEquiv elements with the specified index. Defaults to all TextEquiv elements if not set.',
    type=click.INT
)
@click.option(
    '-l', '--level', 'level', 
    help='PageXML element level to process.', 
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=util.pagetype_callback,
    default='TextLine', 
    show_default=True
)
@click.option(
    '--plaintext/--unicode', 'plaintext',
    help='Select the text element to use.Choose from PlainText (without formatting) or Unicode (formatted).',
    type=click.BOOL, 
    show_default=True
)
@click.option(
    '-r', '--rule', 'rules',
    help='Define substring replacement rules. Each rule is a pair of strings: `--rule SOURCE TARGET`. '
         'Multiple rules can be specified by repeating the option.',
    type=click.STRING, 
    nargs=2, 
    multiple=True, 
    required=True
)
def regularize_codec(
    files: list[Path], 
    output: Path | None = None, 
    index: int | None = None, 
    level: PageType = PageType.TextLine, 
    rules: list[tuple[str, str]] = None, 
    plaintext: bool = False
) -> None:
    """
    Apply character replacement rules to text elements in PAGE-XML files.
    
    Supports selecting PlainText or Unicode elements and limiting replacements to 
    specific element levels.
    
    FILES: List of PageXML file paths to process.
    """
    if output:
        output.mkdir(parents=True, exist_ok=True)
        
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        replacements = 0
        for fp in files:
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            for element in pagexml.find_all(pagetype=level, depth=-1):
                for textequiv in element.find_all(pagetype=PageType.TextEquiv, index=index):
                    for t in textequiv.find_all(pagetype=PageType.PlainText if plaintext else PageType.Unicode):
                        for rule in rules:
                            if count := t.text.count(rule[0]):
                                replacements += count
                                t.text = t.text.replace(rule[0], rule[1])
            pagexml.save(output.joinpath(fp.name) if output else fp)
            progressbar.advance(task)
        progressbar.update(task, status='Done')
    print(f'Replacements: {replacements}')


@click.command('regularize-regions', short_help='Regularize region types in PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Directory to save the modified PageXML files. If omitted, input files will be overwritten.',
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-r', '--rule', 'rules',
    help='Define rules for region regularization. Format: --rule SOURCE TARGET '
         'where SOURCE is the original region type (e.g., TextRegion.paragraph, ImageRegion), '
         'and TARGET is the new region type. Use an `None` TARGET to delete the region. '
         'Only region PageTypes are allowed. Multiple rules can be specified by repeating this option.',
    type=click.STRING,
    callback=util.region_rule_callback,
    nargs=2, 
    multiple=True, 
    required=True
)
def regularize_regions(
    files: list[Path], 
    output: Path | None = None,
    rules: dict[str, tuple[PageType, str | None] | None] = None
) -> None:
    """
    This tool processes PageXML files and updates or removes regions based on specified rules.
    
    Regions are matched by their PageType and optional subtype. 
    Regions matching the source specification are either updated to a new type 
    or deleted if target is set to 'None'.
    
    FILES: List of PageXML file paths to process.
    """
    if output:
        output.mkdir(parents=True, exist_ok=True)
        
    deleted = 0
    changed = 0
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        for fp in files:
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            for region in pagexml.regions:
                key = f'{region.pagetype.value}.{region["type"]}' if 'type' in region else region.pagetype.value
                if key in rules:
                    value = rules[key]
                    if value is None:
                        region.parent.delete(region)
                        deleted += 1
                    else:
                        region.pagetype = value[0]
                        region['type'] = value[1]
                        changed += 1
            pagexml.save(output.joinpath(fp.name) if output else fp)
            progressbar.advance(task)
        progressbar.update(task, status='Done')
    width = max(len(str(changed)), len(str(deleted)))
    print(f'Changed: {changed:>{width}}\nDeleted: {deleted:>{width}}')
