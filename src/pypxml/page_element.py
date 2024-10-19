# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from typing import Optional, Union, Self

import lxml.etree

from .page_types import PageType


class PageElement:
    def __init__(self, _type: PageType, **attributes: str) -> None:
        """
        Please use the .new() constructor.
        :param _type: PageType of this PageElement.
        :param attributes: Attributes of this PageElement.
        """
        self.__type: PageType = _type
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__elements: list[PageElement] = []
        self.__text: Optional[str] = None

    def __len__(self):
        """Returns the number of sub elements."""
        return len(self.__elements)

    def __iter__(self) -> Self:
        """Iterator: starting point for iterating over all elements."""
        self.__n = 0
        return self

    def __next__(self) -> Self:
        """Iterator: yield next element."""
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[Self, str]]:
        """
        Get an PagElement object by its index or an attribute value by its key
        :param key: Index (integer) of an PagElement object or a key (string) of an attribute.
        :return: The PagElement of passed index (returns last object if the key is out of range) or the value of the
            selected attribute. Returns None, if no match was found.
        """
        if isinstance(key, int) and len(self.__elements) > 0:
            return self.__elements[min(key, len(self.__elements) - 1)]
        elif isinstance(key, str) and key in self.__attributes:
            return self.__attributes[key]
        return None

    def __setitem__(self, key: Union[int, str], value: Union[Self, str]) -> None:
        """
        Set an PagElement object or an attribute value.
        :param key: Index (integer) for an PagElement object or a key (string) for an attribute.
        :param value: PagElement object (if key is of type integer) or a string (if key is of type string).
        """
        if isinstance(key, int) and isinstance(value, PageElement) and len(self.__elements) > 0:
            self.__elements[min(key, len(self.__elements) - 1)] = value
        elif isinstance(key, str):
            self.__attributes[key] = value
        else:
            raise ValueError("Invalid key or value")

    def __contains__(self, key: Union[Self, str]) -> bool:
        """
        Checks if an PagElement object or an attribute exists.
        :param key: PagElement object or attribute key.
        :return: True, if either the passed PagElement object or the attribute exists. Else return False.
        """
        if isinstance(key, PageElement):
            return key in self.__elements
        elif isinstance(key, str):
            return key in self.__attributes
        return False

    @property
    def type(self) -> PageType:
        """Type of this PageElement object."""
        return self.__type

    @type.setter
    def type(self, value: PageType) -> None:
        """Type of this PageElement object."""
        self.__type = value

    @property
    def attributes(self) -> dict[str, str]:
        """List of all attributes."""
        return self.__attributes

    @property
    def elements(self) -> list[Self]:
        """List of all elements."""
        return self.__elements

    @property
    def id(self) -> Optional[str]:
        """ID attribute."""
        return self.__attributes.get("id", None)

    @id.setter
    def id(self, value: Optional[str]) -> None:
        """ID attribute."""
        if value is None:
            self.__attributes.pop("id", None)
        else:
            self.__attributes["id"] = value

    @property
    def text(self) -> Optional[str]:
        """XML element text."""
        return self.__text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        """XML element text."""
        self.__text = None if value is None else str(value)

    @classmethod
    def new(cls, _type: PageType, **attributes: str) -> Self:
        """
        Create a new PageElement object from scratch.
        :param _type: The type of page element to create.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created PageElement object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(_type, **attributes)

    @classmethod
    def from_etree(cls, tree: lxml.etree.Element) -> Self:
        """
        Create a new PageElement object from a lxml etree object.
        :param tree: lxml etree object.
        :return: PageElement object that represents the passed etree object.
        """
        element = cls(PageType(tree.tag.split("}")[1]), **dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.add_element(PageElement.from_etree(child))
        return element

    def to_etree(self) -> lxml.etree.Element:
        """
        Convert the PageElement object to a lxml etree object.
        :return: A lxml etree object that represents this PageElement object.
        """
        element = lxml.etree.Element(self.__type.value, **self.__attributes)
        if self.__text is not None:
            element.text = self.__text
        for child in self.__elements:
            element.append(child.to_etree())
        return element

    def is_region(self) -> bool:
        """Returns True, if the Element object is a region."""
        return self.__type.value.endswith("Region")

    def get_attribute(self, key: str) -> Optional[str]:
        """
        Get an attribute.
        :param key: Key of attribute.
        """
        return self.__attributes.get(key, None)

    def set_attribute(self, key: str, value: Optional[str]) -> None:
        """
        Set an attribute.
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

    def get_coords(self) -> Optional[Self]:
        """Return the first direct child PageElement object of type Coords."""
        for element in self.__elements:
            if element.type == PageType.Coords:
                return element
        return None

    def get_baseline(self) -> Optional[Self]:
        """Return the first direct child PageElement object of type Baseline."""
        for element in self.__elements:
            if element.type == PageType.Baseline:
                return element
        return None

    def add_element(self, element: Self, index: Optional[int] = None) -> None:
        """
        Add an existing PageElement object to the list elements.
        :param element: The element to add.
        :param index: If set, insert the element at this index. Else append to the list.
        """
        if index is None:
            self.__elements.append(element)
        else:
            self.__elements.insert(min(index, len(self.__elements) - 1), element)

    def create_element(self, _type: PageType, index: Optional[int] = None, **attributes: str) -> Self:
        """
        Create a new PageElement object and add it to the list of elements.
        :param _type: PageType of new element.
        :param index: If set, insert the new element at this index. Else append to the list.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created PageElement object.
        """
        element = PageElement.new(_type, **attributes)
        self.add_element(element, index)
        return element

    def remove_element(self, element: Union[Self, int]) -> Optional[Self]:
        """
        Remove an element from the list of elements.
        :param element: The PagElement object or the index of the element to remove.
        :return: The removed element, if it existed.
        """
        if isinstance(element, int) and element < len(self.__elements) - 1:
            return self.__elements.pop(element)
        elif isinstance(element, PageElement) and element in self.__elements:
            self.__elements.remove(element)
            return element
        return None

    def clear_elements(self) -> None:
        """Remove all PagElement objects from the list of elements."""
        self.__elements.clear()
