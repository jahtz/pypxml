# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path

import click
from pypxml import PageXML, PageType

from .util import ClickCallback, ClickUtil, progressbar


logger: logging.Logger = logging.getLogger(__name__)


@click.command('regularize-codec', short_help='Regularize character encodings in PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument('xmls', type=click.Path(), callback=ClickCallback.expand_glob, nargs=-1, required=True)
@click.option(
    '-o', '--output', 'output',
    help='Directory to save the modified PAGE-XML files. If omitted, input files will be overwritten.',
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-i', '--index', 'index',
    help='Only consider TextEquiv elements with the specified index. If not set, regularize all indexes.',
    type=click.INT
)
@click.option(
    '-t', '--target', 'targets',
    help='Elements to regularize. Multiple elements can be specified. '
         'If no element is set, all elements are regularized.',
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=ClickCallback.parse_pagetypes,
    default=['TextLine', 'TextLine', 'Word', 'Glyph'],
    multiple=True
)
@click.option(
    '-e', '--element', 'elements',
    help='Select the text elements to regularize. PlainText is without formatting, Unicode is formatted. '
         'Multiple elements can be specified. If not element is set, both text elements are regularized.',
    type=click.Choice(['PlainText', 'Unicode']),
    callback=ClickCallback.parse_pagetypes,
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
def regularize_codec(
    xmls: list[Path],
    rules: list[tuple[str, str]],
    output: Path | None = None,
    index: int | None = None,
    targets: list[tuple[PageType, None]] = [
        (PageType.TextRegion, None), (PageType.TextLine, None), (PageType.Word, None), (PageType.Glyph, None)
    ],
    elements: list[tuple[PageType, None]] = [(PageType.PlainText, None), (PageType.Unicode, None)],
) -> None:
    """
    Apply character replacement rules to text elements in PAGE-XML files.
    
    Supports to limit replacement to specific target elements and index.
    
    XMLS: List of PAGE-XML file paths to process. Supports glob expressions.
    """
    ClickUtil.validate_path(output, directory=True, mkdir=True)
    
    for r in rules:
        print(f'{r[0]} > {r[1]}')
    if not click.confirm('Do you want to continue?'):
        print('Aborted')
        return

    replacements: int = 0
    with progressbar as pb:
        task = pb.add_task('', total=len(xmls), status='')
        for xml in xmls:
            pb.update(task, status='/'.join(xml.parts[-4:]))
            pagexml: PageXML = PageXML.open(xml, raise_on_error=False)
            for element in pagexml.find_all([t[0] for t in targets], -1):
                args: dict[str, str] = {'index': str(index)} if index is not None else {}
                for textequiv in element.find_all(PageType.TextEquiv, -1, **args):
                    for textelement in textequiv.find_all([e[0] for e in elements]):
                        text: str | None = textelement.text
                        if text is None:
                            continue
                        for rule in rules:
                            replacements += text.count(rule[0])
                            textelement.text = text.replace(rule[0], rule[1])
            pagexml.save(output.joinpath(xml.name) if output else xml)
            pb.advance(task)
        pb.update(task, status='Done')
    print(f'Replacements: {replacements}')


@click.command('regularize-regions', short_help='Regularize region types in PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument('xmls', type=click.Path(), callback=ClickCallback.expand_glob, nargs=-1, required=True)
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
    callback=ClickCallback.parse_pagetype_rules,
    nargs=2,
    multiple=True,
    required=True
)
def regularize_regions(
    xmls: list[Path],
    rules: dict[str, tuple[PageType, str | None] | None],
    output: Path | None = None,
) -> None:
    """
    Apply region replacement rules to PAGE-XML files.
        
    FILES: List of PAGE-XML file paths to process. Supports glob expressions.
    """
    ClickUtil.validate_path(output, directory=True, mkdir=True)
    
    for k, v in rules.items():
        v: str = 'None' if v is None else (f'{v[0]}' if v[1] is None else f'{v[0]} ({v[1]})')
        print(f'{k} > {v}')
    if not click.confirm('Do you want to continue?'):
        print('Aborted')
        return
    
    deleted: int = 0
    changed: int = 0
    with progressbar as pb:
        task = pb.add_task('', total=len(xmls), status='')
        for xml in xmls:
            pb.update(task, status='/'.join(xml.parts[-4:]))
            pagexml: PageXML = PageXML.open(xml, raise_on_error=False)
            for r in pagexml.regions:
                old = f'{r.pagetype.value}.{r["type"]}' if 'type' in r else r.pagetype.value
                if old in rules:
                    new: tuple[PageType, str | None] | None = rules[old]
                    if new is None:
                        r.delete()
                        deleted += 1
                    else:
                        r.pagetype, r['type'] = new
                        changed += 1
            pagexml.save(xml)
            pb.advance(task)
        pb.update(task, status='Done')
        
        width = max(len(str(changed)), len(str(deleted)))
        print(f'Changed: {changed:>{width}}')
        print(f'Deleted: {deleted:>{width}}')
