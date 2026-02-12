# SPDX-License-Identifier: Apache-2.0
from collections import Counter
import logging
from pathlib import Path
import string
from typing import Literal
import unicodedata

import click
from pypxml import PageXML, PageType, PageUtil

from . import util


logger = logging.getLogger(__name__)


@click.command('get-codec', short_help='Extract the character set from PAGE-XML files.')
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
    help='PAGE-XML level from which to extract the codec.',
    type=click.Choice(['TextRegion', 'TextLine', 'Word', 'Glyph']),
    callback=util.pagetype_callback,
    default='TextLine',
    show_default=True
)
@click.option(
    '-i', '--index', 'index',
    help='Only consider TextEquiv elements with the specified index.',
    type=click.INT
)
@click.option(
    '-w', '--ignore-whitespaces', 'ignore_whitespaces',
    help='Ignore all whitespace characters when analyzing codec.',
    is_flag=True
)
@click.option(
    '-f', '--frequencies', 'frequencies',
    help='Output character frequencies.',
    is_flag=True
)
@click.option(
    '-n', '--normalize', 'normalize',
    help='Normalize unicode before analyzing codec.',
    type=click.Choice(['NFC', 'NFD', 'NFKC', 'NFKD'])
)
def get_codec(
    files: list[Path], 
    output: Path | None = None, 
    level: PageType = PageType.TextLine,
    index: int | None = None,
    ignore_whitespaces: bool = False,
    frequencies: bool = False,
    normalize: Literal['NFC', 'NFD', 'NFKC', 'NFKD'] | None = None,
    **kwargs
) -> None:
    """
    Analyze the text content of PAGE-XML files and extracts the set of characters used.
    
    It can optionally normalize unicode, remove whitespace, and output character frequencies.
    Results are printed to the console or saved as a CSV file.
    
    FILES: List of PAGE-XML file paths to process.
    """
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
    
    results = Counter()
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        for fp in files:
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            for element in pagexml.find_all(pagetype=level[0], depth=-1):
                if text := PageUtil.get_text(element, index=index):
                    if normalize:
                        text = unicodedata.normalize(normalize, text)
                    if ignore_whitespaces:
                        text = text.translate(str.maketrans('', '', string.whitespace))
                    results.update(text)
            progressbar.advance(task)
        progressbar.update(task, status='Done')
    
    codec_dict = {k: v for k, v in results.most_common(None)}
    data = sorted([[k, v] for k, v in codec_dict.items()], reverse=True, key=lambda x: x[1])
    if output:
        if not frequencies:
            data = [[x[0]] for x in data]
        util.csv_write(data, output, header=['character', 'frequency'] if frequencies else ['character'], delimiter=';')
    else:
        util.print_table(
            data=data if frequencies else [[x[0]] for x in data], 
            header=['char', 'freq'] if frequencies else None
        )


@click.command('get-regions', short_help='List all regions in PageXML files.')
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
    help='Set the aggregation level for the output. `total` combines all files, `directory` aggregates by parent '
         'directory, and `file` lists results per individual file.',
    type=click.Choice(['total', 'directory', 'file']), 
    default='total', 
    show_default=True
)
@click.option(
    '-f', '--frequencies', 'frequencies',
    help='Output the frequency (count) of each region type.',
    type=click.BOOL, is_flag=True
)
@click.option(
    '-t', '--types', 'types',
    help='Include subtypes by printing them as `PageType.type` if available.',
    type=click.BOOL, is_flag=True
)
def get_regions(
    files: list[Path], 
    output: Path | None = None, 
    level: Literal['total', 'directory', 'file'] = '', 
    frequencies: bool = False, 
    types: bool = False,
    **kwargs
) -> None:
    """
    Analyze PAGE-XML files and lists the region types found.
    
    Optionally includes subtypes, outputs frequencies, and group by file, directory, or globally.
    
    FILES: List of PAGE-XML file paths to process.
    """
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        
    results = {}
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        for fp in files:
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            found_regions = [
                f'{region.pagetype.value}.{region["type"]}' if types and 'type' in region else region.pagetype.value
                for region in pagexml.regions
            ]
            results[str(fp)] = Counter(found_regions)
            progressbar.advance(task)
        progressbar.update(task, status='Done')
        
    format_count = lambda c: c if frequencies else ('x' if c > 0 else '')
    if level in ['file', 'directory']:
        groups = results if level == 'file' else {}
        if level == 'directory':
            for fp, count in results.items():
                groups.setdefault(str(Path(fp).parent), Counter()).update(count)
        header = [level] + sorted({r for c in results.values() for r in c})
        data = [
            [name] + [format_count(counter.get(k, 0)) for k in header[1:]]
            for name, counter in groups.items()
        ]
    else:
        header = ['type', 'frequency'] if frequencies else ['type']
        total = Counter()
        for count in results.values():
            total.update(count)
        data = [[r, total[r]] if frequencies else [r] 
                for r in sorted(total, key=lambda x: -total[x] if frequencies else x)]

    if output:        
        util.csv_write(data, output, header=header, delimiter=';')
    else:
        util.print_table(data, header)


@click.command('get-text', short_help='Extract text from PageXML files.')
@click.help_option('--help', hidden=True)
@click.argument(
    'files',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    nargs=-1,
    required=True
)
@click.option(
    '-o', '--output', 'output',
    help='Output destination. If a directory is specified, a separate text file is created for each PageXML file, '
         'ignoring the page separator. If a file is specified, the text from all files is concatenated into that file. '
         'If omitted, the text is printed to stdout.',
    type=click.Path(exists=False, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path)
)
@click.option(
    '-i', '--index', 'index',
    help='Use only the text from TextEquiv elements at the given index.',
    type=click.INT
)
@click.option(
    '-r', '--region-separator', 'region_separator',
    help='Separator string inserted between regions. Use "" for an empty line, "\\n" for two empty lines, etc.', 
    type=click.STRING
)
@click.option(
    '-p', '--page-separator', 'page_separator',
    help='Separator string inserted between pages when outputting to a single file or stdout. '
         'Ignored when outputting multiple files. Use "" for an empty line, "\\n" for two empty lines, etc.',
    type=click.STRING
)
def get_text(
    files: list[Path], 
    output: Path | None = None, 
    index: int | None = None,
    region_separator: str | None = None, 
    page_separator: str | None = None,
    **kwargs
) -> None:
    """
    Extract text from PAGE-XML files at the TextLine level.
    
    Outputs to individual text files, a single file, or prints to stdout, 
    with optional separators between regions and pages.
    
    FILES: List of PageXML file paths to process.
    """
    region_sep = None if region_separator is None else region_separator.replace('\\n', '\n')
    page_sep = None if page_separator is None else page_separator.replace('\\n', '\n')
    
    # multi: output is a directory and a text file for each input file is generated
    # single: output is a file and all text will be written to this file
    # print: no output was passed and text is printed to console
    if output and output.is_dir():
        output.mkdir(parents=True, exist_ok=True)
        mode = 'multi'
    elif output and output.is_file():
        output.parent.mkdir(parents=True, exist_ok=True)
        mode = 'single'
    else:
        mode = 'print'
        
    results = []
    with util.PROGRESSBAR as progressbar:
        task = progressbar.add_task('Processing', total=len(files), status='')
        for i, fp in enumerate(files, start=1):
            progressbar.update(task, status=Path('/', *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.open(fp, raise_on_error=False)
            ptext = False
            for j, region in enumerate(pagexml.regions, start=1):
                rtext = False
                for textline in region.find_all(pagetype=PageType.TextLine):
                    if (text := PageUtil.get_text(textline, index=index)) is not None and text.strip():
                        ptext = rtext = True
                        results.append(text)
                if rtext and region_sep is not None and j != len(pagexml.regions):  # split regions by the defined separator
                    results.append(region_sep)
                if not rtext and j > 0 and results and results[-1] == region_sep:  # remove the separator if the previous one did not contain text as well
                    results.pop()
            if ptext and mode != 'multi' and page_sep is not None and i != len(files):  # split pages by the defined separator
                results.append(page_sep)
            if mode == 'multi':  # write the content of the current file
                output.joinpath(fp.name.split('.')[0] + '.txt').write_text('\n'.join(results), encoding='utf-8')
                results.clear()
            progressbar.advance(task)
        progressbar.update(task, status='Done')
    
    if mode == 'print':  # print all text to stdout
        for line in results:
            print(line)
    elif mode == 'single':  # print all text to a single file
        output.write_text('\n'.join(results), encoding='utf-8')
