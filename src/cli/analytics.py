# SPDX-License-Identifier: Apache-2.0
from collections import Counter
import logging
from pathlib import Path
import string
from typing import Literal
import unicodedata

import click
from pypxml import PageXML, PageType, PageUtil

from .util import ClickCallback, ClickUtil, progressbar


logger: logging.Logger = logging.getLogger(__name__)


@click.command('get-codec', short_help='Extract character set from PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument('xmls', type=click.Path(), callback=ClickCallback.expand_glob, nargs=-1, required=True)
@click.option(
    '-o', '--output',
    help='Path to a CSV file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-s', '--source',
    help='Define the elements from which the codec is extracted.',
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=ClickCallback.parse_pagetype,
    default='TextLine',
    show_default=True
)
@click.option(
    '-i', '--index',
    help='Only consider TextEquiv elements with the specified index.',
    type=click.INT
)
@click.option(
    '--plaintext/--unicode',
    help='Use text from a Unicode or PlainText element',
    default=False,
    show_default=True
)
@click.option(
    '-w', '--whitespace',
    help='Include whitespace characters when analyzing codec. Only if `--source` is set to "TextRegion" or "TextLine"',
    is_flag=True
)
@click.option(
    '-f', '--frequency',
    help='Output character frequencies.',
    is_flag=True
)
@click.option(
    '-n', '--normalize',
    help='Normalize unicode before analysing codec.',
    type=click.Choice(['NFC', 'NFD', 'NFKC', 'NFKD'])
)
def get_codec(
    xmls: list[Path],
    output: Path | None = None,
    source: tuple[Literal[PageType.TextRegion, PageType.TextLine, PageType.Word, PageType.Glyph], None] = (PageType.TextLine, None),
    index: int | None = None,
    plaintext: bool = False,
    whitespace: bool = False,
    frequency: bool = False,
    normalize: Literal['NFC', 'NFD', 'NFKC', 'NFKD'] | None = None 
) -> None:
    """
    Analyze the text content of PAGE-XML files and extracts the set of used characters.
    
    It can optionally normalize unicode, include whitespace, and output character frequencies.
    Results are saved as a CSV file if `--output` is set, else printed to stdout.
    
    XMLS: List of PAGE-XML file paths to process. Supports glob expressions.
    """
    ClickUtil.validate_path(output, mkdir=True, extensions=['csv'])
    counter: Counter[str] = Counter()
    with progressbar as pb:
        task = pb.add_task('', total=len(xmls), status='')
        for xml in xmls:
            pb.update(task, status='/'.join(xml.parts[-4:]))
            pagexml: PageXML = PageXML.open(xml, raise_on_error=False)
            for element in pagexml.find_all(source[0], -1):
                text: str | None = PageUtil.find_text(
                    element, 
                    index, 
                    PageType.PlainText if plaintext else PageType.Unicode
                )
                if text is not None:
                    if normalize is not None:
                        text: str = unicodedata.normalize(normalize, text)
                    if not whitespace:
                        text: str = text.translate(str.maketrans('', '', string.whitespace))
                    counter.update(text)
            pb.advance(task)
        pb.update(task, status='Done')

    result: list[tuple[str, int]] = counter.most_common()
    if output:
        ClickUtil.write_csv(
            data=result if frequency else [r[0] for r in result],
            header=['char', 'freq'] if frequency else None,
            out=output,
        )
    else:
        ClickUtil.print_table(
            data=result if frequency else [r[0] for r in result],
            header=['char', 'freq'] if frequency else None
        )        


@click.command('get-regions', short_help='Extract region types from PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument('xmls', type=click.Path(), callback=ClickCallback.expand_glob, nargs=-1, required=True)
@click.option(
    '-o', '--output',
    help='Path to a CSV file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-l', '--level',
    help='Set the aggregation level for the output. "total" combines all files, "directory" aggregates by parent '
         'directory, and "file" lists results per individual file.',
    type=click.Choice(['total', 'directory', 'file']), 
    default='total', 
    show_default=True
)
@click.option(
    '-f', '--frequency',
    help='Output region frequencies.',
    is_flag=True
)
@click.option(
    '-s', '--subtypes',
    help='Include subtypes by printing them as "PageType.subtype" if available.',
    type=click.BOOL, 
    is_flag=True
)
def get_regions(
    xmls: list[Path], 
    output: Path | None = None, 
    level: Literal['total', 'directory', 'file'] = 'total', 
    frequency: bool = False, 
    subtypes: bool = False,
) -> None:
    """
    Analyse PAGE-XML files and list the region types found.
    
    Optionally include subtypes, outputs frequencies, and group numbers by file, directory, or total.
    Results are saved as a CSV file if `--output` is set, else printed to stdout.
    
    XMLS: List of PAGE-XML file paths to process. Supports glob expressions.
    """
    def format_count(count: int) -> str:
        return str(count) if frequency else ('x' if count > 0 else '')
    
    ClickUtil.validate_path(output, mkdir=True, extensions=['csv'])
    
    counter: dict[str, Counter] = {}
    with progressbar as pb:
        task = pb.add_task('', total=len(xmls), status='')
        for xml in xmls:
            pb.update(task, status='/'.join(xml.parts[-4:]))
            pagexml: PageXML = PageXML.open(xml, raise_on_error=False)
            counter[xml.as_posix()] = Counter([
                f'{r.pagetype.value}.{r["type"]}' if subtypes and 'type' in r else r.pagetype.value 
                for r in pagexml.regions
            ])
            pb.advance(task)
        pb.update(task, status='Done')
    
    if level == 'total':
        total: Counter[str] = Counter()
        for c in counter.values():
            total.update(c)
        if frequency:
            header: list[str] = ['type', 'frequency']
            data: list[tuple[str, int]] = total.most_common(None)
        else:
            header: list[str] = ['type']
            data: list[list[str]] = sorted([[r[0]] for r in total.most_common(None)], key=lambda r: r[0])
    else:
        if level == 'file':
            groups: dict[str, Counter[str]] = counter
        else:
            groups: dict[str, Counter] = {}
            for fp, c in counter.items():
                groups.setdefault(str(Path(fp).parent), Counter()).update(c)
        header: list[str] = [level.capitalize()] + sorted({rtype for counter in groups.values() for rtype in counter})
        data: list[list[str]] = [
            [name] + [format_count(c.get(rtype, 0)) for rtype in header[1:]]
            for name, c in groups.items()
        ]

    if output:        
        ClickUtil.write_csv(data, output, header=header, delimiter=';')
    else:
        ClickUtil.print_table(data, header)


@click.command('get-text', short_help='Extract text from a PAGE-XML file.')
@click.help_option('--help', hidden=True) 
@click.argument('xml', type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), required=True)
@click.option(
    '-o', '--output',
    help='Path to a TXT file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-i', '--index',
    help='Use only the text from TextEquiv elements at the given index.',
    type=click.INT
)
@click.option(
    '--plaintext/--unicode',
    help='Use text from a unicode or plaintext element',
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    '-s', '--separator',
    help='An optional separator string that can be printed between regions. For an empty line, pass an empty string ""',
    type=click.STRING
)
def get_text(
    xml: Path,
    output: Path | None = None,
    index: int | None = None,
    plaintext: bool = False,
    separator: str | None = None
) -> None:
    """
    Extract text from PAGE-XML files at the TextLine level.
    
    Results are saved as a TXT file if `--output` is set, else printed to stdout.
    Optionally, a separator between regions can be specified.
    
    XML: A PageXML file path to process.
    """
    ClickUtil.validate_path(output, mkdir=True, extensions=['txt'])
    pagexml: PageXML = PageXML.open(xml, raise_on_error=False)
    pagexml.apply_reading_order()
    
    result: list[str] = []
    with progressbar as pb:
        task = pb.add_task('', total=len(pagexml.regions), status='')
        for r in pagexml.regions:
            rtext: list[str] = []
            for tl in r.find_all(pagetype=PageType.TextLine):
                text: str | None = PageUtil.find_text(tl, index, PageType.PlainText if plaintext else PageType.Unicode)
                if text is not None:
                   rtext.append(text)
            result.append('\n'.join(rtext))
            pb.advance(task)
        pb.update(task, status='Done')
    
    sep: str = '\n' if separator is None else '\n' + separator + '\n'
    if output:
        output.write_text(sep.join(result), encoding="utf-8")
        print(f'Results written to {output.as_posix()}')
    else:
        print(sep.join(result))
