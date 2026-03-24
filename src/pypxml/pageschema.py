# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class PageSchema:
    """
    Immutable representation of a PAGE-XML schema.

    Encapsulates XML namespace declarations and schema location for a PAGE-XML
    document. Supports predefined versions ('2017', '2019') and custom schemas.
    """

    xmlns: str
    xmlns_xsi: str
    xsi_schema_location: str

    _registry: ClassVar[dict[str, PageSchema]] = {}

    @classmethod
    def register(cls, name: str, schema: PageSchema) -> None:
        """ Register a PAGE-XML schema under a given name. """
        cls._registry[name] = schema

    @classmethod
    def get(cls, name: str) -> PageSchema:
        """ Retrieve a registered schema by name. Raises ValueError if unknown. """
        try:
            return cls._registry[name]
        except KeyError:
            raise ValueError(f'Unknown schema: {name}')

    @classmethod
    def custom(cls, xmlns: str, xmlns_xsi: str, xsi_schema_location: str) -> PageSchema:
        """ Create a custom PAGE-XML schema definition. """
        return cls(xmlns=xmlns, xmlns_xsi=xmlns_xsi, xsi_schema_location=xsi_schema_location)


PageSchema.register(
    name='2017',
    schema=PageSchema(
        xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15',
        xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
        xsi_schema_location='http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 '
                            'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd',
    )
)

PageSchema.register(
    name='2019',
    schema=PageSchema(
        xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15',
        xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
        xsi_schema_location='http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 '
                            'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd'
    )
)
