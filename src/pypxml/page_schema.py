# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

import json
from pathlib import Path
from typing import Union


DEFAULT_SCHEMA = {
    "2017": {
        "xmlns": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15",
        "xmlns_xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi_schema_location": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd",
    },
    "2019": {
        "xmlns": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15",
        "xmlns_xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi_schema_location": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd",
    },
}


class PageSchema:
    @staticmethod
    def get(version: str = "2019") -> dict[str, str]:
        """
        Returns the xml schema values of a specified PageXML version.
        :param version: The PageXML version to use. Currently supported: `2017`, `2019`
        :return: A dictionary containing all header attributes: `xmlns`, `xmlns_xsi`, `xsi_schema_location`
        """
        return DEFAULT_SCHEMA[version]

    @staticmethod
    def custom(version: str, schema_file: Union[Path, str]) -> dict[str, str]:
        """
        Returns the custom xml schema values of a specified version.
        :param version: The version to use.
        :param schema_file: A JSON file containing the custom xml schema values.
        :return: A dictionary containing all header attributes provided by the custom schema.
        """
        with open(schema_file) as stream:
            schema = json.load(stream)
        return schema[version]
