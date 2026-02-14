# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path

import click
from pypxml import PageXML, PageType

from .util import PROGRESSBAR, ClickCallback, ClickUtil


logger = logging.getLogger(__name__)


@click.command('regularise-codec', short_help='Regularise character encodings in PAGE-XML files.')
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
    '-i', '--index', 'index',
    help='Only consider TextEquiv elements with the specified index. If not set, regularise all indexes.',
    type=click.INT
)
@click.option(
    '-t', '--target', 'targets',
    help='Elements to regularise. Multiple elements can be specified. '
         'If no element is set, all elements are regularised.',
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=ClickCallback.pagetype(multiple=True),
    default=['TextLine', 'TextLine', 'Word', 'Glyph'],
    multiple=True
)
@click.option(
    '-e', '--element', 'elements',
    help='Select the text elements to regularise. PlainText is without formatting, Unicode is formatted. '
         'Multiple elements can be specified. If not element is set, both text elements are regularised.',
    type=click.Choice(['PlainText', 'Unicode']),
    callback=ClickCallback.pagetype(multiple=True),
    default=['PlainText', 'Unicode'],
    multiple=True
)
@click.option(
    '-r', '--rule', 'rules',
    help='Define substring replacement rules. Each rule is a pair of strings: "-r OLD NEW". '
         'Multiple rules can be specified. To replace with nothing or spaces, use quotation marks.',
    type=click.STRING,
    nargs=2,
    multiple=True,
    required=True
)
def regularise_codec(
    files: list[Path],
    output: Path | None = None,
    index: int | None = None,
    targets: list[PageType] = [PageType.TextRegion, PageType.TextLine, PageType.Word, PageType.Glyph],
    elements: list[PageType] = [PageType.PlainText, PageType.Unicode],
    rules: list[tuple[str, str]] = None
) -> None:
    """
    Apply character replacement rules to text elements in PAGE-XML files.
    
    Supports to limit replacement to specific target elements and index.
    
    FILES: List of PAGE-XML file paths to process.
    """
    ClickUtil.validate_directory(output)
    
    for r in rules:
        print(f'{r[0]} > {r[1]}')
    if not click.confirm('Do you want to continue?'):
        print('Aborted')
        return
    
    replacements: int = 0
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(files), status='')
        for fp in files:
            pb.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            page = PageXML.open(fp, raise_on_error=False)
            for e in page.find_all(pagetype=targets, depth=-1):
                for te in e.find_all(pagetype=PageType.TextEquiv, index=index):
                    for t in te.find_all(pagetype=elements):
                        for rule in rules:
                            replacements += t.text.count(rule[0])
                            t.text = t.text.replace(rule[0], rule[1])
            page.save(output.joinpath(fp.name) if output else fp)
            pb.advance(task)
        pb.update(task, status='Done')
    print(f'Replacements: {replacements}')
    
    
@click.command('regularise-regions', short_help='Regularise region types in PAGE-XML files.')
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
    '-r', '--rule', 'rules',
    help='Define region replacement rules. Each rule is a pair of strings: "-r OLD NEW", '
         'where OLD is the original region type and NEW is the new region type. Region types should be of type '
         '"PageType" or "PageType.subtype" (e.g., "TextRegion.paragraph", "ImageRegion"). '
         'If NEW is None, the region type specified with OLD is deleted. Only region PageTypes are allowed. '
         'Multiple rules can be specified.',
    type=click.STRING,
    callback=ClickCallback.pagetype_rules,
    nargs=2,
    multiple=True,
    required=True
)
def regularise_regions(
    files: list[Path],
    output: Path | None = None,
    rules: dict[str, tuple[PageType, str | None] | None] | None = None
) -> None:
    """
    Apply region replacement rules to PAGE-XML files.
        
    FILES: List of PAGE-XML file paths to process.
    """
    ClickUtil.validate_directory(output)
    
    for k, v in rules.items():
        v = 'None' if v is None else (f'{v[0]}' if v[1] is None else f'{v[0]} ({v[1]})')
        print(f'{k} > {v}')
    if not click.confirm('Do you want to continue?'):
        print('Aborted')
        return
    
    deleted: int = 0
    changed: int = 0
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(files), status='')
        for fp in files:
            pb.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            page = PageXML.open(fp, raise_on_error=False)
            for r in page.regions:
                old = f'{r.pagetype.value}.{r["type"]}' if 'type' in r else r.pagetype.value
                if old in rules.keys():
                    new = rules[old]
                    if new is None:
                        r.delete()
                        deleted += 1
                    else:
                        r.pagetype, r['type'] = new
                        changed += 1
            page.save(output.joinpath(fp.name) if output else fp)
            pb.advance(task)
        pb.update(task, status='Done')
        width = max(len(str(changed)), len(str(deleted)))
        print(f'Changed: {changed:>{width}}')
        print(f'Deleted: {deleted:>{width}}')
