# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterator

from lxml import etree

from .pagetype import PageType
if TYPE_CHECKING:
    from .pagexml import PageXML


logger: logging.Logger = logging.getLogger(__name__)


class PageElement:
    """
    Represents a single structural element within a PAGE-XML document.
    """
    def __init__(
        self,
        pagetype: PageType | str,
        parent: PageXML | PageElement,
        **attributes: str | None
    ) -> None:
        """
        Create a new `PageElement` object.

        Args:
            pagetype: PageType of this element.
            parent: Parent object of this element.
            attributes: Named arguments that represent additional attributes of this element.
        """
        self.pagetype: PageType = pagetype  # ty:ignore[invalid-assignment]
        self.attributes: dict[str, str] = attributes  # ty:ignore[invalid-assignment]
        
        self.__parent: PageXML | PageElement = parent
        self.__elements: list[PageElement] = []
        self.__text: str | None = None
        
        logger.info(f'New PageElement ({self.pagetype.value}) object created')
        
    def __str__(self) -> str:
        return repr(self)
    
    def __repr__(self) -> str:
        return f'PageElement ({self.pagetype.value}) {str(self.attributes)}'

    def __getitem__(self, key: str) -> str | None:
        return self.__attributes.get(str(key), None)
    
    def __setitem__(self, key: str, value: str | None) -> None:
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)
    
    def __contains__(self, key: str) -> bool:
        return str(key) in self.__attributes
    
    @property
    def pagetype(self) -> PageType:
        """ Type of the element """
        return self.__pagetype
    
    @pagetype.setter
    def pagetype(self, value: PageType | str) -> None:
        if isinstance(value, str):
            if not PageType.validate(value):
                raise ValueError(f'Invalid PageType: {value}')
            self.__pagetype: PageType = PageType[value]
        elif isinstance(value, PageType):
            self.__pagetype: PageType = value
        else:
            raise ValueError(f'Expected value of type PageType or str, got {type(value).__name__}')
    
    @property
    def region(self) -> bool:
        return self.__pagetype.region
    
    @property
    def attributes(self) -> dict[str, str]:
        """ Dictionary containing key/value pairs that represent attributes of the PAGE element (copy)"""
        return self.__attributes.copy()
    
    @attributes.setter
    def attributes(self, value: dict[str, str] | None) -> None:
        if value is None:
            self.__attributes: dict[str, str] = {}
        else:
            self.__attributes: dict[str, str] = {
                str(k): str(v) for k, v in value.items() 
                if v is not None
            }
    
    @property
    def parent(self) -> PageXML | PageElement:
        """ Parent element of the current element """
        return self.__parent

    @property
    def elements(self) -> list[PageElement]:
        """ List of child `PageElement` objects (copy)"""
        return self.__elements.copy()
    
    @property
    def text(self) -> str | None:
        """ Text of the element """
        return self.__text
    
    @text.setter
    def text(self, value: str | None) -> None:
        """ Text of the element """
        self.__text: None | str = None if value is None else str(value)
    
    @classmethod
    def _from_etree(
        cls,
        tree: etree._Element,
        parent: PageXML | PageElement,
        raise_on_error: bool = True
    ) -> PageElement | None:
        pagetype: str = str(tree.tag).split('}')[1]
        if not PageType.validate(pagetype):
            if not raise_on_error:
                logger.warning(f'Unknown element type: {pagetype}')
                return None
            raise ValueError(f'Unknown element type: {pagetype}')
        
        element: PageElement = cls(PageType[pagetype], parent, **dict(tree.items()))
        element.text = tree.text
        
        for child in tree:
            if (pe := PageElement._from_etree(child, element, raise_on_error)) is not None:
                element.set(pe)
        return element
    
    def _to_etree(self) -> etree._Element:
        element: etree._Element = etree.Element(self.__pagetype.value, **self.__attributes)  # type: ignore[arg-type]
        element.text = self.__text
        for child in self.__elements:
            element.append(child._to_etree())
        return element
    
    def _find_all(self, pt: list[PageType] | None, d: int, attrs: dict[str, list[str]]) -> Iterator[PageElement]:
        for element in self.__elements:
            if pt is None or element.pagetype in pt:
                for sk, sv in attrs.items():
                    if sk not in element or element[sk] not in sv:
                        break
                else:
                    yield element
            if d != 0:
                yield from element._find_all(pt, max(-1 ,d - 1), attrs)

    def find_all(
        self,
        pagetype: list[PageType | str] | PageType | str | None = None,
        depth: int = 0,
        **attributes: list[str] | str
    ) -> Iterator[PageElement]:
        """
        Find `PageElements` by their type and attributes.

        Args:
            pagetype: One or more `PageType`s to look for. Defaults to None.
            depth: Depth of search:
                - `=0` search only on the current level
                - `<0` search all levels recursively
                - `>0` limit the search to the specified number of levels
                Defaults to 0.
            attributes: Named arguments representing the attributes that the found elements must have.
        
        Yields:
            The next found `PageElement`.
        """
        attributes: dict[str, list[str]] = {
            k: list(map(str, v)) if isinstance(v, list) else [str(v)] 
            for k, v in attributes.items()
        }
        
        if pagetype is not None:
            if not isinstance(pagetype, list):
                pagetype = [pagetype]
            pagetype: list[PageType] = [pt if isinstance(pt, PageType) else PageType[pt] for pt in pagetype]
        
        yield from self._find_all(pagetype, depth, attributes)
    
    def find(
        self,
        pagetype: list[PageType | str] | PageType | str | None = None,
        depth: int = 0,
        **attributes: str | list[str]
    ) -> PageElement | None:
        """
        Find a `PageElement` by their type and attributes.
        Args:
            pagetype: One or more `PageType`s to look for. Defaults to None.
            depth: Depth of search:
                - `=0` search only on the current level
                - `<0` search all levels recursively
                - `>0` limit the search to the specified number of levels
                Defaults to 0.
            attributes: Named arguments representing the attributes that the found elements must have.
        Returns:
            The first found `PageElement` or None if no match was found.
        """
        return next(self.find_all(pagetype, depth, **attributes), None)
    
    def create(self, pagetype: PageType, pos: int | None = None, **attributes: str) -> PageElement:
        """
        Create a new child `PageElement` and add it to the list of elements.
        Args:
            pagetype: Type of the new child element.
            pos: If set, inserts the new element at this position (start with 0), else append. Defaults to None.
            attributes: Named arguments that represent the attributes of the child object.
        Returns:
            The newly created child `PageElement`.
        """
        element: PageElement = PageElement(pagetype, self, **attributes)
        self.set(element, pos)
        return element
    
    def set(self, element: PageElement, pos: int | None = None) -> None:
        """
        Adds an existing `PageElement` to the list of child elements.
        
        Args:
            element: The element to add as a child element.
            pos: If set, inserts the new element at this position (start with 0), else append. Defaults to None.
        """
        if pos is None:
            self.__elements.append(element)
        else:
            self.__elements.insert(pos, element)
        if element.parent is not self:
            element._PageElement__parent = self  # type: ignore[prv-type]
            
    def delete(self, element: PageElement | None = None) -> PageElement | None:
        """
        Remove an element from the list of child elements or the element itself.
        
        Args:
            element: The element to remove. If set to None, the current element itself is removed.
        
        Returns:
            The deleted `PageElement`. Otherwise, None.
        """
        if element is None and self.parent:
            self.parent.delete(self)
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
