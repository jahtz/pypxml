# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from datetime import datetime
from pathlib import Path
from typing import Optional, Self, Union

from lxml import etree

from .page_element import PageElement
from .page_schema import PageSchema
from .page_types import PageType


class PageXML:
    def __init__(self, creator: Optional[str] = None, created: Optional[Union[datetime, str]] = None,
                 changed: Optional[Union[datetime, str]] = None, **attributes: str) -> None:
        """
        Please use the .new() constructor.
        :param creator: Metadata `Creator` content.
        :param created: Metadata `Created` content.
        :param changed: Metadata `LastChange` content.
        :param attributes: Addition page attributes.
        """
        # Metadata:
        self.__creator: Optional[str] = creator
        self.__created: Optional[str] = None
        if isinstance(created, datetime):
            self.__created = created.isoformat()
        elif isinstance(created, str):
            self.__created = created
        self.__changed: Optional[str] = None
        if isinstance(changed, datetime):
            self.__changed = changed.isoformat()
        elif isinstance(changed, str):
            self.__changed = changed

        # Page:
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__reading_order: list[str] = []  # list of region id's in correct order
        self.__elements: list[PageElement] = []  # content of page

    def __len__(self) -> int:
        """Return number of elements"""
        return len(self.__elements)

    def __iter__(self) -> Self:
        self.__n = 0
        return self

    def __next__(self) -> PageElement:
        """Iterator: yield next element."""
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[PageElement, str]]:
        """
        Get an PageElement object by its index or an attribute value by its key
        :param key: Index (integer) of an PageElement object or a key (string) of an attribute.
        :return: The PageElement of passed index (returns last object if the key is out of range) or the value of the
            selected attribute. Returns None, if no match was found.
        """
        if isinstance(key, int) and len(self.__elements) > 0:
            return self.__elements[min(key, len(self.__elements) - 1)]
        elif isinstance(key, str) and key in self.__attributes:
            return self.__attributes[key]
        return None

    def __setitem__(self, key: Union[int, str], value: Union[PageElement, str]) -> None:
        """
        Set an PageElement object or an attribute value.
        :param key: Index (integer) for an PageElement object or a key (string) for an attribute.
        :param value: PageElement object (if key is of type integer) or a string (if key is of type string).
        """
        if isinstance(key, int) and isinstance(value, PageElement) and len(self.__elements) > 0:
            self.__elements[min(key, len(self.__elements) - 1)] = value
        elif isinstance(key, str):
            self.__attributes[key] = value
        else:
            raise ValueError("Invalid key or value")

    def __contains__(self, key: Union[PageElement, str]) -> bool:
        """
        Checks if an PageElement object or an attribute exists.
        :param key: PageElement object or attribute key.
        :return: True, if either the passed PageElement object or the attribute exists. Else return False.
        """
        if isinstance(key, PageElement):
            return key in self.__elements
        elif isinstance(key, str):
            return key in self.__attributes
        return False

    @property
    def creator(self) -> Optional[str]:
        """PageXML Metadata: `Creator`."""
        return self.__creator

    @creator.setter
    def creator(self, creator: str) -> None:
        """PageXML Metadata: `Creator`."""
        self.__creator = str(creator)

    @property
    def created(self) -> Optional[str]:
        """PageXML Metadata: `Created`."""
        return self.__created

    @created.setter
    def created(self, created: Union[datetime, str]) -> None:
        """PageXML Metadata: `Created`."""
        if isinstance(created, datetime):
            self.__created = created.isoformat()
        else:
            self.__created = str(created)

    @property
    def changed(self) -> Optional[str]:
        """PageXML Metadata: `LastChange`."""
        return self.__changed

    @changed.setter
    def changed(self, changed: Union[datetime, str]) -> None:
        """PageXML Metadata: `LastChange`."""
        if isinstance(changed, datetime):
            self.__changed = changed.isoformat()
        else:
            self.__changed = str(changed)

    @property
    def attributes(self) -> dict[str, str]:
        """Page: List of all attributes."""
        return self.__attributes

    @property
    def reading_order(self) -> list[str]:
        """Page: List of ReadingOrder region id's"""
        return self.__reading_order

    @property
    def elements(self) -> list[PageElement]:
        """List of all PageElement objects."""
        return self.__elements

    @property
    def regions(self) -> list[PageElement]:
        """List of all PageElement objects that are regions."""
        return list([element for element in self.__elements if element.is_region()])

    @property
    def image_filename(self) -> Optional[str]:
        """Page: imageFilename attribute."""
        return self.__attributes.get("imageFilename", None)

    @image_filename.setter
    def image_filename(self, filename: Optional[str]) -> None:
        """Page: imageFilename attribute."""
        if filename is None:
            self.__attributes.pop("imageFilename", None)
        else:
            self.__attributes["imageFilename"] = str(filename)

    @property
    def width(self) -> Optional[int]:
        """Page: imageWidth attribute."""
        if (w := self.__attributes.get("imageWidth", None)) is not None:
            return int(w)
        return None

    @width.setter
    def width(self, width: Optional[Union[int, str]]) -> None:
        """Page: imageWidth attribute."""
        if width is None:
            self.__attributes.pop("imageWidth", None)
        else:
            self.__attributes["imageWidth"] = str(width)

    @property
    def height(self) -> Optional[int]:
        """Page: imageHeight attribute."""
        if (h := self.__attributes.get("imageHeight", None)) is not None:
            return int(h)
        return None

    @height.setter
    def height(self, height: Optional[Union[int, str]]) -> None:
        """Page: imageHeight attribute."""
        if height is None:
            self.__attributes.pop("imageHeight", None)
        else:
            self.__attributes["imageHeight"] = str(height)

    @classmethod
    def new(cls, creator: str = "PyPXML", **attributes: str) -> Self:
        """
        Create a new PageXML object from scratch.
        :param creator: Specify creator tag in PageXMLs metadata.
        :param attributes: Named arguments that will be stored as attributes.
        :return: Newly created PageXML object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(creator, datetime.now().isoformat(), datetime.now().isoformat(), **attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element, skip_unknown: bool = False) -> Self:
        """
        Create a new PageXML object from a lxml etree object.
        :param tree: lxml etree object.
        :param skip_unknown: Skip unknown elements.
        :return: PageXML object that represents the passed etree object.
        """
        if (page := tree.find("./{*}Page")) is not None:
            attributes = dict(page.items())
            # Metadata
            if (md_tree := tree.find("./{*}Metadata")) is not None:
                if (creator := md_tree.find("./{*}Creator")) is not None:
                    creator = creator.text
                if (created := md_tree.find("./{*}Created")) is not None:
                    created = created.text
                if (last_change := md_tree.find("./{*}LastChange")) is not None:
                    last_change = last_change.text
                pxml = cls(creator, created, last_change, **attributes)
            else:
                pxml = cls.new(**attributes)
            # ReadingOrder
            if (ro := tree.find("./{*}ReadingOrder")) is not None:
                if (ro_elements := tree.findall("../{*}RegionRefIndexed")) is not None:
                    page._ro = list([i.get("regionRef") for i in sorted(list(ro_elements),
                                                                        key=lambda i: i.get("index"))])
                tree.remove(ro)
            # Elements
            for element in page:
                if (pe := PageElement.from_etree(element, skip_unknown=skip_unknown)) is not None:
                    pxml.add_element(pe, ro=False)
            return pxml
        else:
            raise ValueError("Page not found")

    def to_etree(self, version: str = "2019", schema_file: Optional[Path] = None) -> etree.Element:
        """
        Convert a PageXML object to a lxml etree element.
        :param version: PageXML Version to use. Currently supported: `2019`.
        :param schema_file: Custom schema in json format.
        :return: A lxml etree object that represents this PageXML object.
        """
        self.__changed = datetime.now().isoformat()
        if schema_file is not None:
            schema = PageSchema.custom(version, schema_file)
        else:
            schema = PageSchema.get(version)
        xsi_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        nsmap = {None: schema["xmlns"], "xsi": schema["xmlns_xsi"]}
        root = etree.Element( "PcGts", {xsi_qname: schema["xsi_schema_location"]}, nsmap=nsmap)
        # Metadata
        metadata = etree.SubElement(root, "Metadata")
        etree.SubElement(metadata, "Creator").text = self.__creator
        etree.SubElement(metadata, "Created").text = self.__created
        etree.SubElement(metadata, "LastChange").text = self.__changed
        # Page
        page = etree.Element("Page", **self.__attributes)
        root.append(page)
        # ReadingOrder
        if len(self.__reading_order) > 0:
            reading_order = etree.SubElement(page, "ReadingOrder")
            order_group = etree.SubElement(reading_order, "OrderedGroup", id="g0")  # does id matter?
            for i, rid in enumerate(self.__reading_order):
                etree.SubElement(order_group, "RegionRefIndexed", index=str(i), regionRef=rid)
        # Elements
        for element in self.__elements:
            page.append(element.to_etree())
        return root

    @classmethod
    def from_xml(cls, fp: Union[Path, str], encoding: str = "utf-8", skip_unknown: bool = False) -> Self:
        """
        Create a new PageXML object from a PageXML file.
        :param fp: Path of PageXML file.
        :param encoding: Set custom encoding.
        :param skip_unknown: Skip unknown elements.
        :return: PageXML object.
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        tree = etree.parse(fp, parser).getroot()
        return cls.from_etree(tree, skip_unknown=skip_unknown)

    def to_xml(self, fp: Union[Path, str], version: str = "2019", schema_file: Optional[Path] = None,
               encoding: str = "utf-8") -> None:
        """
        Create a PageXML file from a PageXML file.
        :param fp: Path to new PageXML file.
        :param version: The PageXML version to use. Currently supported: `2019`.
        :param schema_file: Custom schema in json format.
        :param encoding: Set custom encoding.
        """
        with open(fp, "wb") as f:
            tree = etree.tostring(self.to_etree(version, schema_file), pretty_print=True,
                                  encoding=encoding, xml_declaration=True)
            f.write(tree)

    def add_element(self, element: PageElement, index: Optional[int] = None, ro: bool = True) -> None:
        """
        Add an existing PageElement object to the list elements.
        :param element: The element to add.
        :param index: If set, insert the element at this index. Else append to the list.
        :param ro: If set to true, add the element to the reading order at the specified index.
            Only if the element is a region.
        """
        if index is None:
            self.__elements.append(element)
            if ro and element.is_region() and element.id:
                self.__reading_order.append(element.id)
        else:
            self.__elements.insert(min(index, len(self.__elements) - 1), element)
            if ro and element.is_region() and element.id:
                self.__reading_order.insert(min(index, len(self.__elements) - 1), element.id)

    def create_element(self, _type: PageType, index: Optional[int] = None,
                       ro: bool = True, **attributes: str) -> PageElement:
        """
        Create a new PageElement object and add it to the list of elements.
        :param _type: PageType of new element.
        :param index: If set, insert the new element at this index. Else append to the list.
        :param ro: If set to true, add the element to the reading order at the specified index.
            Only if the element is a region.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created Element object.
        """
        element = PageElement.new(_type, **attributes)
        self.add_element(element, index, ro)
        return element

    def get_attribute(self, key: str) -> Optional[str]:
        """
        Get an attribute.
        :param key: Key of attribute.
        """
        return self.__attributes.get(key, None)

    def set_attribute(self, key: str, value: Optional[str]) -> None:
        """
        Set or create an attribute.
        :param key: Key of attribute. Creates a new one if the key does not exist.
        :param value: Value for the attribute. Deletes the attribute of None is passed.
        """
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)

    def delete_attribute(self, key: str) -> Optional[str]:
        """
        Delete an attribute.
        :param key: The key to delete.
        :return: Returns the deleted attribute value. If the key does not exist, None is returned.
        """
        return self.__attributes.pop(str(key), None)

    def get_regions(self, region: Optional[Union[list[PageType], PageType]] = None) -> list[PageElement]:
        """
        Return a list of all direct child elements that are regions.
        :param region: Only select a specific region type or a set of region types.
        :return: List of matching PageElement objects.
        """
        if region is None:
            return list([e for e in self.__elements if e.is_region()])
        if isinstance(region, PageType):
            region = [region]
        return list([e for e in self.__elements if e.type in region])

    def remove_element(self, element: Union[PageElement, int]) -> Optional[PageElement]:
        """
        Remove an element from the list of elements.
        :param element: The PageElement object or the index of the element to remove.
        :return: The removed element, if it existed.
        """
        if isinstance(element, int) and element < len(self.__elements) - 1:
            return self.__elements.pop(element)
        elif isinstance(element, PageElement) and element in self.__elements:
            self.__elements.remove(element)
            return element
        return None

    def clear_elements(self) -> None:
        """Remove all PageElement objects from the list of elements."""
        self.__elements.clear()
        self.clear_reading_order()

    def find(self, type: PageType, recursive: bool = False) -> Optional[PageElement]:
        """
        Find the first element in the list of elements of a specified type.
        :param type: The PageType to search for.
        :param recursive: If set to true, search recursively.
        :return: The found object or None if it does not exist.
        """
        for element in self.__elements:
            if element.type == type:
                return element
            if recursive:
                if (res := element.find(type, recursive=True)) is not None:
                    return res
        return None

    def find_all(self, type: PageType, recursive: bool = False) -> list[PageElement]:
        """
        Find all elements in the list of elements of a specified type.
        :param type: The PageType to search for.
        :param recursive: If set to true, search recursively.
        :return: A list of found PageElement objects.
        """
        result: list[PageElement] = []
        for element in self.__elements:
            if element.type == type:
                result.append(element)
            if recursive:
                result.extend(element.find_all(type, recursive=True))
        return result

    def clear_regions(self) -> None:
        """Remove all PageElement objects from the list of elements, that are regions."""
        for element in self.__elements:
            if element.is_region():
                self.__elements.remove(element)
                if element.id and element.id in self.__reading_order:
                    self.__reading_order.remove(element.id)

    def clear_reading_order(self) -> None:
        """Reset the reading order."""
        self.__reading_order.clear()
