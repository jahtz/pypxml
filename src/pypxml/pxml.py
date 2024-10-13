# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from typing import Optional, Union, Self
from datetime import datetime
from pathlib import Path
import json

from lxml import etree

from .page import Page
from .resources.xml_schema import XMLSchema


class PageXML:
    def __init__(self, creator: str, created: str, changed: str) -> None:
        self.__creator: str = creator
        self.__created: str = created
        self.__changed: str = changed
        self.__pages: list[Page] = []

    def __len__(self) -> int:
        """ Returns the number of pages. """
        return len(self.__pages)

    def __iter__(self) -> Self:
        """ Iterator: starting point for iterating over all pages. """
        self.__n = 0
        return self

    def __next__(self) -> Page:
        """ Iterator: yield next page. """
        if self.__n < len(self.__pages):
            self.__n += 1
            return self.__pages[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: int) -> Optional[Page]:
        """
        Get the Page object of a given index.
        :param key: The index value of the Page object.
        :return: Page object if pages are available. Returns last page if index is out of range.
        """
        if len(self.__pages) > 0:
            return self.__pages[min(key, len(self.__pages) - 1)]
        return None

    def __setitem__(self, key: int, value: Page) -> None:
        """
        Set a Page object for a given index.
        :param key: The target index for the Page object.
        :param value: The new Page object.
        """
        if len(self.__pages) > 0:
            self.__pages[min(key, len(self.__pages) - 1)] = value

    def __contains__(self, key: Page) -> bool:
        """
        Checks if a Page objects exists.
        :param key: The Page object.
        :return: True, if the Page object exists. Else return False.
        """
        if isinstance(key, Page):
            return key in self.__pages
        return False

    @property
    def creator(self) -> Optional[str]:
        return self.__creator

    @creator.setter
    def creator(self, creator: str) -> None:
        self.__creator = str(creator)

    @property
    def created(self) -> Optional[str]:
        return self.__created

    @created.setter
    def created(self, created: Union[datetime, str]) -> None:
        if isinstance(created, datetime):
            self.__created = created.isoformat()
        else:
            self.__created = str(created)

    @property
    def changed(self) -> Optional[str]:
        return self.__changed

    @changed.setter
    def changed(self, changed: Union[datetime, str]) -> None:
        if isinstance(changed, datetime):
            self.__changed = changed.isoformat()
        else:
            self.__changed = str(changed)

    @property
    def pages(self) -> list[Page]:
        return self.__pages

    @classmethod
    def new(cls, creator: str = 'PyPXML') -> Self:
        """
        Create a new PageXML object from scratch.
        :param creator: Specify creator tag in PageXMLs metadata.
        :return: Newly created PageXML object.
        """
        return cls(creator, datetime.now().isoformat(), datetime.now().isoformat())

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """
        Create a new PageXML object from a lxml etree object.
        :param tree: lxml etree object.
        :return: PageXML object that represents the passed etree object.
        """
        if (md_tree := tree.find('./{*}Metadata')) is not None:
            if (creator := md_tree.find('./{*}Creator')) is not None:
                creator = creator.text
            if (created := md_tree.find('./{*}Created')) is not None:
                created = created.text
            if (last_change := md_tree.find('./{*}LastChange')) is not None:
                last_change = last_change.text
            pxml = cls(creator, created, last_change)
        else:
            pxml = cls.new()
        if (pages := tree.findall('./{*}Page')) is not None:
            for page_tree in pages:
                pxml.add_page(Page.from_etree(page_tree))
        return pxml

    def to_etree(self, version: str = '2019', schema_file: Optional[Path] = None) -> etree.Element:
        """
        Convert a PageXML object to a lxml etree element.
        :param version: PageXML Version to use. Currently supported: `2019`.
        :param schema_file: Custom schema in json format.
        :return: A lxml etree object that represents this PageXML object.
        """
        self.changed = datetime.now().isoformat()
        if schema_file is not None:
            with open(schema_file) as stream:
                schema = XMLSchema.custom('pagexml', version, json.load(stream))
        else:
            schema = XMLSchema.pagexml(version)
        xsi_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", 'schemaLocation')
        nsmap = { None: schema['xmlns'], 'xsi': schema['xmlns_xsi'] }
        root = etree.Element('PcGts', { xsi_qname: schema['xsi_schema_location'] }, nsmap=nsmap)
        metadata = etree.SubElement(root, 'Metadata')
        etree.SubElement(metadata, 'Creator').text = self.__creator
        etree.SubElement(metadata, 'Created').text = self.__created
        etree.SubElement(metadata, 'LastChange').text = self.__changed
        for page in self.__pages:
            root.append(page.to_etree())
        return root

    @classmethod
    def from_xml(cls, fp: Union[Path, str], encoding: Optional[str] = None) -> Self:
        """
        Create a new PageXML object from a PageXML file.
        :param fp: Path of PageXML file.
        :param encoding: Set custom encoding.
        :return: PageXML object.
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        tree = etree.parse(fp, parser).getroot()
        return cls.from_etree(tree)

    def to_xml(self, fp: Union[Path, str], version: str = '2019-07-15', schema_file: Optional[Path] = None,
               encoding: str = 'utf-8') -> None:
        """
        Create a PageXML file from a PageXML file.
        :param fp: Path to new PageXML file.
        :param version: The PageXML version to use. Currently supported: `2019`.
        :param schema_file: Custom schema in json format.
        :param encoding: Set custom encoding.
        """
        with open(fp, 'wb') as f:
            tree = etree.tostring(self.to_etree(version, schema_file),
                                  pretty_print=True,
                                  encoding=encoding,
                                  xml_declaration=True)
            f.write(tree)

    def add_page(self, page: Page, index: Optional[int] = None) -> None:
        """
        Add a Page object to the list of pages.
        :param page: The Page object to add.
        :param index: If set, insert the Page object at this index.
        """
        if index is None or index >= len(self.__pages) - 1:
            self.__pages.append(page)
        else:
            self.__pages.insert(index, page)

    def create_page(self, index: Optional[int] = None, **attributes: str) -> Page:
        """
        Create a new Page object and add it to the list of pages.
        :param index: If set, insert the Page object at this index.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created Page object.
        """
        page = Page.new(**attributes)
        self.add_page(page, index)
        return page

    def remove_page(self, page: Union[Page, int]) -> Optional[Page]:
        """
        Remove a Page object from the list of pages.
        :param page: The index of the Page object to remove or the Page object itself.
        :return: The Page object that was removed if it existed.
        """
        if isinstance(page, Page) and page in self.__pages:
            self.__pages.remove(page)
            return page
        elif isinstance(page, int) and page < len(self.__pages):
            return self.__pages.pop(page)

    def clear_pages(self) -> None:
        """ Remove all Page objects from the list of pages. """
        self.__pages.clear()
