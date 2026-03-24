# SPDX-License-Identifier: Apache-2.0
import csv
import glob
import logging
from pathlib import Path
from typing import Any

import click
from pypxml import PageType
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn


columns: list[Any] = [
    BarColumn(bar_width=30),
    TextColumn('[progress.percentage]{task.percentage:>3.0f}%'),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    TextColumn('• {task.fields[status]}'),
]
progressbar = Progress(*columns)
logger: logging.Logger = logging.getLogger(__name__)


class ClickCallback:
    """ Collection of useful click callback methods """
    @staticmethod
    def expand_glob(ctx: click.Context, param: click.Parameter, patterns: list[str]) -> list[Path]:
        """ Expand glob expressions in path strings """
        paths: list[Path] = []
        for pattern in patterns:
            if glob.has_magic(pattern):
                for match in glob.iglob(pattern, recursive=True):
                    path: Path = Path(match)
                    if path.is_file():
                        paths.append(path.resolve())
            else:
                path: Path = Path(pattern)
                if path.is_file() and path.exists():
                    paths.append(path.resolve())
        return paths
    
    @staticmethod
    def __parse_pagetype(ctx: click.Context, param: click.Parameter, value: str) -> tuple[PageType, str | None]:
        parts: list[str] = value.split('.', 1)
        pt: str = parts[0]
        st: str | None = parts[1] if len(parts) == 2 else None
        if not pt or (st == '') or (st and '.' in st):
            raise click.BadParameter(f'Error parsing PageType "{value}"', ctx, param)
        if not PageType.validate(pt):
            raise click.BadParameter(f'Unknown PageType "{pt}"', ctx, param)
        return PageType[pt], st

    @staticmethod
    def parse_pagetype(
        ctx: click.Context, 
        param: click.Parameter, 
        value: str | None
    ) -> tuple[PageType, str | None] | PageType | None:
        """ Parse a string of type PageType or PageType.subtype to a PageType object """
        if value is None:
            return None
        return ClickCallback.__parse_pagetype(ctx, param, value)

    @staticmethod
    def parse_pagetypes(
        ctx: click.Context, 
        param: click.Parameter,
        value: tuple[str,...]
    ) -> list[tuple[PageType, str | None]] | list[PageType]:
        """ Parse a list of string of type PageType or PageType.subtype to PageType objects """
        return [ClickCallback.__parse_pagetype(ctx, param, p) for p in value]
    
    @staticmethod
    def parse_pagetype_rules(
        ctx: click.Context, 
        param: click.Parameter, 
        value: tuple[tuple[str, str],...]
    ) -> dict[str, tuple[PageType, str | None] | None]:
        """ Parse a list of rules (from, to) with PageTypes. """
        rules: dict[str, tuple[PageType, str | None] | None] = {}
        for old, new in value:
            ClickCallback.__parse_pagetype(ctx, param, old)  # just for validation
            if old in rules:
                raise click.BadParameter(f'"{old}" can not be declared multiple times as a source', ctx, param)
            rules[old] = None if new.lower() == 'none' else ClickCallback.__parse_pagetype(ctx, param, new)
        return rules


class ClickUtil:
    @staticmethod
    def validate_path(
        path: Path | None,
        directory: bool = False,
        mkdir: bool = False,
        extensions: list[str] | None = None
    ) -> None:
        """
        Helper method for validating paths

        Args:
            path: Path object to validate. If it is None, nothing happens.
            file: Check if `path` is a directory, else it has to be a file. Defaults to False.
            mkdir: Create the directory if a directory `path` is passed (and `file` is set to False), else create the 
                file's parents. Defaults to False.
            extensions: If `path` is a file, check if it has one of the passed file extensions. Defaults to None.

        Raises:
            click.BadOptionUsage: The path does not meet the requirements.
        """
        if path is None:
            return
        is_dir: bool = path.is_dir()
        if is_dir != directory:
            click.BadOptionUsage('', f'Passed path is not a {"file" if is_dir else "directory"}')
        if mkdir:
            parent: Path = path if is_dir else path.parent
            parent.mkdir(parents=True, exist_ok=True)
        if not is_dir and extensions is not None:
            extensions: list[str] = [e.lower().replace('.', '') for e in extensions]
            ext: str = path.name.split('.')[-1].lower()
            if ext not in extensions:
                raise click.BadOptionUsage('', f'Allowed file extensions: {extensions}, got \'{ext}\'')
    
    @staticmethod
    def write_csv(
        data: list[Any], 
        out: Path, 
        header: list[str] | None = None, 
        delimiter: str = ',',
        encoding: str = 'utf-8'
    ) -> None:
        """ Write data to a CSV file """
        if header and len(header) != max(len(d) for d in data):
            raise ValueError(f'Header length {len(header)} does not match data length {max(len(d) for d in data)}!')
        
        with open(out, 'w', encoding='utf-8') as f:
            writer= csv.writer(f, delimiter=delimiter)
            if header:
                writer.writerow(header)
            writer.writerows(data)
        logger.info(f'Results written to {out.as_posix()}')
        
    @staticmethod
    def print_table(data: list[Any], header: list[str] | None = None) -> None:
        """ Pretty print a table to stdout """
        if not data:
            logger.error('No data to print')
            return
        
        str_header: list[str] | None = [str(h) for h in header] if header else None
        num_cols: int = len(str_header) if str_header else max(len(row) for row in data)
        col_widths: list[int] = [
            max(len(str(header[col])) if header else 0, *(len(str(row[col])) for row in data)) 
            for col in range(num_cols)
        ]
        
        if str_header:
            print(' '.join([f'{str(x):<{col_widths[i]}}' for i, x in enumerate(str_header)]))
            
        for row in data:
            print(
                ' '.join([
                    f'{str(x):>{col_widths[i]}}' 
                    if isinstance(x, (int, float)) 
                    else f'{str(x):<{col_widths[i]}}' 
                    for i, x in enumerate(row)
                ])
            )
