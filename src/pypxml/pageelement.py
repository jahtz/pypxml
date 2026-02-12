# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from lxml import etree

if TYPE_CHECKING:
    from .pagexml import PageXML
from .pagetypes import PageType


logger = logging.getLogger(__name__)


class PageElement:
    """
    Represents a single structural element within a PAGE-XML document.

    A `PageElement` models one XML element inside the PAGE hierarchy (e.g. regions,
    text lines, text equivalents, coordinates, baselines, etc.). 
    
    Each element:

    - Has a well-defined `PageType` corresponding to its PAGE-XML tag
    - Stores XML attributes and optional textual content
    - Can contain nested child `PageElement` objects, forming a tree structure
    - Maintains a reference to its parent (`PageXML` or another `PageElement`)
    - Supports recursive search by ID, type, and attributes
    - Can be parsed from and serialized back to lxml etree elements

    `PageElement` is the fundamental building block of the PAGE-XML object model and
    is used to represent both layout regions and their associated content in a
    uniform, hierarchical way.
    """
    
    def __init__(
        self,
        pagetype: PageType,
        parent: PageXML | PageElement,
        **attributes: str
    ) -> None:
        """
        Create a new empty `PageElement` object.
        Args:
            pagetype: The type of the element.
            parent: The parent of the element.
            attributes: Named arguments that represent the attributes of the element.
        Returns:
            An empty `PageElement` object.
        """
        if type(parent).__name__ not in {'PageXML', 'PageElement'}: 
            raise TypeError(f'Expected a PageXML or PageElement parent object, got {type(parent).__name__}')
        self.__parent: PageXML | PageElement = parent

        self.pagetype: PageType = pagetype
        self.attributes: dict[str, str] = attributes
        
        self.__elements: list[PageElement] = []
        self.__text: str | None = None    
        
    def __str__(self) -> str:
        return repr(self)
    
    def __repr__(self) -> str:
        s = f'{self.pagetype.value} {str(self.__attributes)}'
        if self.__text:
            s += f' (\'{self.__text}\')'
        return s
    
    def __len__(self) -> int:
        return len(self.__elements)
    
    def __iter__(self) -> PageElement:
        self.__n = 0
        return self

    def __next__(self) -> PageElement:
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration

    def __getitem__(self, key: str) -> str | None:
        return self.__attributes.get(str(key), None)

    def __setitem__(self, key: str, value: str | None) -> None:
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)
            
    def __contains__(self, key: PageElement | str) -> bool:
        if isinstance(key, PageElement):
            return key in self.__elements
        else:
            return str(key) in self.__attributes
        
    @property
    def pagetype(self) -> PageType:
        """
        The type of the `PageElement` object.
        """
        return self.__pagetype
    
    @pagetype.setter
    def pagetype(self, pagetype: PageType | str) -> None:
        """
        The type of the `PageElement` object.
        """
        if isinstance(pagetype, str):
            if not PageType.is_valid(pagetype):
                raise ValueError(f'Invalid PageType string: {pagetype}')
            self.__pagetype = PageType[pagetype]
        elif isinstance(pagetype, PageType):
            self.__pagetype = pagetype
        else:
            raise TypeError(f'Expected a PageType or string, got {type(pagetype).__name__}')
        
    @property
    def is_region(self) -> bool:
        """
        Check if the `PageElement` object is a region.
        """
        return self.__pagetype.is_region
    
    @property
    def parent(self) -> PageXML | PageElement:
        """
        The parent of the `PageElement` object. This may be a `PageXML` or `PageElement` object.
        """
        return self.__parent
    
    @property
    def attributes(self) -> dict[str, str]:
        """
        A dictionary (copy) containing key/value pairs that represent XML attributes.
        """
        return self.__attributes.copy()
    
    @attributes.setter
    def attributes(self, attributes: dict[str, str] | None) -> None:
        """
        Sets the dictionary containing key/value pairs that represent XML attributes. 
        """
        self.__attributes = {} if attributes is None else {
            str(k): str(v) for k, v in attributes.items() if v is not None
        }
        
    @property
    def elements(self) -> list[PageElement]:
        """
        A copy of the list of child elements.
        """
        return self.__elements.copy()
        
    @property
    def text(self) -> str | None:
        """
        The stored text.
        """
        return self.__text

    @text.setter
    def text(self, value: str | None) -> None:
        """ 
        Store a text. If set to None, the text is deleted
        """
        self.__text = None if value is None else str(value)
        
    @classmethod
    def _from_etree(
        cls, 
        tree: etree.Element, 
        parent: PageXML | PageElement, 
        raise_on_error: bool = True
    ) -> PageElement:
        """
        Create a new `PageElement` object from a lxml etree element.
        Args:
            tree: The lxml etree element.
            parent: The parent of this element.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Raises:
            ValueError: If the element is not a valid PAGE-XML and raise_on_error is True.
        Returns:
            A `PageElement` object that represents the passed etree element.
        """
        pagetype = tree.tag.split('}')[1]
        if not PageType.is_valid(pagetype):
            if not raise_on_error:
                logger.warning(f'Skipping invalid element: {pagetype}')
                return None
            raise ValueError(f'Invalid element: {pagetype}')
        element = cls(PageType[pagetype], parent, **dict(tree.items()))
        element.text = tree.text
        for child in tree:
            if (pe := PageElement._from_etree(child, element, raise_on_error=raise_on_error)) is not None:
                element.set(pe)
        return element
    
    def _to_etree(self) -> etree.Element:
        """
        Convert the `PageElement` object to a lxml etree element.
        Returns:
            An lxml etree object that represents this object with all its childs.
        """
        element = etree.Element(self.__pagetype.value, **self.__attributes)
        if self.__text is not None:
            element.text = self.__text
        for child in self.__elements:
            element.append(child._to_etree())
        return element
    
    def find_all(
        self,
        id: str | list[str] | None = None,
        pagetype: PageType | list[PageType] | None = None,
        depth: int = 0,
        **attributes: str
    ) -> list[PageElement]:
        """
        Find `PageElements` by their type, id and attributes.
        Args:
            id: One or more element IDs to look for. If not set, no ID filter is applied.
            pagetype: One or more element types to look for. If not set, no type filter is applied.
            depth: The depth level of the search. 
                - "0" (default) searches only the current level. 
                - "-1" searches all levels recursively (no depth limit, may be slow). 
                - ">0" limits the search to the specified number of levels deep.
            attributes: Named arguments representing the attributes that the found elements must have.
                If not set, no attribute filter is applied
        Returns:
            A (possibly empty) list of found `PageElements`
        """
        if isinstance(id, str):
            id = [id]
        if isinstance(pagetype, PageType):
            pagetype = [pagetype]
            
        results: list[PageElement] = []
        for element in self.__elements:
            if (not pagetype or element.pagetype in pagetype) and \
               (not id or element['id'] in id) and \
               (not attributes or all(element[str(k)] == str(v) for k, v in attributes.items() if v is not None)):
                results.append(element)
            if depth != 0:
                results.extend(element.find_all(id, pagetype, max(-1, depth - 1), **attributes))
        return results
    
    def find(
        self,
        id: str | list[str] | None = None,
        pagetype: PageType | list[PageType] | None = None,
        depth: int = 0,
        **attributes: str
    ) -> PageElement | None:
        """
        Find a `PageElement` by their type, id and attributes.
        Args:
            id: One or more element IDs to look for. If not set, no ID filter is applied.
            pagetype: One or more element types to look for. If not set, no type filter is applied.
            depth: The depth level of the search. 
                - "0" (default) searches only the current level. 
                - "-1" searches all levels recursively (no depth limit, may be slow). 
                - ">0" limits the search to the specified number of levels.
            attributes: Named arguments representing the attributes that the found elements must have.
                If not set, no attribute filter is applied
        Returns:
            The first found `PageElement` or None if no match was found.
        """
        matches = self.find_all(id=id, pagetype=pagetype, depth=depth, **attributes)
        return matches[0] if matches else None

    def create(self, pagetype: PageType, i: int | None = None, **attributes: str) -> PageElement:
        """
        Create a new child `PageElement` and add it to the list of elements.
        Args:
            pagetype: The PageType of the new child element.
            i: If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
            attributes: Named arguments that represent the attributes of the child object.
        Returns:
            The newly created `PageElement` child object.
        """
        element = PageElement(pagetype, self, **attributes)
        self.set(element, i)
        return element
    
    def set(self, element: PageElement, i: int | None = None) -> None:
        """
        Adds an existing `PageElement` object to the list of child elements.
        Args:
            element: The element to add as a child element.
            index: If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.
        """
        self.__elements.insert(i if i is not None else len(self.__elements), element)
        if element.parent is not self:
            element._PageElement__parent = self
    
    def delete(self, element: PageElement | None = None) -> PageElement | None:
        """
        Remove an element from the list of child elements or the element itself.
        Args:
            element: The element to remove. If set to None, the current element itself is removed.
        Returns:
            The `PageElement` if it was deleted. Otherwise, None.
        """
        if element is None and self.parent:
            self.parent.delete_element(self)
            return self
        elif element in self.__elements:
            self.__elements.remove(element)
            return element
        return None
    
    def clear(self) -> None:
        """
        Remove all elements from the list of child elements.
        """
        self.__elements.clear()
