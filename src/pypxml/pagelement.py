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

from typing import TYPE_CHECKING, Self, Optional, Union

from lxml import etree

from .pagetype import PageType, is_region, is_valid
if TYPE_CHECKING:
    from .pagexml import PageXML


class PageElement:
    """
    PageXML Element class.
    """
    
    def __init__(self, pagetype: PageType, parent: Union["PageXML", Self], **attributes: str):
        """
        PLEASE USE THE .new() METHOD TO CREATE A NEW PAGEELEMENT OBJECT.
        This constructor is only for internal use.
        Args:
            pagetype: The type of the page element.
            parent: The parent element of the page element.
            attributes: Named arguments which represent the attributes of the `PageElement` object.
        """
        self.__pagetype: PageType = pagetype
        self.__parent: Union["PageXML", PageElement] = parent
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__elements: list[PageElement] = []
        self.__text: Optional[str] = None
        
    def __str__(self) -> str:
        """ Returns the string representation of the PageElement object. """
        return f"<PageElement ({self.__pagetype.value}) {self.__attributes}>"
    
    def __repr__(self) -> str:
        """ Returns the string representation of the PageElement object. """
        return self.__str__()
        
    def __len__(self) -> int:
        """ Returns the number elements in this element. """
        return len(self.__elements)
            
    def __iter__(self) -> Self:
        """ Iterate over all elements in this element. """
        self.__n = 0
        return self

    def __next__(self) -> Self:
        """ Yield next element. """
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration
    
    def __getitem__(self, key: Union[int, str]) -> Optional[Union[Self, str]]:
        """
        Get an PageElement object by its index or an attribute value by its key
        Args:
            key: Index (integer) of an PageElement object or a key (string) of an attribute.
        Returns:
            The PageElement of passed index (returns last object if the key is out of range) or the value of the
            selected attribute. Returns None, if no match was found.
        """
        if isinstance(key, int) and len(self.__elements) > 0:
            return self.__elements[min(key, len(self.__elements) - 1)]
        elif isinstance(key, str) and key in self.__attributes:
            return self.__attributes[key]
        return None

    def __setitem__(self, key: Union[int, str], value: Union[Self, str]) -> None:
        """
        Set an PageElement object or an attribute value.
        Args:
            key: Index (integer) for an PageElement object or a key (string) for an attribute.
            value: PageElement object (if key is of type integer) or a string (if key is of type string).
        """
        if isinstance(key, int) and isinstance(value, PageElement) and len(self.__elements) > 0:
            self.__elements[min(key, len(self.__elements) - 1)] = value
            if value.parent is not self:
                value._PageElement__parent = self
        elif isinstance(key, str):
            self.__attributes[key] = value
        else:
            raise ValueError("Invalid key or value")

    def __contains__(self, key: Union[Self, str]) -> bool:
        """
        Checks if an PageElement object or an attribute exists.
        Args:
            key: PageElement object or attribute key.
        Returns:
            True, if either the passed PageElement object or the attribute exists. Else return False.
        """
        if isinstance(key, PageElement):
            return key in self.__elements
        elif isinstance(key, str):
            return key in self.__attributes
        return False
    
    @property
    def pagetype(self) -> PageType:
        """ Get the type of the page element. """
        return self.__pagetype
    
    @pagetype.setter
    def pagetype(self, pagetype: PageType) -> None:
        """ Set the type of the page element. """
        if isinstance(pagetype, str):
            if not is_valid(pagetype):
                raise ValueError("Invalid PageXML element string.")
            self.__pagetype = PageType[pagetype]
        elif isinstance(pagetype, PageType):
            self.__pagetype = pagetype
        else:
            raise ValueError("Invalid PageXML element type.")
        
    @property
    def parent(self) -> Union["PageXML", Self]:
        """ Get the parent of the page element. """
        return self.__parent
    
    @property
    def attributes(self) -> dict[str, str]:
        """ Get the attributes of the page element. """
        return self.__attributes
    
    @attributes.setter
    def attributes(self, attributes: dict[str, str]) -> None:
        """ Set the attributes of the page element. """
        self.__attributes = {} if not attributes else {str(k): str(v) for k, v in attributes.items() if v is not None}
        
    @property
    def elements(self) -> list[Self]:
        """ Returns a copy of the elements list. """
        return self.__elements.copy()
    
    @property
    def text(self) -> Optional[str]:
        """ XML element text. """
        return self.__text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        """ XML element text. """
        self.__text = None if not value else str(value)
    
    @classmethod
    def new(cls, pagetype: PageType, parent: Optional[Union["PageXML", Self]] = None, **attributes: str) -> Self:
        """
        Create a new empty PageElement object.
        Args:
            creator: Set a custom PageXML `Metadata` creator. Defaults to "pypxml".
            parent: The parent element of the page element.
            attributes: Named arguments which represent the attributes of the `PageElement` object.
        Returns:
            A empty PageXML object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(pagetype, parent, **attributes)
    
    @classmethod
    def from_etree(cls, tree: etree.Element, parent: Union["PageXML", Self], skip_unknown: bool = False) -> Self:
        """
        Create a new PageElement object from an etree element.
        Args:
            tree: lxml etree object.
            parent: The parent element of this page element.
            skip_unknown: Skip unknown elements. Else raise ValueError. Defaults to False.
        Raises:
            ValueError: If the element is not a valid PageXML element and skip_unknown is False.
        Returns:
            PageElement object that represents the passed etree element.
        """
        pagetype = tree.tag.split("}")[1]
        if not is_valid(pagetype):
            if skip_unknown:
                return None
            raise ValueError(f"Invalid PageXML element: {pagetype}")
        element = cls.new(PageType[pagetype], parent, **dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.set_element(PageElement.from_etree(child, element, skip_unknown=skip_unknown))
        return element
    
    def to_etree(self) -> etree.Element:
        """
        Convert the PageElement object to an etree element.
        Returns:
            A lxml etree object that represents this PageElement object.
        """
        element = etree.Element(self.__pagetype.value, **self.__attributes)
        if self.__text is not None:
            element.text = self.__text
        for child in self.__elements:
            element.append(child.to_etree())
        return element
    
    def find_by_id(self, id: str, depth: int = 0) -> Optional[Self]:
        """
        Find an element by its id.
        Args:
            id: ID of the element to find.
            depth: Determines the depth of the search. `0` searches only the current level, `-1` searches all levels 
                   recursively and `>0` limits the search to that many levels deep.
        Returns:
            The PageElement object with the given ID. Returns None, if no match was found.
        """
        for element in self.__elements:
            if element.get_attribute("id") == id:
                return element
            if depth != 0:
                if (found := element.find_by_id(id, max(-1, depth - 1))) is not None:
                    return found
        return None
   
    def find_by_type(self, pagetype: Union[PageType, list[PageType]], depth: int = 0, **attributes: str) -> list[Self]:
        """
        Find all elements by their type.
        Args:
            pagetype: Type of the elements to find.
            depth: Determines the depth of the search. `0` searches only the current level, `-1` searches all levels 
                   recursively and `>0` limits the search to that many levels deep.
            attributes: Named arguments which represent the attributes that the elements must have.
        Returns:
            A list of PageElement objects with the given type. Returns an empty list, if no match was found.
        """
        if isinstance(pagetype, PageType):
            pagetype = [pagetype]
        found_elements: list[PageElement] = []
        for element in self.__elements:
            if element.pagetype in pagetype:
                if not attributes or all(element.get_attribute(str(k)) == str(v) for k, v in attributes.items()):
                    found_elements.append(element)
            if depth != 0:
                found_elements.extend(element.find_by_type(pagetype, max(-1, depth - 1), **attributes))
        return found_elements

    def create_element(self, pagetype: PageType, index: Optional[int] = None, **attributes: str) -> Self:
        """
        Create a new PageElement object and add it to the list of elements.
        Args:
            pagetype: PageType of the new PageElement object.
            index: If set, insert the new element at this index. Else append to the list. Defaults to None.
            attributes: Named arguments which represent the attributes of the `PageElement` object.
        Returns:
            The new PageElement object.
        """
        element = PageElement.new(pagetype, self, **attributes)
        self.set_element(element, index)
        return element

    def get_element(self, index: int) -> Optional[Self]:
        """
        Get an PageElement object by its index.
        Args:
            index: Index of the PageElement object.
        Returns:
            The PageElement object of passed index (returns None if the index is out of range).
        """
        if len(self.__elements) > 0 and index < len(self.__elements):
            return self.__elements[index]
        return None
    
    def set_element(self, element: Self, index: Optional[int] = None) -> None:
        """
        Add an existing PageElement object to the list of elements.
        Args:
            element: The PageElement to add.
            index: If set, insert the element at this index. Else append to the list. Defaults to None.
        """
        if index is None:
            self.__elements.append(element)
        else:
            self.__elements.insert(min(index, len(self.__elements) - 1), element)
        if element.parent is not self:
            element._PageElement__parent = self
        
    def remove_element(self, element: Union[Self, int]) -> Optional[Self]:
        """
        Remove an element from the list of elements.
        Args:
            element: The PageElement or the index of the PageElement to remove.
        Returns:
            The removed element, if it was found. Else None.
        """
        if isinstance(element, int) and element < len(self.__elements) - 1:
            return self.__elements.pop(element)
        elif isinstance(element, PageElement) and element in self.__elements:
            self.__elements.remove(element)
            return element
        return None
    
    def clear_elements(self) -> None:
        """ Remove all elements from the list of elements. This will not remove the element itself. """
        self.__elements.clear() 
    
    def get_attribute(self, key: str) -> Optional[str]:
        """
        Get an attribute value by its key.
        Args:
            key: Key of the attribute.
        Returns:
            The value of the attribute. Returns None, if no match was found.
        """
        return self.__attributes.get(key, None)
    
    def set_attribute(self, key: str, value: Optional[str]) -> None:
        """
        Set an attribute value.
        Args:
            key: Key of the attribute. Creates a new attribute if it does not exist.
            value: Value of the attribute. If None, remove the attribute.
        """
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)
    
    def remove_attribute(self, key: str) -> Optional[str]:
        """
        Remove an attribute by its key.
        Args:
            key: Key of the attribute.
        Returns:
            The value of the removedattribute. Returns None, if no match was found.
        """
        return self.__attributes.pop(str(key), None)
    
    def clear_attributes(self) -> None:
        """ Remove all attributes from the PageElement object. """
        self.__attributes = {}
    
    def is_region(self) -> bool:
        """
        Check if the page element is a region.
        Returns:
            True, if the page element is a region. Else return False.
        """
        return is_region(self.__pagetype)
    