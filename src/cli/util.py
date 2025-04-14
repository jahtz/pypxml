# Copyright 2025 Janik Haitz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Union
from pathlib import Path
import csv

import rich_click as click
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn

from pypxml import PageType
from pypxml.pagetype import is_valid


# Progressbar
progress = Progress(TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    MofNCompleteColumn(),
                    TextColumn("•"),
                    TimeElapsedColumn(),
                    TextColumn("•"),
                    TimeRemainingColumn(),
                    TextColumn("• {task.fields[filename]}"))


# Callbacks
def paths_callback(ctx, param, value: list[str]) -> list[Path]:
    """ Parse a list of click paths to a list of pathlib Path objects. """
    return [] if value is None else list([Path(p) for p in value])

def path_callback(ctx, param, value: str) -> Optional[Path]:
    """ Parse a click path to a pathlib Path object. """
    return None if value is None else Path(value)

def suffix_callback(ctx, param, value: Optional[str]) -> Optional[str]:
    """ Parses a string to a valid suffix. """
    return None if not value else (value if value.startswith('.') else f".{value}")

def pagetype_callback(ctx, param, value: str) -> Optional[tuple[PageType, Optional[str]]]:
    """ Parses a string to a valid PageType and subtype"""
    if value is None:
        return None
    parts = value.split(".")
    if is_valid(parts[0]):
        if len(parts) == 1:
            return (PageType(parts[0]), None)
        elif len(parts) == 2:
            return (PageType(parts[0]), parts[1])
    raise click.BadArgumentUsage(f"Invalid PageType: {value}. Valid PageTypes are: \n{', '.join([p.name for p in PageType])}.")


# Helper
def expand_paths(paths: Union[Path, list[Path]], glob: str = '*') -> list[Path]:
    """ Expands a list of paths by unpacking directories. """
    result = []
    if isinstance(paths, list):
        for path in paths:
            if path.is_dir():
                result.extend([p for p in path.glob(glob) if p.is_file()])
            else:
                result.append(path)
    elif isinstance(paths, Path):
        if paths.is_dir():
            result.extend([p for p in paths.glob(glob) if p.is_file()])
        else:
            result.append(paths)
    return sorted(result)


def csv_print(data: list[list], header: Optional[list[str]] = None, delimiter: Optional[str] = None) -> None:
    """
    Prints a list of lists to stdout. If a delimiter is specified, it will be printed in a csv format.
    If no delimiter is specified, it will be printed in a tabular format.
    Args:
        data: The data to be printed.
        header: The header of the data. If None, no header will be printed. Defaults to None.
        delimiter: The delimiter to be used. If None, a tabular format will be used. Defaults to None.
    """
    if header and len(header) != len(data[0]):
        raise ValueError(f"Header length {len(header)} does not match data length {len(data[0])}!")
    
    if delimiter is not None:
        print(delimiter.join(header))
        for row in data:
            print(delimiter.join([str(r) for r in row]))
            
    else:
        if header: 
            data.insert(0, header)
        max_lengths = [max([len(str(r)) for r in col]) for col in zip(*data)]
        for i, row in enumerate(data):
            print("  ".join([f"{str(r):>{max_lengths[i]}}" if isinstance(r, int) else f"{str(r):<{max_lengths[i]}}" for i, r in enumerate(row)]))
            if header and i == 0:
                print("  ".join(["-" * max_lengths[i] for i in range(len(row))]))


def csv_write(data: list[list], output: Path, header: Optional[list[str]] = None, delimiter: str = ",") -> None:
    """
    Writes a list of lists to a csv file.
    Args:
        data: The data to be written.
        output: The output file path.
        header: The header of the data. If None, no header will be written. Defaults to None.
        delimiter: The delimiter to be used. Defaults to ",".
    """
    if header and len(header) != len(data[0]):
        raise ValueError(f"Header length {len(header)} does not match data length {len(data[0])}!")
    
    with open(output, "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        if header:
            writer.writerow(header)
        writer.writerows(data)