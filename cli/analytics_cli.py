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

from collections import Counter
from pathlib import Path
import string
from typing import Optional, Literal
import unicodedata as ud

from pypxml import PageXML, PageType
import click

from . import util


@click.command("get-codec", short_help="Extract the character set from PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument(
    "files",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    callback=util.callback_paths, 
    nargs=-1, 
    required=True
)
@click.option(
    "-o", "--output", "output",
    help="Path to a CSV file to save the results. If omitted, results are printed to stdout. "
         "If a directory is given, the file 'codec.csv' will be created inside it.",
    type=click.Path(exists=False, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path)
)
@click.option(
    "-l", "--level", "level", 
    help="PageXML level from which to extract text.", 
    type=click.Choice(["TextRegion", "TextLine", "Word", "Glyph"]),
    callback=util.callback_pagetype,
    default="TextLine", show_default=True
)
@click.option(
    "-i", "--index", "index",
    help="Only consider TextEquiv elements with the specified index.",
    type=click.INT
)
@click.option(
    "-w", "--remove-whitespace", "remove_whitespace", 
    help="Remove all whitespace characters before analyzing text.",
    type=click.BOOL, is_flag=True
)
@click.option(
    "-f", "--frequencies", "frequencies",
    help="Also output character frequencies.",
    type=click.BOOL, is_flag=True
)
@click.option(
    "-n", "--normalize", "normalize",
    help="Normalize unicode before analyzing text.",
    type=click.Choice(["NFC", "NFD", "NFKC", "NFKD"])
)
def get_codec(
    files: list[Path], 
    output: Optional[Path] = None, 
    level: PageType = PageType.TextLine, 
    index: Optional[int] = None, 
    remove_whitespace: bool = False, 
    frequencies: bool = False, 
    normalize: Optional[Literal["NFC", "NFD", "NFKC", "NFKD"]] = None
) -> None:
    """
    This tool analyzes the text content of PageXML files and extracts the set of characters used.
    
    It can optionally normalize unicode, remove whitespace, and output character frequencies.
    Results are printed to the console or saved as a CSV file.
    
    FILES: List of PageXML file paths to process. Accepts individual files, glob wildcards, or directories.
    """
    if output and output.is_dir():
        output = output.joinpath("codec.csv")
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)

    results = Counter()
    with util.PROGRESS as progressbar:
        task = progressbar.add_task("Processing", total=len(files), filename="")
        for fp in files:
            progressbar.update(task, filename=Path("/", *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.from_file(fp, raise_on_error=False)
            for element in pagexml.find_by_type(level, depth=-1):
                if text := element.find_text(index=index):
                    if normalize:
                        text = ud.normalize(normalize, text)
                    if remove_whitespace:
                        text = text.translate(str.maketrans('', '', string.whitespace))
                    results.update(text)
            progressbar.advance(task)
        progressbar.update(task, filename="Done")
    
    codec_dict = {k: v for k, v in results.most_common(None)}
    data = sorted([[k, v] for k, v in codec_dict.items()], reverse=True, key=lambda x: x[1])
    if not frequencies:
            data = [[x[0]] for x in data]
    if output:        
        util.csv_write(data, output, header=["character", "frequency"] if frequencies else ["character"], delimiter=";")
    else:
        for x in data:
            print(f"{x[0]}" if not frequencies else f"{x[0]}: {x[1]}")


@click.command("get-regions", short_help="List all regions in PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument(
    "files",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    callback=util.callback_paths, 
    nargs=-1, 
    required=True
)
@click.option(
    "-o", "--output", "output",
    help="CSV file or directory where the results are saved. If a directory is given, the file 'regions.csv' will be "
         "created inside it. If omitted, results are printed to stdout.",
    type=click.Path(exists=False, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path)
)
@click.option(
    "-l", "--level", "level",
    help="Set the aggregation level for the output. 'total' combines all files, 'directory' aggregates by parent "
         "directory, and 'file' lists results per individual file.",
    type=click.Choice(["total", "directory", "file"]), 
    default="total", 
    show_default=True
)
@click.option(
    "-f", "--frequencies", "frequencies",
    help="Also output the frequency (count) of each region type.",
    type=click.BOOL, is_flag=True
)
@click.option(
    "-t", "--types", "types",
    help="Include subtypes by printing them as 'PageType.type' if available.",
    type=click.BOOL, is_flag=True
)
def get_regions(
    files: list[Path], 
    output: Optional[Path] = None, 
    level: Literal["total", "directory", "file"] = "", 
    frequencies: bool = False, 
    types: bool = False
) -> None:
    """
    Analyzes PageXML files and lists the region types found.
    
    Optionally includes subtypes, outputs frequencies, and group by file, directory, or globally.
    
    FILES: List of PageXML file paths to process. Accepts individual files, glob wildcards, or directories.
    """
    if output and output.is_dir():
        output = output.joinpath("regions.csv")
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)

    results = {}
    with util.PROGRESS as progressbar:
        task = progressbar.add_task("Processing", total=len(files), filename="")
        for fp in files:
            progressbar.update(task, filename=Path("/", *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.from_file(fp, raise_on_error=False)
            found_regions = []
            for region in pagexml.regions:
                t = f"{region.pagetype.value}.{region['type']}" if types and "type" in region else region.pagetype.value
                found_regions.append(t)
            results[str(fp)] = Counter(found_regions)
            progressbar.advance(task)
        progressbar.update(task, filename="Done")

    format_count = lambda c: str(c) if frequencies else ("x" if c > 0 else "")
    if level in ["file", "directory"]:
        groups = results if level == "file" else {}
        if level == "directory":
            for fp, count in results.items():
                groups.setdefault(str(Path(fp).parent), Counter()).update(count)
        header = [level] + sorted({r for c in results.values() for r in c})
        data = [[name] + [format_count(counter.get(k, 0)) for k in header[1:]]
                for name, counter in groups.items()]
    else:
        header = ["type", "frequency"] if frequencies else ["type"]
        total = Counter()
        for count in results.values():
            total.update(count)
        data = [[r, str(total[r])] if frequencies else [r] 
                for r in sorted(total, key=lambda x: -total[x] if frequencies else x)]

    if output:        
        util.csv_write(data, output, header=header, delimiter=",")
    else:
        print(";".join(header))
        for row in data:
            print(";".join(row))


@click.command("get-custom", short_help="List all custom region attributes in PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument(
    "files",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    callback=util.callback_paths, 
    nargs=-1, 
    required=True
)
@click.option(
    "-o", "--output", "output",
    help="CSV file or directory where the results are saved. If a directory is given, the file 'customs.csv' will be "
         "created inside it. If omitted, results are printed to stdout.",
    type=click.Path(exists=False, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path)
)
@click.option(
    "-l", "--level", "level",
    help="Set the aggregation level for the output. 'total' combines all files, 'directory' aggregates by parent "
         "directory, and 'file' lists results per individual file.",
    type=click.Choice(["total", "directory", "file"]), 
    default="total", show_default=True
)
@click.option(
    "-f", "--frequencies", "frequencies",
    help="Also output the frequency (count) of each custom attribute.",
    type=click.BOOL, is_flag=True
)
def get_custom(
    files: list[Path], 
    output: Optional[Path] = None, 
    level: Literal["total", "directory", "file"] = "", 
    frequencies: bool = False
) -> None:
    """
    Analyzes PageXML files and lists the custom region types found.
    
    Optionally outputs frequencies and group by file, directory, or globally.
    
    FILES: List of PageXML file paths to process. Accepts individual files, glob wildcards, or directories.
    """
    if output and output.is_dir():
        output = output.joinpath("regions.csv")
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)

    results = {}
    with util.PROGRESS as progressbar:
        task = progressbar.add_task("Processing", total=len(files), filename="")
        for fp in files:
            progressbar.update(task, filename=Path("/", *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.from_file(fp, raise_on_error=False)
            found_regions = []
            for region in pagexml.regions:
                found_regions.append(region["custom"] if "custom" in region else "None")
            results[str(fp)] = Counter(found_regions)
            progressbar.advance(task)
        progressbar.update(task, filename="Done")

    format_count = lambda c: str(c) if frequencies else ("x" if c > 0 else "")
    if level in ["file", "directory"]:
        groups = results if level == "file" else {}
        if level == "directory":
            for fp, count in results.items():
                groups.setdefault(str(Path(fp).parent), Counter()).update(count)
        header = [level] + sorted({r for c in results.values() for r in c})
        data = [[name] + [format_count(counter.get(k, 0)) for k in header[1:]]
                for name, counter in groups.items()]
    else:
        header = ["type", "frequency"] if frequencies else ["type"]
        total = Counter()
        for count in results.values():
            total.update(count)
        data = [[r, str(total[r])] if frequencies else [r] 
                for r in sorted(total, key=lambda x: -total[x] if frequencies else x)]

    if output:        
        util.csv_write(data, output, header=header, delimiter=",")
    else:
        print(";".join(header))
        for row in data:
            print(";".join(row))

    
@click.command("get-text", short_help="Extract text from PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument(
    "files",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    callback=util.callback_paths, 
    nargs=-1, 
    required=True
)
@click.option(
    "-o", "--output", "output",
    help="Output destination. If a directory is specified, a separate text file is created for each PageXML file, "
         "ignoring the page separator. If a file is specified, the text from all files is concatenated into that file. "
         "If omitted, the text is printed to stdout.",
    type=click.Path(exists=False, dir_okay=True, file_okay=True, resolve_path=True, path_type=Path)
)
@click.option(
    "-i", "--index", "index",
    help="Use only the text from TextEquiv elements at the given index.",
    type=click.INT
)
@click.option(
    "-r", "--region-separator", "region_separator",
    help="Separator string inserted between regions. Use \"\" for an empty line, \"\\n\" for two empty lines, ...", 
    type=click.STRING
)
@click.option(
    "-p", "--page-separator", "page_separator",
    help="Separator string inserted between pages when outputting to a single file or stdout. "
         "Ignored when outputting multiple files. Use \"\" for an empty line, \"\\n\" for two empty lines, ...",
    type=click.STRING
)
def get_text(
    files: list[Path], 
    output: Optional[Path] = None, 
    index: Optional[int] = None,
    region_separator: Optional[str] = None, 
    page_separator: Optional[str] = None
) -> None:
    """
    Extract text from PageXML files at the TextLine level.
    
    Outputs to individual text files, a single file, or prints to the console, 
    with optional separators between regions and pages.
    
    FILES: List of PageXML file paths to process. Accepts individual files, glob wildcards, or directories.
    """
    region_sep = None if region_separator is None else region_separator.replace("\\n", "\n")
    page_sep = None if page_separator is None else page_separator.replace("\\n", "\n")
    
    # multi: output is a directory and a text file for each input file is generated
    # single: output is a file and all text will be written to this file
    # print: no output was passed and text is printed to console
    if output and output.is_dir():
        output.mkdir(parents=True, exist_ok=True)
        mode = "multi"
    elif output and output.is_file():
        output.parent.mkdir(parents=True, exist_ok=True)
        mode = "single"
    else:
        mode = "print"
    
    results = []
    with util.PROGRESS as progressbar:
        task = progressbar.add_task("Processing", total=len(files), filename="")
        for i, fp in enumerate(files, start=1):
            progressbar.update(task, filename=Path("/", *fp.parts[-min(len(fp.parts), 4):]))
            pagexml = PageXML.from_file(fp, raise_on_error=False)
            ptext = False
            for j, region in enumerate(pagexml.regions, start=1):
                rtext = False
                for textline in region.find_by_type(PageType.TextLine):
                    if (text := textline.find_text(index=index)) is not None and text.strip():
                        ptext = rtext = True
                        results.append(text)
                if rtext and region_sep is not None and j != len(pagexml.regions):  # split regions by the defined separator
                    results.append(region_sep)
                if not rtext and j > 0 and results and results[-1] == region_sep:  # remove the separator if the previous one did not contain text as well
                    results.pop()
            if ptext and mode != "multi" and page_sep is not None and i != len(files):  # split pages by the defined separator
                results.append(page_sep)

            if mode == "multi":  # write the content of the current file
                output.joinpath(fp.name.split(".")[0] + ".txt").write_text("\n".join(results), encoding="utf-8")
                results.clear()
            progressbar.advance(task)
        progressbar.update(task, filename="Done")

    if mode == "print":  # print all text to the console
        for line in results:
            print(line)
    elif mode == "single":  # print all text to a single file
        output.write_text("\n".join(results), encoding="utf-8")
