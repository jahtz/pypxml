# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from typing import Optional, Union, Self

from lxml import etree

from .element import Element
from .resources.xml_types import XMLType


class Page:
    """ Represents a page of a PageXML file. """
    def __init__(self, attributes: Optional[dict[str, str]] = None):
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__reading_order: list[str] = []  # region id's
        self.__elements: list[Element] = []

    def __len__(self) -> int:
        """ Returns the number of elements. """
        return len(self.__elements)

    def __iter__(self) -> Self:
        """ Iterator: starting point for iterating over all elements that are regions. """
        self.__n = 0
        self.__regions = [element for element in self.__elements if element.is_region()]
        return self

    def __next__(self) -> Element:
        """ Iterator: yield next element that is a region. """
        if self.__n < len(self.__regions):
            self.__n += 1
            return self.__regions[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[Element, str]]:
        """
        Get an Element object by its index or an attribute value by its key
        :param key: Index (integer) of an Element object or a key (string) of an attribute.
        :return: The Element of passed index (returns last object if the key is out of range) or the value of the
            selected attribute. Returns None, if no match was found.
        """
        if isinstance(key, int) and len(self.__elements) > 0:
            return self.__elements[min(key, len(self.__elements) - 1)]
        elif isinstance(key, str) and key in self.__attributes:
            return self.__attributes[key]
        return None

    def __setitem__(self, key: Union[int, str], value: Union[Element, str]) -> None:
        """
        Set an Element object or an attribute value.
        :param key: Index (integer) for an Element object or a key (string) for an attribute.
        :param value: Element object (if key is of type integer) or a string (if key is of type string).
        """
        if isinstance(key, int) and isinstance(value, Element) and len(self.__elements) > 0:
            self.__elements[min(key, len(self.__elements) - 1)] = value
        elif isinstance(key, str):
            self.__attributes[key] = value
        else:
            raise ValueError('Invalid key or value')

    def __contains__(self, key: Union[Element, str]) -> bool:
        """
        Checks if an Element object or an attribute exists.
        :param key: Element object or attribute key.
        :return: True, if either the passed Element object or the attribute exists. Else return False.
        """
        if isinstance(key, Element):
            return key in self.__elements
        elif isinstance(key, str):
            return key in self.__attributes
        return False

    @property
    def attributes(self) -> dict[str, str]:
        return self.__attributes

    @property
    def reading_order(self) -> list[str]:
        return self.__reading_order

    @property
    def elements(self) -> list[Element]:
        return self.__elements

    @property
    def regions(self) -> list[Element]:
        return list([element for element in self.__regions if element.is_region()])

    @property
    def image_filename(self) -> Optional[str]:
        return self.__attributes.get('imageFilename', None)

    @image_filename.setter
    def image_filename(self, filename: Optional[str]) -> None:
        if filename is None:
            self.__attributes.pop('imageFilename', None)
        else:
            self.__attributes['imageFilename'] = str(filename)

    @property
    def width(self) -> Optional[int]:
        if (w := self.__attributes.get('imageWidth', None)) is not None:
            return int(w)
        return None

    @property
    def height(self) -> Optional[int]:
        if (h := self.__attributes.get('imageHeight', None)) is not None:
            return int(h)
        return None

    @classmethod
    def new(cls, **attributes: str) -> Self:
        """
        Create a new Page object from scratch.
        :param attributes: Named arguments that will be stored as attributes.
        :return: The newly created Page object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """
        Create a new Page object from a lxml etree object.
        :param tree: lxml etree object.
        :return: Page object that represents the passed etree object.
        """
        page = cls(dict(tree.items()))
        if (ro := tree.find('./{*}ReadingOrder')) is not None:
            if (ro_elements := tree.findall('../{*}RegionRefIndexed')) is not None:
                page._ro = list([i.get('regionRef') for i in sorted(list(ro_elements), key=lambda i: i.get('index'))])
            tree.remove(ro)
        for element in tree:
            page.add_element(Element.from_etree(element), ro=False)
        return page

    def to_etree(self) -> etree.Element:
        """
        Convert the Page object to a lxml etree object.
        :return: A lxml etree object that represents this Page object.
        """
        page = etree.Element('Page', **self.__attributes)
        if len(self.__reading_order) > 0:
            reading_order = etree.SubElement(page, 'ReadingOrder')
            order_group = etree.SubElement(reading_order, 'OrderedGroup', id='g0')  # does id matter?
            for i, rid in enumerate(self.__reading_order):
                etree.SubElement(order_group, 'RegionRefIndexed', index=str(i), regionRef=rid)
        for element in self.__elements:
            page.append(element.to_etree())
        return page

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

    def get_regions(self, region: Optional[XMLType] = None) -> list[Element]:
        """
        Return a list of all direct child elements that are regions.
        :param region: Only select a specific region type.
        :return: List of matching Element objects.
        """
        if region is None:
            return list([e for e in self.__elements if e.is_region()])
        return list([e for e in self.__elements if e.type == region])

    def add_element(self, element: Element, index: Optional[int] = None, ro: bool = True) -> None:
        """
        Add an existing Element object to the list elements.
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

    def create_element(self, _type: XMLType, index: int = None, ro: bool = True, **attributes: str) -> Element:
        """
        Create a new Element object and add it to the list of elements.
        :param _type: XMLType of new element.
        :param index: If set, insert the new element at this index. Else append to the list.
        :param ro: If set to true, add the element to the reading order at the specified index.
            Only if the element is a region.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created Element object.
        """
        element = Element.new(_type, **attributes)
        self.add_element(element, index, ro)
        return element

    def remove_element(self, element: Union[Element, int]) -> Optional[Element]:
        """
        Remove an element from the list of elements.
        :param element: The Element object or the index of the element to remove.
        :return: The removed element, if it existed.
        """
        if isinstance(element, int) and element < len(self.__elements) - 1:
            return self.__elements.pop(element)
        elif isinstance(element, Element) and element in self.__elements:
            self.__elements.remove(element)
            return element
        return None

    def clear_elements(self) -> None:
        """ Remove all Element objects from the list of elements. """
        self.__elements.clear()
        self.clear_reading_order()

    def clear_regions(self) -> None:
        """ Remove all Element objects from the list of elements, that are regions. """
        for element in self.__elements:
            if element.is_region():
                self.__elements.remove(element)
                if element.id and element.id in self.__reading_order:
                    self.__reading_order.remove(element.id)

    def clear_reading_order(self) -> None:
        """ Reset the reading order. """
        self.__reading_order.clear()
