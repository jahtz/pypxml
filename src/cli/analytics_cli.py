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
from pypxml import PageXML

from . import util


@click.command("list-regions", short_help="List all PageXML regions in a directory.")
@click.help_option("--help", hidden=True)
@click.argument("directory",
                type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
                callback=util.path_callback, required=True)
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
@click.option("-p", "--pages", "pages",
              help="If set, the output will contain the number of pages for each PageType.",
              is_flag=True, default=False)
@click.option("-c", "--count", "count",
              help="If set, the output will contain the number of occurrences of each PageType.",
              is_flag=True, default=False)
def list_regions_cli(directory: Path, glob: str = "**/*.xml", output: Optional[Path] = None, 
                     delimiter: str = ",", pages: bool = False, count: bool = False) -> None:
    """
    List all PageXML regions in a directory.
    """
    files = util.expand_paths(directory, glob)
    if not files:
        raise click.BadArgumentUsage(f"No PageXML files found in \"{directory}\" with glob pattern \"{glob}\"!")
    rprint(f"{len(files)} PageXML files found")
    
    if output is not None:
        output.parent.mkdir(exist_ok=True, parents=True)
    
    results = {}
    with util.progress as p:
        task = p.add_task("Seaching...", total=len(files), filename="")
        for fp in files:
            p.update(task, filename=Path(*fp.parts[-min(len(fp.parts), 4):]))
            found = []
            pagexml = PageXML.from_file(fp, skip_unknown=True)
            for region in pagexml.regions:
                pagetype = region.pagetype.value
                if (t := region["type"]) is not None:
                    pagetype += f".{t}"
                if pagetype not in results:
                    results[pagetype] = [0, 0]  # stores page count and total count
                results[pagetype][1] += 1
                if pagetype not in found:
                    found.append(pagetype)
                    results[pagetype][0] += 1
            p.advance(task)
        p.update(task, filename="Done")
    
    header = ["Type"]
    if pages: 
        header.append("Pages")
    if count:
        header.append("Count")
    res = []
    keys = sorted(results.keys())
    for k in keys:
        v = results[k]
        data = [k]
        if pages:
            data.append(v[0])
        if count:
            data.append(v[1])
        res.append(data)
    
    if output is None:       
        util.csv_print(res, header=header) 
    else:
        util.csv_write(res, output, header=header, delimiter=delimiter)
        rprint(f"Results written to {output}")