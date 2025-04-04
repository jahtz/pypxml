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

from pathlib import Path
from typing import Optional

import rich_click as click
from rich import print as rprint
from pypxml import PageXML, PageType

from . import util


@click.command("search-string", short_help="Search for a string in PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument("directory",
                type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
                callback=util.path_callback, required=True)
@click.argument("string", 
                type=click.STRING, required=True)
@click.option("-g", "--glob", "glob",
              help="Glob pattern for matching PageXML files in directory passed in DIRECTORY.",
              type=click.STRING, default="**/*.xml", required=False, show_default=True)
@click.option("-o", "--output", "output",
              help="Output file for the results. If not specified, the results will be printed to stdout. "
                   "CSV format is recommended.",
              type=click.Path(exists=False, dir_okay=False, file_okay=True, resolve_path=True),
              callback = util.path_callback, default=None, required=False)
@click.option("-d", "--delimiter", "delimiter",
              help="Delimiter for the output file. Default is a comma.",
              type=click.STRING, default=",", required=False, show_default=True)
@click.option("-i", "--index", "index",
              help="Specify an `index` attribute so select a specific TextEquiv.",
              type=click.INT, default=None, required=False)
@click.option("-l", "--lines", "lines",
              help="If set, the output will contain the line id's in which the search string was found.",
              is_flag=True, default=False)
@click.option("-c", "--count", "count",
              help="If set, the output will contain the number of occurrences of the search string.",
              is_flag=True, default=False)
@click.option("-t", "--total", "total",
              help="If set, the output will only contain the total number of occurrences of the search string.",
              is_flag=True, default=False)
def search_string_cli(directory: Path, string: str, glob: str = "**/*.xml", output: Optional[Path] = None, 
                      delimiter: str = ",", index: Optional[int] = None, lines: bool = False, 
                      count: bool = False, total: bool = False) -> None:
    """
    Search for a string in PageXML files.
    """
    files = util.expand_paths(directory, glob)
    if not files:
        raise click.BadArgumentUsage(f"No PageXML files found in \"{directory}\" with glob pattern \"{glob}\"!")
    rprint(f"{len(files)} PageXML files found")
    
    if output is not None:
        output.parent.mkdir(exist_ok=True, parents=True)
    
    results = []  # stores data in the format: [filepath, counter, line id's]
        
    with util.progress as p:
        task = p.add_task("Seaching...", total=len(files), filename="")
        for fp in files:
            p.update(task, filename=Path(*fp.parts[-min(len(fp.parts), 4):]))
            page_res = [fp.as_posix(), 0, []]
            pagexml = PageXML.from_file(fp, skip_unknown=True)
            for textline in pagexml.find_by_type(PageType.TextLine, recursive=True):
                for textequiv in textline.find_by_type(PageType.TextEquiv):
                    if index is not None:
                        if textequiv["index"] is None or textequiv["index"] != str(index):
                            continue
                    uc = textequiv.find_by_type(PageType.Unicode)
                    if uc is None:
                        continue
                    if uc[0].text and string in uc[0].text:
                        page_res[1] += uc[0].text.count(string)
                        if textline["id"] not in page_res[2]:
                            page_res[2].append(textline["id"])
            if page_res[1] != 0:
                results.append(page_res)
            p.update(task, advance=1)
    
    if total:
        header = ["Search", "Pages"]
        res = [[string, len(results)]]
        if lines:
            header.append("Lines")
            res[0].append(sum([len(r[2]) for r in results]))
        if count:
            header.append("Total Count")
            res[0].append(sum([r[1] for r in results]))
        results = res
    else:
        header = ["File", "Count", "Lines"]
        rules = [True, count, lines]
        header = [h for i, h in enumerate(header) if rules[i]]
        for row in results:
            data = [r for i, r in enumerate(row) if rules[i]]
            row.clear()
            row.extend(data)     

    if output is None:       
        util.csv_print(results, header=header) 
    else:
        util.csv_write(results, output, header=header, delimiter=delimiter)
        rprint(f"Results written to {output}")
    
    
@click.command("search-type", short_help="Search for a PageType in PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument("directory",
                type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
                callback=util.path_callback, required=True)
@click.argument("pagetype", 
                type=click.STRING, callback=util.pagetype_callback, required=True)
@click.option("-g", "--glob", "glob",
              help="Glob pattern for matching PageXML files in directory passed in DIRECTORY.",
              type=click.STRING, default="**/*.xml", required=False, show_default=True)
@click.option("-o", "--output", "output",
              help="Output file for the results. If not specified, the results will be printed to stdout. "
                   "CSV format is recommended.",
              type=click.Path(exists=False, dir_okay=False, file_okay=True, resolve_path=True),
              default=None, required=False)
@click.option("-d", "--delimiter", "delimiter",
              help="Delimiter for the output file. Default is a comma.",
              type=click.STRING, default=",", required=False, show_default=True)
@click.option("-c", "--count", "count",
              help="If set, the output will contain the number of occurrences of the PageType in each file.",
              is_flag=True, default=False)
@click.option("-t", "--total", "total",
              help="If set, the output will only contain the total number of occurrences of the search type.",
              is_flag=True, default=False)
def search_type_cli(directory: Path, pagetype: tuple[PageType, str], glob: str = "**/*.xml", 
                    output: Optional[Path] = None, delimiter: str = ",", count: bool = False, 
                    total: bool = False) -> None:
    """
    Search for a PageType in PageXML files.
    
    PageTypes can be specified in the following format:
    
    - "PageType" (e.g. TextLine)
    
    - "PageType.subtype" (e.g. TextLine.marginalia)
    """
    files = util.expand_paths(directory, glob)
    if not files:
        raise click.BadArgumentUsage(f"No PageXML files found in \"{directory}\" with glob pattern \"{glob}\"!")
    rprint(f"{len(files)} PageXML files found")
    
    if output is not None:
        output.parent.mkdir(exist_ok=True, parents=True)
    
    results = []  # stores data in the format: [filepath, counter, line id's]
    
    with util.progress as p:
        task = p.add_task("Seaching...", total=len(files), filename="")
        for fp in files:
            p.update(task, filename=Path(*fp.parts[-min(len(fp.parts), 4):]))
            page_res = [fp.as_posix(), 0]
            pagexml = PageXML.from_file(fp, skip_unknown=True)
            regions = pagexml.find_by_type(pagetype[0], recursive=True)
            if pagetype[1] is not None:
                regions = [r for r in regions if r["type"] == pagetype[1]]
            page_res[1] = len(regions)
            if page_res[1] != 0:
                results.append(page_res)
            p.update(task, advance=1)
    
    if total:
        header = ["Search", "Pages"]
        res = [[str(pagetype[0].value) + (f" ({pagetype[1]})" if pagetype[1] else ""), len(results)]]
        if count:
            header.append("Total Count")
            res[0].append(sum([r[1] for r in results]))
        results = res
    else:
        header = ["File", "Count"]
        rules = [True, count]
        header = [h for i, h in enumerate(header) if rules[i]]
        for row in results:
            data = [r for i, r in enumerate(row) if rules[i]]
            row.clear()
            row.extend(data)     

    if output is None:       
        util.csv_print(results, header=header) 
    else:
        util.csv_write(results, output, header=header, delimiter=delimiter)
        rprint(f"Results written to {output}")
