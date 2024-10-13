# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from typing import Optional, Union, Self

from lxml import etree

from .resources.xml_types import XMLType


class Element:
    def __init__(self, _type: XMLType, attributes: Optional[dict[str, str]] = None):
        self.__type: XMLType = _type
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__elements: list[Element] = []
        self.__text: Optional[str] = None

    def __len__(self) -> int:
        """ Returns the number of elements. """
        return len(self.__elements)

    def __iter__(self) -> Self:
        """ Iterator: starting point for iterating over all elements. """
        self.__n = 0
        return self

    def __next__(self) -> Self:
        """ Iterator: yield next element. """
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[Self, str]]:
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

    def __setitem__(self, key: Union[int, str], value: Union[Self, str]) -> None:
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

    def __contains__(self, key: Union[Self, str]) -> bool:
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
    def type(self) -> XMLType:
        return self.__type

    @type.setter
    def type(self, value: XMLType) -> None:
        self.__type = value

    @property
    def attributes(self) -> dict[str, str]:
        return self.__attributes

    @property
    def elements(self) -> list[Self]:
        return self.__elements

    @property
    def id(self) -> Optional[str]:
        return self.__attributes.get('id', None)

    @id.setter
    def id(self, value: Optional[str]) -> None:
        if value is None:
            self.__attributes.pop('id', None)
        else:
            self.__attributes['id'] = value

    @property
    def text(self) -> Optional[str]:
        return self.__text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        self.__text = None if value is None else str(value)

    @classmethod
    def new(cls, _type: XMLType, **attributes: str) -> Self:
        """
        Create a new Element object from scratch.
        :param _type: The type of element to create.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created Element object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(_type, attributes)

    @classmethod
    def from_etree(cls, tree: etree.Element) -> Self:
        """
        Create a new Element object from a lxml etree object.
        :param tree: lxml etree object.
        :return: Element object that represents the passed etree object.
        """
        element = cls(XMLType(tree.tag.split('}')[1]), dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.add_element(Element.from_etree(child))
        return element

    def to_etree(self) -> etree.Element:
        """
        Convert the Element object to a lxml etree object.
        :return: A lxml etree object that represents this Element object.
        """
        element = etree.Element(self.__type.value, **self.__attributes)
        if self.__text is not None:
            element.text = self.__text
        for child in self.__elements:
            element.append(child.to_etree())
        return element

    def is_region(self) -> bool:
        """ Returns True, if the Element object is a region. """
        return self.__type.value.endswith('Region')

    def contains_text(self) -> bool:
        """ Returns True, if the Element object contains text. """
        return self.__text is not None

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
        """ Return the first direct child Element object of type Coords. """
        for element in self.__elements:
            if element.type == XMLType.Coords:
                return element
        return None

    def get_baseline(self) -> Optional[Self]:
        """ Return the first direct child Element object of type Baseline. """
        for element in self.__elements:
            if element.type == XMLType.Baseline:
                return element
        return None

    def add_element(self, element: Self, index: Optional[int] = None) -> None:
        """
        Add an existing Element object to the list elements.
        :param element: The element to add.
        :param index: If set, insert the element at this index. Else append to the list.
        """
        if index is None:
            self.__elements.append(element)
        else:
            self.__elements.insert(min(index, len(self.__elements) - 1), element)

    def create_element(self, _type: XMLType, index: int = None, **attributes: str) -> Self:
        """
        Create a new Element object and add it to the list of elements.
        :param _type: XMLType of new element.
        :param index: If set, insert the new element at this index. Else append to the list.
        :param attributes: Named arguments that will be stores as xml attributes.
        :return: The newly created Element object.
        """
        element = Element.new(_type, **attributes)
        self.add_element(element, index)
        return element

    def remove_element(self, element: Union[Self, int]) -> Optional[Self]:
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
