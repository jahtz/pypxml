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

import csv
from pathlib import Path
from typing import Optional, Union

import rich_click as click
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn

from pypxml import PageType


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
def callback_path(ctx, param, value: Optional[str]) -> Optional[Path]:
    """ Parses a click path into a pathlib Path object. """
    return None if value is None else Path(value)

def callback_paths(ctx, param, value: Optional[list[str]]) -> list[Path]:
    """ Parses a list of click paths into a list of pathlib Path objects. """
    return [] if value is None else list([Path(p) for p in value])

def callback_suffix(ctx, param, value: Optional[str]) -> Optional[str]:
    """ Parses a string into a valid suffix. """
    return None if value is None else (value if value.startswith('.') else f".{value}")

def callback_logging(ctx, param, value: Optional[int]) -> int:
    """ Returns the logging level based on a verbosity counter ("0": ERROR, "1": WARNING, "2": INFO, ">2": DEBUG). """
    return 40 if value is None else 40 - (min(3, value) * 10)

def callback_pagetype(ctx, param, value: Optional[str]) -> Optional[PageType]:
    """ Returns a PageType from a string. """
    if value is None:
        return None
    elif PageType.is_valid(value):
        return PageType[value]
    else:
        raise click.BadOptionUsage(param, f"{value} is not a valid PageType")
    
def callback_region_rules(ctx, param, value: tuple[str]) -> dict[str, tuple[PageType, Optional[str]]]:
    """ 
    Parses a list or tuple with rule strings into a dictionary (keys are strings of format pagetype.subtype or pagetype 
    and represent the source) and values are tuples of type (PageType, subtype). 
    All PageTypes have to be valid and regions.
    """
    def parse_type(t: str) -> tuple[PageType, Optional[str]]:
        if t.count('.') > 1:
            raise click.BadOptionUsage(param, f"Invalid format: region can only be specified in format RegionType or "
                                              f"RegionType.subtype, got `{t}`")
        if '.' in t:
            pagetype, subtype = t.split('.')
        else:
            pagetype, subtype = t, None
        if not PageType.is_valid(pagetype):
            raise click.BadOptionUsage(param, f"Invalid PageType: `{pagetype}`")
        pagetype = PageType[pagetype]
        if not pagetype.is_region:
            raise click.BadOptionUsage(param, f"Invalid Region: `{pagetype}`")
        return pagetype, subtype
    
    result = {}
    for rule in value:
        if rule.count(':') != 1:
            raise click.BadOptionUsage(param, f"Invalid format: expected exactly one `:`, got {rule.count(':')}")
        sources, target = rule.split(':')
        sources = [s.strip() for s in sources.split(',') if s.strip()]
        if not sources:
            raise click.BadOptionUsage(param, f"Invalid format: at least one non-empty source is required, got `{rule}`")
        if ',' in target:
            raise click.BadOptionUsage(param, f"Invalid format: only one target can be specified, got `{target}`")
        target = parse_type(target) if target else None
        for source in sources:
            parse_type(source)  # validate
            if source in result:
                raise click.BadOptionUsage(param, f"Invalid format: `{source}` cannot declared multiple times as a source")
            result[source] = target
    return result

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
