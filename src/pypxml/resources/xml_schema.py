# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from typing import Literal


DEFAULT_SCHEMA = {
    'pagexml': {
        '2019': {
            'xmlns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15',
            'xmlns_xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi_schema_location': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd'
        },
        '2017': {
            'xmlns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15',
            'xmlns_xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi_schema_location': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd'
        }
    }
}


class XMLSchema:
    @staticmethod
    def pagexml(version: Literal['2019', '2017'] = '2019') -> dict[str, str]:
        """
        Returns the xml schema values of a specified PageXML version.
        :param version: The PageXML version to use.
        :return: A dictionary containing all header attributes: `xmlns`, `xmlns_xsi`, `xsi_schema_location`
        """
        return DEFAULT_SCHEMA['pagexml'][version]

    @staticmethod
    def custom(schema: str, version: str, custom: dict) -> dict[str, str]:
        """
        Returns the custom xml schema values of a specified version.
        :param schema: The schema to use.
        :param version: The version to use.
        :param custom: A dictionary containing custom xml schema values. See DEFAULT_SCHEMA as example.
        :return: A dictionary containing all header attributes provided by the custom schema.
        """
        return custom[schema][version]
