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

import logging
from typing import TYPE_CHECKING, Self, Optional, Union, Literal

from lxml import etree

from .pagetype import PageType
if TYPE_CHECKING:
    from .pagexml import PageXML
   
 
logger = logging.getLogger("pagexml")
    
    
class PageElement:
    """
    Represents a PageXML element within the "Page" element.
    """
    
    def __init__(self, pagetype: PageType, parent: Union["PageXML", Self], **attributes: str) -> Self:
        """
        Creates a new empty PageElement object.
        Args:
            pagetype: The type of the PageElement.
            parent: The parent element of the page element.
            attributes: Named arguments that represent the attributes of the "PageElement" object.
        Returns:
            An empty PageElement object.
        """
        if parent.__class__.__name__ not in ("PageXML", "PageElement"):  # PageXML is not imported at runtime
            raise TypeError(f"Expected a PageXML or PageElement for parent, got {type(parent).__name__}")
        self.__parent: Union["PageXML", PageElement] = parent
        self.__elements: list[PageElement] = []
        self.__text: Optional[str] = None
        
        self.pagetype = pagetype
        self.attributes = attributes
        
    def __repr__(self) -> str:
        """ Returns a text representation of the object for debugging. """
        return (f"PageElement(pagetype={self.__pagetype}, attributes={str(self.__attributes)}, "
                f"childs={len(self.__elements)}, text={self.__text})")
        
    def __str__(self) -> str:
        """ Returns a text representation of the object for printing. """
        return f"<PageElement ({self.__pagetype})>"
    
    def __len__(self) -> int:
        """ Returns the number of child elements of this object. """
        return len(self.__elements)
    
    def __iter__(self) -> Self:
        """ Iterates over all child elements of this object. """
        self.__n = 0
        return self

    def __next__(self) -> Self:
        """ Yields the next element. """
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration
        
    def __getitem__(self, key: str) -> Optional[str]:
        """
        Gets an attribute value by its key.
        Args:
            key: The key of an attribute.
        Returns:
            The value of the selected attribute. Returns None if no match is found.
        """
        return self.__attributes.get(str(key), None)

    def __setitem__(self, key: str, value: Optional[str]) -> None:
        """
        Sets an attribute value.
        Args:
            key: The key of the attribute.
            value: The value of the attribute. If the value is None, the attribute is removed.
        """
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)

    def __contains__(self, key: Union[Self, str]) -> bool:
        """
        Checks if a child element or an attribute exists.
        Args:
            key: A child element or attribute key.
        Returns:
            True if the passed child element or attribute exists.
        """
        if isinstance(key, PageElement):
            return key in self.__elements
        else:
            return str(key) in self.__attributes
    
    @property
    def pagetype(self) -> PageType:
        """ The type of the PageElement object. """
        return self.__pagetype
    
    @pagetype.setter
    def pagetype(self, pagetype: Union[PageType, str]) -> None:
        """ Sets the type of the PageElement object. """
        if isinstance(pagetype, str):
            if not PageType.is_valid(pagetype):
                raise ValueError(f"Invalid PageType string: {pagetype}")
            self.__pagetype = PageType[pagetype]
        elif isinstance(pagetype, PageType):
            self.__pagetype = pagetype
        else:
            raise TypeError(f"Expected a PageType or string, got {type(pagetype).__name__}")
        
    @property
    def is_region(self) -> bool:
        """ Checks if the PageElement object is a region. """
        return self.__pagetype.is_region
    
    @property
    def parent(self) -> Union["PageXML", Self]:
        """ The parent of the PageElement object. This may be a PageXML or PageElement object. """
        return self.__parent
    
    @property
    def attributes(self) -> dict[str, str]:
        """ A dictionary containing key/value pairs that represent XML attributes. """
        return self.__attributes
    
    @attributes.setter
    def attributes(self, attributes: Optional[dict[str, str]]) -> None:
        """ Sets the dictionary containing key/value pairs that represent XML attributes. """
        self.__attributes = {} if attributes is None else {str(k): str(v) 
                                                           for k, v in attributes.items() if v is not None}
        
    @property
    def elements(self) -> list[Self]:
        """ Returns a copy of the list of child elements. """
        return self.__elements.copy()
        
    @property
    def text(self) -> Optional[str]:
        """ The stored text. """
        return self.__text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        """ Sets the stored text. """
        self.__text = None if value is None else str(value)
        
    @classmethod
    def from_etree(cls, tree: etree.Element, parent: Union["PageXML", Self], raise_on_error: bool = True) -> Self:
        """
        Creates a new PageElement object from an etree element.
        Args:
            tree: An lxml etree object.
            parent: The parent element of this page element.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Raises:
            ValueError: If the element is not a valid PageXML element and raise_on_error is True.
        Returns:
            A PageElement object that represents the passed etree element.
        """
        pagetype = tree.tag.split("}")[1]
        if not PageType.is_valid(pagetype):
            if not raise_on_error:
                logger.warning(f"Skipping unknown element: {pagetype}")
                return None
            raise ValueError(f"Could not parse unknown element: {pagetype}")
        element = cls(PageType[pagetype], parent, **dict(tree.items()))
        element.text = tree.text
        for child in tree:
            element.set_element(PageElement.from_etree(child, element, raise_on_error=raise_on_error))
        return element
        
    def to_etree(self) -> etree.Element:
        """
        Converts the PageElement object to an etree element.
        Returns:
            An lxml etree object that represents this PageElement object.
        """
        element = etree.Element(self.__pagetype.value, **self.__attributes)
        if self.__text is not None:
            element.text = self.__text
        for child in self.__elements:
            element.append(child.to_etree())
        return element
    
    def find_by_id(self, id: str, depth: int = 0) -> Optional[Self]:
        """
        Finds a child element by its ID.
        Args:
            id: The ID of the element to find.
            depth: The depth level of the search. 
                "0" searches only the current level. 
                "-1" searches all levels recursively (no depth limit). 
                ">0" limits the search to the specified number of levels deep.
        Returns:
            The PageElement object with the given ID. Returns None if no match is found.
        """
        for element in self.__elements:
            if element["id"] == id:
                return element
            if depth != 0:
                if (found := element.find_by_id(id, max(-1, depth - 1))) is not None:
                    return found
        return None
    
    def find_by_type(self, pagetype: Union[PageType, list[PageType]], depth: int = 0, **attributes: str) -> list[Self]:
        """
        Finds elements by their type.
        Args:
            pagetype: The type of the elements to find.
            depth: The depth level of the search. 
                "0" searches only the current level. 
                "-1" searches all levels recursively (no depth limit). 
                ">0" limits the search to the specified number of levels deep.
            attributes: Named arguments representing the attributes that the found elements must have.
        Returns:
            A list of PageElement objects with the given type. Returns an empty list if no match is found.
        """
        if isinstance(pagetype, PageType):
            pagetype = [pagetype]
        results: list[PageElement] = []
        for element in self.__elements:
            if element.pagetype in pagetype:
                if not attributes or all(element[str(k)] == str(v) for k, v in attributes.items() if v is not None):
                    results.append(element)
            if depth != 0:
                results.extend(element.find_by_type(pagetype, max(-1, depth - 1), **attributes))
        return results
    
    def find_coords(self) -> Optional[Self]:
        """
        Finds the coords element of the current element.
        Returns:
            The PageType.Coords element of the current object if it exists as a direct child.
        """
        if self.pagetype == PageType.Coords:
            return self
        elif (coords := self.find_by_type(PageType.Coords, depth=0)):
            return coords[0]
        return None
    
    def find_baseline(self) -> Optional[Self]:
        """
        Finds the baseline element of the current element.
        Returns:
            The PageType.Baseline element of the current object if it exists as a direct child.
        """
        if self.pagetype == PageType.Baseline:
            return self
        elif (baselines := self.find_by_type(PageType.Baseline, depth=0)):
            return baselines[0]
        return None
    
    def find_text(self, index: Optional[int] = None, 
                  source: Literal[PageType.Unicode, PageType.PlainText] = PageType.Unicode) -> Optional[str]:
        """
        Finds the text of the current element.
        Args:
            index: Selects a certain TextEquiv element index. If index is not set and multiple TextEquiv elements are 
                found, the first one with the lowest or no index is picked. Only applied if the current element is 
                a level above the TextEquivs.
            source: Selects whether the text from Unicode or PlainText is picked.
        Returns:
            The text of the current element if it was found.
        """
        if self.pagetype in [PageType.Unicode, PageType.PlainText]:
            return self.text
        if self.pagetype == PageType.TextEquiv:
            textequivs = [self]
        else:
            textequivs = self.find_by_type(PageType.TextEquiv, depth=0, index=index)
        if len(textequivs) > 1:
            logger.warning("Multiple TextEquiv elements found. Selecting the element with the lowest index")
            textequivs.sort(key = lambda x: -1 if "index" not in x else int(x["index"]))
        if textequivs and (textelement := textequivs[0].find_by_type(source, depth=0)):
            return textelement[0].text
        return None
        
    def create_element(self, pagetype: PageType, index: Optional[int] = None, **attributes: str) -> Self:
        """
        Creates a new child element and adds it to the list of elements.
        Args:
            pagetype: The PageType of the new child element.
            index: If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
            attributes: Named arguments that represent the attributes of the "PageElement" object.
        Returns:
            The newly created child element.
        """
        element = PageElement(pagetype, self, **attributes)
        self.set_element(element, index)
        return element
    
    def set_element(self, element: Self, index: Optional[int] = None) -> None:
        """
        Adds an existing PageElement object to the list of child elements.
        Args:
            element: The PageElement to add as a child element.
            index: If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.
        """
        self.__elements.insert(index if index is not None else len(self.__elements), element)
        if element.parent is not self:
            element._PageElement__parent = self
    
    def delete_element(self, element: Self) -> Optional[Self]:
        """
        Removes an element from the list of child elements.
        Args:
            element: The PageElement to remove.
        Returns:
            The removed element if it was found. Otherwise, None.
        """
        if element in self.__elements:
            self.__elements.remove(element)
            return element
        return None
    
    def clear_elements(self) -> None:
        """ Removes all elements from the list of child elements. """
        self.__elements.clear()
