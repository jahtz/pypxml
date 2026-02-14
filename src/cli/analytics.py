# SPDX-License-Identifier: Apache-2.0
from collections import Counter
import logging
from pathlib import Path
import string
from typing import Literal
import unicodedata

import click
from pypxml import PageXML, PageType, PageUtil

from .util import PROGRESSBAR, ClickUtil, ClickCallback


logger = logging.getLogger(__name__)


@click.command('get-codec', short_help='Extract character set from PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Path to a CSV file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-s', '--source', 'source',
    help='Define the elements from which the codec is extracted.',
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=ClickCallback.pagetype(),
    default='TextLine',
    show_default=True
)
@click.option(
    '-i', '--index', 'index',
    help='Only consider TextEquiv elements with the specified index.',
    type=click.INT
)
@click.option(
    '--plaintext/--unicode', 'plaintext',
    help='Use text from a Unicode or PlainText element',
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    '-w', '--whitespace', 'whitespace',
    help='Include whitespace characters when analysing codec. Only if `--source` is set to "TextRegion" or "TextLine"',
    is_flag=True
)
@click.option(
    '-f', '--frequency', 'frequency',
    help='Output character frequencies.',
    is_flag=True
)
@click.option(
    '-n', '--normalize', 'normalize',
    help='Normalize unicode before analysing codec.',
    type=click.Choice(['NFC', 'NFD', 'NFKC', 'NFKD'])
)
def get_codec(
    files: list[Path],
    output: Path | None = None,
    source: Literal[PageType.TextRegion, PageType.TextLine, PageType.Word, PageType.Glyph] = PageType.TextLine,
    index: int | None = None,
    plaintext: bool = False,
    whitespace: bool = False,
    frequency: bool = False,
    normalize: Literal['NFC', 'NFD', 'NFKC', 'NFKD'] | None = None 
) -> None:
    """
    Analyse the text content of PAGE-XML files and extracts the set of characters used.
    
    It can optionally normalize unicode, include whitespace, and output character frequencies.
    Results are saved as a CSV file if `--output` is set, else printed to stdout.
    
    FILES: List of PAGE-XML file paths to process.
    """
    ClickUtil.validate_file(output, 'csv')
    
    result: Counter = Counter()
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(files), status='')
        for fp in files:
            pb.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            page = PageXML.open(fp, raise_on_error=False)
            for e in page.find_all(pagetype=source, depth=-1):
                text = PageUtil.get_text(e, index=index, source=PageType.PlainText if plaintext else PageType.Unicode)
                if text is not None:
                    if normalize is not None:
                        text = unicodedata.normalize(normalize, text)
                    if not whitespace:
                        text = text.translate(str.maketrans('', '', string.whitespace))
                    result.update(text)
            pb.advance(task)
        pb.update(task, status='Done')
    
    result = sorted(result.most_common(None), reverse=True, key=lambda r: r[1])
    if output is None:
        ClickUtil.print_table(
            data=result if frequency else [[r[0] for r in result]],
            header=['char', 'freq'] if frequency else None
        )
    else:
        ClickUtil.write_csv(
            data=result if frequency else [[r[0] for r in result]],
            header=['char', 'freq'] if frequency else None,
            output=output,
            delimiter=';'
        )


@click.command('get-regions', short_help='Extract region types from PAGE-XML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Path to a CSV file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-l', '--level', 'level',
    help='Set the aggregation level for the output. "total" combines all files, "directory" aggregates by parent '
         'directory, and "file" lists results per individual file.',
    type=click.Choice(['total', 'directory', 'file']), 
    default='total', 
    show_default=True
)
@click.option(
    '-f', '--frequency', 'frequency',
    help='Output region frequencies.',
    is_flag=True
)
@click.option(
    '-s', '--subtypes', 'subtypes',
    help='Include subtypes by printing them as "PageType.subtype" if available.',
    type=click.BOOL, 
    is_flag=True
)
def get_regions(
    files: list[Path], 
    output: Path | None = None, 
    level: Literal['total', 'directory', 'file'] = 'total', 
    frequency: bool = False, 
    subtypes: bool = False,
) -> None:
    """
    Analyse PAGE-XML files and list the region types found.
    
    Optionally include subtypes, outputs frequencies, and group numbers by file, directory, or total.
    Results are saved as a CSV file if `--output` is set, else printed to stdout.
    
    FILES: List of PAGE-XML file paths to process.
    """
    ClickUtil.validate_file(output, 'csv')
    
    result: dict[str, Counter] = {}
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(files), status='')
        for fp in files:
            pb.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            page = PageXML.open(fp, raise_on_error=False)
            result[fp.as_posix()] = Counter([
                f'{r.pagetype.value}.{r["type"]}' if subtypes and 'type' in r else r.pagetype.value 
                for r in page.regions
            ])
            pb.advance(task)
        pb.update(task, status='Done')
        
    format_count = lambda count: count if frequency else ('x' if count > 0 else '')
    
    if level == 'total':
        total = Counter()
        for counter in result.values():
            total.update(counter)
        if frequency:
            header = ['type', 'frequency']
            data = sorted(total.most_common(None), reverse=True, key=lambda r: r[1])
        else:
            header = ['type']
            data = sorted([[r[0]] for r in total.most_common(None)], key=lambda r: r[0])
    else:
        if level == 'file':
            groups = result
        else:
            groups: dict[str, Counter] = {}
            for fp, counter in result.items():
                groups.setdefault(str(Path(fp).parent), Counter()).update(counter)
        header = [level.capitalize()] + sorted({rtype for counter in groups.values() for rtype in counter})
        data = [
            [name] + [format_count(counter.get(rtype, 0)) for rtype in header[1:]]
            for name, counter in groups.items()
        ]

    if output:        
        ClickUtil.write_csv(data, output, header=header, delimiter=';')
    else:
        ClickUtil.print_table(data, header)


@click.command('get-text', short_help='Extract text from a PAGE-XML file.')
@click.help_option('--help', hidden=True) 
@click.argument(
    'file',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Path to a TXT file to save the results. If omitted, results are printed to stdout.',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    '-i', '--index', 'index',
    help='Use only the text from TextEquiv elements at the given index.',
    type=click.INT
)
@click.option(
    '--plaintext/--unicode', 'plaintext',
    help='Use text from a unicode or plaintext element',
    is_flag=True,
    default=False,
    show_default=True
)
@click.option(
    '-s', '--separator', 'separator',
    help='An optional separator string that can be printed between regions. For an empty line, pass an empty string ""',
    type=click.STRING
)
def get_text(
    file: Path,
    output: Path | None = None,
    index: int | None = None,
    plaintext: bool = False,
    separator: str | None = None
) -> None:
    """
    Extract text from PAGE-XML files at the TextLine level.
    
    Results are saved as a TXT file if `--output` is set, else printed to stdout.
    Optionally, a separator between regions can be specified.
    
    FILE: A PageXML file path to process.
    """
    ClickUtil.validate_file(output, 'txt')
    
    page = PageXML.open(file, raise_on_error=False)
    page.reading_order_apply()
    
    result: list[str] = []
    with PROGRESSBAR as pb:
        task = pb.add_task('Processing', total=len(page.regions), status='')
        for r in page.regions:
            rtext = []
            for tl in r.find_all(pagetype=PageType.TextLine):
                text = PageUtil.get_text(tl, index=index, source=PageType.PlainText if plaintext else PageType.Unicode)
                if text is not None:
                   rtext.append(text)
            result.append('\n'.join(rtext))
            pb.advance(task)
        pb.update(task, status='Done')
    
    if output:
        output.write_text(f'{"\n" if separator is None else f"\n{separator}\n"}'.join(result), encoding='utf-8')
        print(f'Results written to {output.as_posix()}')
    else:
        print(f'{"\n" if separator is None else f"\n{separator}\n"}'.join(result))
