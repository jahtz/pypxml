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

import logging

import click
from rich.logging import RichHandler

from .analytics_cli import get_codec, get_regions, get_custom, get_text
from .regularize_cli import regularize_codec, regularize_regions


__version__ = "4.2.3"
__prog__ = "pypxml"
__footer__ = "Developed at Centre for Philology and Digitality (ZPD), University of Würzburg"

logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)]
)
logger = logging.getLogger("pagexml")


@click.group(epilog=__footer__)
@click.help_option("--help")
@click.version_option(
    __version__, "--version",
    prog_name=__prog__,
    message=f"{__prog__} v{__version__}\n{__footer__}"
)
def cli(**kwargs):
    """
    A python library for parsing, converting and modifying PageXML files.
    """
    pass


# analytics
cli.add_command(get_codec)
cli.add_command(get_regions)
cli.add_command(get_custom)
cli.add_command(get_text)

# regularize
cli.add_command(regularize_codec)
cli.add_command(regularize_regions)
