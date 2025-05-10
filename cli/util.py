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
from glob import glob
from pathlib import Path
from typing import Optional

import click
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn

from pypxml import PageType


PROGRESS = Progress(TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    MofNCompleteColumn(),
                    TextColumn("•"),
                    TimeElapsedColumn(),
                    TextColumn("•"),
                    TimeRemainingColumn(),
                    TextColumn("• {task.fields[filename]}"))


# CALLBACK
def callback_paths(ctx, param, value) -> list[Path]:
    if not value:
        raise click.BadParameter("", param=param)
    paths = []
    for pattern in value:
        expanded = glob(pattern, recursive=True)
        if not expanded:
            p = Path(pattern)
            if p.exists() and p.is_file():
                paths.append(p)
        else:
            paths.extend(Path(p) for p in expanded if Path(p).is_file())
    if not paths:
        raise click.BadParameter("None of the provided paths or patterns matched existing files.")
    return paths


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
        source, target = rule
        parse_type(source)  # validate source
        if source in result:
            raise click.BadOptionUsage(param, f"Invalid format: `{source}` cannot declared multiple times as a source")
        target = parse_type(target) if target.lower() != "none" else None
        result[source] = target
    return result


# HELPER
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
