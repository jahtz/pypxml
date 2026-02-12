# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class PageSchema:
    """
    Immutable representation of a PAGE-XML schema definition.

    This class encapsulates the XML namespace declarations and schema location
    required for a PAGE-XML document root. It also maintains a class-level
    registry of predefined schema versions (`2017`, `2019`) for convenient
    lookup, while allowing the creation of custom schema definitions.

    Instances are immutable and safe to share. The registry is intended as a
    lightweight factory for commonly used PAGE-XML schema variants.
    """

    xmlns: str
    xmlns_xsi: str
    xsi_schema_location: str

    _registry: ClassVar[dict[str, 'PageSchema']] = {}

    @classmethod
    def register(cls, name: str, schema: 'PageSchema') -> None:
        cls._registry[name] = schema

    @classmethod
    def get(cls, name: str) -> 'PageSchema':
        try:
            return cls._registry[name]
        except KeyError:
            raise ValueError(f'Unknown schema: {name}')

    @classmethod
    def custom(cls, xmlns: str, xmlns_xsi: str, xsi_schema_location: str) -> 'PageSchema':
        return cls(xmlns=xmlns, xmlns_xsi=xmlns_xsi, xsi_schema_location=xsi_schema_location)


PageSchema.register(
    name='2017',
    schema=PageSchema(
        xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15',
        xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
        xsi_schema_location='http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd',
    )
)

PageSchema.register(
    name='2019',
    schema=PageSchema(
        xmlns='http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15',
        xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
        xsi_schema_location='http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd'
    )
)