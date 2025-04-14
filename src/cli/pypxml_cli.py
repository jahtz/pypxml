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

import rich_click as click

from .analytics_cli import list_regions_cli
from .search_cli import search_text_cli, search_type_cli
from .transformation_cli import remove_elements_cli


__version__ = "3.0.0"
__prog__ = "pypxml"

click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.MAX_WIDTH = 90
#click.rich_click.RANGE_STRING = ""
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True
click.rich_click.FOOTER_TEXT = f"Developed at Centre for Philology and Digitality (ZPD), University of Würzburg"
click.rich_click.OPTION_GROUPS = {
    "pypxml": [
        {
            "name": "Help",
            "options": ["--help", "--version"],
        }
    ],
    "pypxml list-regions": [
        {
            "name": "Input",
            "options": ["directory", "--glob"],
        },
        {
            "name": "Options",
            "options": ["--pages", "--count"],
        },
        {
            "name": "Output",
            "options": ["--output", "--delimiter"],
        }
    ],
    "pypxml remove-elements": [
        {
            "name": "Input",
            "options": ["PageXML", "--glob"],
        },
        {
            "name": "Options",
            "options": ["--type", "--attribute"],
        },
        {
            "name": "Output",
            "options": ["--output"],
        }
    ],
    "pypxml search-text": [
        {
            "name": "Input",
            "options": ["directory", "string", "--glob", "--index"],
        },
        {
            "name": "Options",
            "options": ["--lines", "--count", "--total"],
        },
        {
            "name": "Output",
            "options": ["--output", "--delimiter"],
        }
    ],
    "pypxml search-type": [
        {
            "name": "Input",
            "options": ["directory", "pagetype", "--glob"],
        },
        {
            "name": "Options",
            "options": ["--count", "--total"],
        },
        {
            "name": "Output",
            "options": ["--output", "--delimiter"],
        }
    ],
}


@click.group()
@click.help_option("--help")
@click.version_option(__version__,
                      "--version",
                      prog_name=__prog__,
                      message=f"{__prog__} v{__version__} - Developed at Centre for Philology and Digitality (ZPD), "
                              f"University of Würzburg")
def cli(**kwargs):
    """
    A python library for parsing, converting and modifying PageXML files.
    """
    pass


# analytics
cli.add_command(list_regions_cli)

# search
cli.add_command(search_text_cli)
cli.add_command(search_type_cli)

# transformation
cli.add_command(remove_elements_cli)
