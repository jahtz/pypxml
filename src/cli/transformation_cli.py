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


@click.command("remove-elements", short_help="Remove PageElements from PageXML files.")
@click.help_option("--help", hidden=True)
@click.argument("PageXML",
                type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
                callback=util.paths_callback, required=True, nargs=-1)
@click.option("-g", "--glob", "glob",
              help="Glob pattern for matching PageXML files in directory passed in PageXML.",
              type=click.STRING, default="*.xml", required=False, show_default=True)
@click.option("-o", "--output", "output",
              help="Output file for the results. If not specified, the results will overwrite the input PageXML files.",
              type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
              callback=util.path_callback, default=None, required=False)
@click.option("-t", "--type", "pagetype", 
              help="Type of PageElement to remove. If not set, all PageElements will be removed (ignoring attributes).",
              type=click.STRING, callback=util.pagetype_callback, required=False)
@click.option("-a", "--attribute", "attribute",
              help="Attribute of the PageElement to remove. If not set, all matching PageElements will be removed. "
                   "Example: --attribute type paragraph",
              type=click.Tuple([str, str]), nargs=2, required=False, multiple=True)
def remove_elements_cli(pagexml: list[Path], glob: str = "*.xml", output: Optional[Path] = None, 
                        pagetype: Optional[tuple[PageType, Optional[str]]] = None, 
                        attribute: list[tuple[str, str]] = None) -> None:
    """
    Remove PageElements from PageXML files.
    """
    files = util.expand_paths(pagexml, glob)
    if not files:
        raise click.BadArgumentUsage(f"No PageXML files found!")
    rprint(f"{len(files)} PageXML files found")
    
    if output is not None:
        output.parent.mkdir(exist_ok=True, parents=True)
        
    attributes = {attr[0]: attr[1] for attr in attribute}
    
    with util.progress as p:
        task = p.add_task("Removing...", total=len(files), filename="")
        for fp in files:
            p.update(task, filename=Path(*fp.parts[-min(len(fp.parts), 4):]))
            pxml = PageXML.from_file(fp, skip_unknown=True)
            if pagetype is not None:
                for element in pxml.find_by_type(pagetype[0], depth=-1, **attributes):
                    element.parent.remove_element(element)
            else:
                pxml.clear_elements()
            if output is not None:
                pxml.to_file(output.joinpath(fp.name))
            else:
                pxml.to_file(fp)
            p.update(task, advance=1)
        p.update(task, filename="Done")
        

