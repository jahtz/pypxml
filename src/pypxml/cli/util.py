# SPDX-License-Identifier: Apache-2.0
import csv
from pathlib import Path

import click
from pypxml import PageType
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn


PROGRESSBAR = Progress(
    TextColumn('[progress.description]{task.description}'),
    BarColumn(),
    TextColumn('[progress.percentage]{task.percentage:>3.0f}%'),
    MofNCompleteColumn(),
    TextColumn('•'),
    TimeElapsedColumn(),
    TextColumn('•'),
    TimeRemainingColumn(),
    TextColumn('• {task.fields[status]}')
)


def pagetype_callback(ctx, param, value: str | None) -> tuple[PageType, str | None] | None:
    """
    Parses a string representation of a PageType and an optional subtype.
    Args:
        value: A string represtation of a PageType and an optional subtype. 
            Example: 'ImageRegion' or 'TextRegion.paragraph'
    Returns:
        A tuple containing the PageType and optional subtype. Example: (ImageRegion, None) or (TextRegion, paragraph)
    """
    if value is None:
        return None
    
    parts = value.split('.', 1)
    pt = parts[0]
    st = parts[1] if len(parts) == 2 else None
    
    if not pt or (st == ""):
        raise click.BadOptionUsage(param, f'Error parsing PageType {value}')
    if not PageType.is_valid(pt):
        raise click.BadOptionUsage(param, f'Unknown PageType {pt}')
    return PageType[pt], st


def region_rule_callback(ctx, param, value: tuple[str]) -> dict[str, tuple[PageType, str | None]]:
    """ 
    Parses a list or tuple with rule strings into a dictionary (keys are strings of format pagetype.subtype or pagetype 
    and represent the source) and values are tuples of type (PageType, subtype). 
    All PageTypes have to be valid and regions.
    """
    def parse_type(t: str) -> tuple[PageType, str | None]:
        if t.count('.') > 1:
            raise click.BadOptionUsage(
                param, 
                f'Invalid format: region can only be specified in format RegionType or RegionType.subtype, got `{t}`'
            )
        if '.' in t:
            pagetype, subtype = t.split('.')
        else:
            pagetype, subtype = t, None
        if not PageType.is_valid(pagetype):
            raise click.BadOptionUsage(param, f'Invalid PageType: `{pagetype}`')
        pagetype = PageType[pagetype]
        if not pagetype.is_region:
            raise click.BadOptionUsage(param, f'Invalid Region: `{pagetype}`')
        return pagetype, subtype
    
    result = {}
    for rule in value:
        source, target = rule
        parse_type(source)  # validate source
        if source in result:
            raise click.BadOptionUsage(param, f'Invalid format: `{source}` cannot declared multiple times as a source')
        target = parse_type(target) if target.lower() != 'none' else None
        result[source] = target
    return result


def write_csv(data: list[list], output: Path, header: list[str] | None = None, delimiter: str = ',') -> None:
    """
    Write a list of lists to a CSV file.
    Args:
        data: The data to be written.
        output: The output file path.
        header: The header of the data. If None, no header will be written. Defaults to None.
        delimiter: The delimiter to be used. Defaults to ",".
    """
    if header and len(header) != len(data[0]):
        raise ValueError(f'Header length {len(header)} does not match data length {len(data[0])}!')
    
    with open(output, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=delimiter)
        if header:
            writer.writerow(header)
        writer.writerows(data)
        
    
def print_table(data: list[list], header: list[str] | None = None) -> None:
    """
    Pretty print a table to stdout.
    Args:
        data: The data to be printed.
        header: The header of the data. If None, no header will be printed. Defaults to None. Defaults to None.
    """
    if not data and not header:
        return
    
    str_header = [str(h) for h in header] if header else None
    num_cols = len(str_header) if str_header else max(len(row) for row in data)

    col_widths = []
    for col in range(num_cols):
        max_width = 0
        if str_header:
            max_width = len(str_header[col])
        for row in data:
            max_width = max(max_width, len(str(row[col])))
        col_widths.append(max_width)
        
    col_widths = [max(len(str(header[col])) if header else 0,
                      *(len(str(row[col])) for row in data))
                  for col in range(num_cols)]
    if str_header:
        print(' '.join([f'{str(x):<{col_widths[i]}}' for i, x in enumerate(str_header)]))
    for row in data:
        print(' '.join([f'{str(x):>{col_widths[i]}}' if isinstance(x, (int, float)) else f'{str(x):<{col_widths[i]}}' 
                        for i, x in enumerate(row)]))
