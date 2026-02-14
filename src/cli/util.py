# SPDX-License-Identifier: Apache-2.0
import csv
from pathlib import Path
from typing import Callable

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


class ClickUtil:
    @staticmethod
    def validate_file(
        target: str | Path | None, 
        extension: list[str] | str | None = None,
    ) -> None:
        """
        Validates a file path and creates the target directory.
        Args:
            target: The file target to validate.
            extension: A whitelisted extension or a list of extensions without leading dots. Defaults to None.
        """
        if target is None:
            return
        if isinstance(target, str):
            target = Path(target)
        if isinstance(extension, str):
            extension = [extension]
        ext = target.name.split('.', maxsplit=1)[1].lower()
        if extension is not None and ext not in extension:
            raise click.BadOptionUsage('', f'Allowed file extensions: {extension}, got \'{ext}\'')
        target.parent.mkdir(parents=True, exist_ok=True)
        
    @staticmethod
    def validate_directory(
        target: str | Path | None
    ) -> None:
        """
        Validates a diretory and creates it if it does not exist.
        Args:
            target: The directory target to validate.
        """
        if target is None:
            return
        if isinstance(target, str):
            target = Path(target)
        target.mkdir(parents=True, exist_ok=True)

    @staticmethod
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
        print(f'Results written to {output.as_posix()}')

    @staticmethod
    def print_table(data: list[list], header: list[str] | None = None) -> None:
        """
        Pretty print a table to stdout.
        Args:
            data: The data to be printed.
            header: The header of the data. If None, no header will be printed. Defaults to None. Defaults to None.
        """
        if not data:
            print('No data to output')
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
            print(' '.join([f'{str(x):>{col_widths[i]}}' if isinstance(x, (int, float)) 
                            else f'{str(x):<{col_widths[i]}}' 
                            for i, x in enumerate(row)]))


class ClickCallback:
    @staticmethod
    def __parse_pagetype(
        ctx: click.Context, 
        param: click.Parameter, 
        value: str
    ) -> tuple[PageType, str | None]:
        parts = value.split('.', 1)
        pt = parts[0]
        st = parts[1] if len(parts) == 2 else None
        if not pt or (st == '') or (st and '.' in st):
            raise click.BadParameter(f'Error parsing PageType "{value}"', ctx, param)
        if not PageType.is_valid(pt):
            raise click.BadParameter(f'Unknown PageType "{pt}"', ctx, param)
        return PageType[pt], st
    
    @staticmethod
    def pagetype(
        subtype: bool = False, 
        multiple: bool = False
    ) -> Callable[
        [click.Context, click.Parameter, tuple[str, ...] | str | None],
        list[tuple[PageType, str | None]] | list[PageType] | tuple[PageType, str | None] | PageType | None
    ]:
        def _callback(
            ctx: click.Context, 
            param: click.Parameter, 
            value: tuple[str,...] | str | None
        ) -> list[tuple[PageType, str | None]] | list[PageType] | tuple[PageType, str | None] | PageType | None:
            if value is None:
                return None
            if isinstance(value, tuple):
                if not multiple:
                    raise click.BadParameter(f'Expected a string, got a tuple: "{value}"', ctx, param)
                return [
                    ClickCallback.__parse_pagetype(ctx, param, p) if subtype else 
                    ClickCallback.__parse_pagetype(ctx, param, p)[0] for p in value
                ]
            elif isinstance(value, str):
                if multiple:
                    raise click.BadParameter(f'Expected a tuple, got a string: "{value}"', ctx, param)
                res = ClickCallback.__parse_pagetype(ctx, param, value)
                return res if subtype else res[0]
            raise click.BadParameter(f'Unknown type of input: "{type(value)}"', ctx, param)
        return _callback
    
    @staticmethod
    def pagetype_rules(
        ctx: click.Context, 
        param: click.Parameter,
        value: tuple[tuple[str, str],...]
    ) -> dict[str, tuple[PageType, str | None]]:
        rules: dict[str, tuple[PageType, str | None]] = {}
        for old, new in value:
            ClickCallback.__parse_pagetype(ctx, param, old)  # just for validation
            if old in rules:
                raise click.BadParameter(
                    f'"{old}" can not be declared multiple times as a source', ctx, param
                )
            rules[old] = None if new.lower() == 'none' else ClickCallback.__parse_pagetype(ctx, param, new)
        return rules
