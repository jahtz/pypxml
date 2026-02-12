# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Literal

from lxml import etree

from .pageelement import PageElement
from .pageschema import PageSchema
from .pagetypes import PageType


logger = logging.getLogger(__name__)


class PageXML:
    """
    High-level representation of a PAGE-XML document and its top-level 'Page' element.

    This class models the logical and structural contents of a PAGE-XML file as
    defined by the PAGE (Page Analysis and Ground Truth Elements) specification,
    which can be found here: https://ocr-d.de/de/gt-guidelines/trans/trPage.html
    
    Provided functionalities:

    - Store image metadata (filename, width, height)
    - Manage PAGE metadata (creator, creation time, last modification time)
    - Hold and manipulate child `PageElement` objects (regions and other elements)
    - Maintain, generate, and apply reading order information
    - Parse PAGE-XML documents from files or create a new one
    - Serialize the in-memory representation back to valid PAGE-XML

    `PageXML` acts as the root container for all page-level layout elements and
    serves as the primary entry point for reading, modifying, and writing PAGE-XML
    documents within the _pypxml_ library.
    """
    
    def __init__(
        self,
        creator: str = 'pypxml',
        created: datetime | str | None = None,
        last_change: datetime | str | None = None,
        **attributes: str
    ) -> None:
        """
        Create a new empty `PageXML` object.
        Args:
            creator: The creator of the PAGE-XML object. Defaults to 'pypxml'.
            created: The timestamp (ISO 8601) of the creation of the PAGE-XML. 
                The timestamp must be in UTC (Coordinated Universal Time) and not local time. 
                Defaults to None.
            last_change: The timestamp (ISO 8601) of the last change. 
                The timestamp must be in UTC (Coordinated Universal Time) and not local time. 
                Defaults to None.
            attributes: Named arguments that represent the optional attributes of the 'Page' element.
        """
        self.creator: str = creator
        self.created: str = created
        self.last_change: str = last_change
        
        self.attributes: dict[str, str] = attributes
        
        self.__reading_order: list[str] = []
        self.__elements: list[PageElement] = []

    def __str__(self) -> str:
        return repr(self)
    
    def __repr__(self) -> str:
        s = f'PcGts {str({'creator': self.__creator, 'created': self.__created, 'last_change': self.__last_change})}\n'\
            + f'Page {str(self.__attributes)}'
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
        
    def __getitem__(self, key: int | str) -> PageElement | str | None:
        if isinstance(key, int):
            return self.__elements[key]
        else:
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
    def creator(self) -> str:
        """
        The creator of the PAGE-XML.
        """
        return self.__creator
    
    @creator.setter
    def creator(self, value: str | None) -> None:
        """
        The creator of the PAGE-XML file.
        """
        self.__creator = 'pypxml' if not value else str(value)

    @property
    def created(self) -> str:
        """
        The timestamp (ISO 8601) of the creation of the PAGE-XML file.
        """
        return self.__created
    
    @created.setter
    def created(self, value: datetime | str | None) -> None:
        """
        The timestamp (ISO 8601) of the creation of the PAGE-XML file.
        """
        if isinstance(value, datetime):
            self.__created: str = value.isoformat()
        elif isinstance(value, str):
            self.__created: str = value
        else:
            self.__created: str = datetime.now(timezone.utc).isoformat()
    
    @property
    def last_change(self) -> str:
        """
        The timestamp (ISO 8601) of the last change.
        """
        return self.__last_change
    
    @last_change.setter
    def last_change(self, value: datetime | str | None) -> None:
        """
        The timestamp (ISO 8601) of the last change.
        """
        if isinstance(value, datetime):
            self.__last_change: str = value.isoformat()
        elif isinstance(value, str):
            self.__last_change: str = value
        else:
            self.__last_change: str = datetime.now(timezone.utc).isoformat()
    
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
    def reading_order(self) -> list[str]:
        """ Returns a copy of the reading order of the page. """
        return self.__reading_order.copy()
        
    @property
    def elements(self) -> list[PageElement]:
        """
        A copy of the list of child elements.
        """
        return self.__elements.copy()

    @property
    def regions(self) -> list[PageElement]:
        """
        Returns a copy of the list of child regions.
        """
        return list([e for e in self.__elements if e.is_region])
    
    @classmethod
    def _from_etree(cls, tree: etree.Element, raise_on_error: bool = True) -> PageXML:
        """
        Create a new `PageXML` object from a lxml etree element.
        Args:
            tree: The lxml etree element.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Raises:
            ValueError: If the element is not a valid PageXML and raise_on_error is True.
        Returns:
            A `PageXML` object that represents the passed etree element.
        """
        if (page := tree.find('./{*}Page')) is not None:
            attributes = {str(k): str(v) for k, v in dict(page.items()).items() if v is not None}
            
            # Metadata
            creator = None
            created = None
            last_change = None
            if (md_tree := tree.find('./{*}Metadata')) is not None:
                if (creator := md_tree.find('./{*}Creator')) is not None:
                    creator = creator.text
                if (created := md_tree.find('./{*}Created')) is not None:
                    created = created.text
                if (last_change := md_tree.find('./{*}LastChange')) is not None:
                    last_change = last_change.text
            pagexml = cls(creator=creator, created=created, last_change=last_change, **attributes)
            
            # ReadingOrder
            if (ro := page.find('./{*}ReadingOrder')) is not None:
                if (ro_elements := ro.findall('.//{*}RegionRefIndexed')) is not None:
                    pagexml._PageXML__reading_order = list(
                        [e.get('regionRef') for e in sorted(list(ro_elements), key=lambda x: int(x.get('index')))]
                    )
                page.remove(ro)
                
            # PageElements
            for element in page:
                if (pe := PageElement._from_etree(element, parent=pagexml, raise_on_error=raise_on_error)) is not None:
                    pagexml.set(pe, reading_order=False)
            return pagexml
        raise ValueError('The passed etree object does not contain a Page element.')
    
    def _to_etree(self, schema: PageSchema | str | None = None) -> etree.Element:
        """
        Convert the `PageXML` object to a lxml etree element. 
        Args:
            schema: Select a schema version (currently supported: `2017`, `2019`) or pass a custom schema. 
            Defaults to None.
        Returns:
            A lxml etree object that represents the `PageXML` object.
        """
        PRE_RO = [PageType.AlternativeImage, PageType.Border, PageType.PrintSpace]
        POST_RO = [PageType.Layers, PageType.Relations, PageType.TextStyle, PageType.UserDefined, PageType.Labels]

        self.__last_change = datetime.now().isoformat()
        
        if schema:
            if isinstance(schema, str):
                schema = PageSchema.get(schema)
            xsi_qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
            nsmap = {None: schema.xmlns, 'xsi': schema.xmlns_xsi}
            root = etree.Element('PcGts', {xsi_qname: schema.xsi_schema_location}, nsmap=nsmap)
        else:
            root = etree.Element('PcGts')
        
        # Metadata
        metadata = etree.SubElement(root, 'Metadata')
        etree.SubElement(metadata, 'Creator').text = self.creator
        etree.SubElement(metadata, 'Created').text = self.created
        etree.SubElement(metadata, 'LastChange').text = self.last_change
        
         # Page
        page = etree.Element('Page', **self.__attributes)
        root.append(page)
        
        # Pre ReadingOrder elements
        for pt in PRE_RO:
            for element in self.find_all(pagetype=pt):
                page.append(element._to_etree())
                
        # ReadingOrder
        if len(self.__reading_order) > 0:
            reading_order = etree.SubElement(page, 'ReadingOrder')
            order_group = etree.SubElement(reading_order, 'OrderedGroup', id='g0')
            for i, rid in enumerate(self.__reading_order):
                etree.SubElement(order_group, 'RegionRefIndexed', index=str(i), regionRef=rid)
                
        # Post Pre ReadingOrder elements
        for pt in POST_RO:
            for element in self.find_all(pagetype=pt):
                page.append(element._to_etree())
                
        # PageElements
        for region in self.regions:
            page.append(region._to_etree())
        return root
    
    @classmethod
    def open(cls, file: Path | str, encoding: str = 'utf-8', raise_on_error: bool = True) -> PageXML:
        """
        Create a new `PageXML` object from a PAGE-XML file.
        Args:
            file: The path of the PAGE-XML file.
            encoding: Custom encoding. Defaults to 'utf-8'.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Returns:
            A `PageXML` object that represents the passed PAGE-XML file.
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        tree = etree.parse(file, parser).getroot()
        pagexml = cls._from_etree(tree, raise_on_error)
        return pagexml
    
    def save(self, file: Path | str, encoding: str = 'utf-8', schema: PageSchema | str = '2019') -> None:
        """
        Write the `PageXML` object to a file.
        Args:
            file: The file path to write the object to.
            encoding: Set file encofing. Defaults to 'utf-8'.
            schema: Select a schema version (currently supported: `2017`, `2019`) or pass a custom schema. 
        """
        with open(file, 'wb') as f:
            tree = etree.tostring(self._to_etree(schema), pretty_print=True, encoding=encoding, xml_declaration=True)
            f.write(tree)
    
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
    
    def create(
        self, 
        pagetype: PageType, 
        i: int | None = None, 
        reading_order: bool = True, 
        **attributes: str
    ) -> PageElement:
        """
        Create a new child `PageElement` and add it to the list of elements.
        Args:
            pagetype: The `PageType` of the new child element.
            i: If set, insert the new element at this index. Otherwise, append it to the list. Defaults to None.
            reading_order: If set to True, add the element to the reading order at the specified index. 
                Only applies if the element is a region. Defaults to True.
            attributes: Named arguments that represent the attributes of the child object.
        Returns:
            The newly created `PageElement` child object.
        """
        element = PageElement(pagetype, self, **attributes)
        self.set(element=element, i=i, reading_order=reading_order)
        return element
    
    def set(self, element: PageElement, i: int | None = None, reading_order: bool = True) -> None:
        """
        Add an existing `PageElement` object to the list of child elements.
        Args:
            element: The element to add as a child element.
            i: If set, insert the element at this index. Otherwise, append it to the list. Defaults to None.
            reading_order: If set to True, add the element to the reading order at the specified index. 
                Only applies if the element is a region. Defaults to True.
        """
        if reading_order and element.is_region and 'id' in element:
            if element['id'] in self.__reading_order:
                raise ValueError(f'Element with id {element["id"]} already exists')
            self.__reading_order.insert(i if i is not None else len(self.__reading_order), element['id'])
        self.__elements.insert(i if i is not None else len(self.__elements), element)
        if element.parent is not self:
            element._PageElement__parent = self
            
    def delete(self, element: PageElement) -> PageElement | None:
        """
        Remove an element from the list of child elements. This includes occurences in the reading order.
        Args:
            element: The element to remove.
        Returns:
            The `PageElement` if it was deleted. Otherwise, None.
        """
        if element in self.__elements:
            self.__elements.remove(element)
            if 'id' in element and element['id'] in self.__reading_order:
                self.__reading_order.remove(element['id'])
            return element
        return None
    
    def clear(self, regions_only: bool = False) -> None:
        """
        Remove all elements from the list of child elements.
        Args:
            regions_only: Only delete region elements. Defaults to False.
        """
        if regions_only:
            for element in self.regions:
                self.delete(element)
        else:
            self.__elements.clear()
        self.__reading_order.clear()
    
    def reading_order_apply(self) -> None:
        """ 
        Sort the child elements based on the current reading order.

        Non-region elements are placed first, followed by regions according to the reading order.
        Regions not included in the reading order are placed last.
        """
        order = {_id: index for index, _id in enumerate(self.__reading_order)}  # improves performance over list.index()
        
        def sort_key(obj: PageElement):
            if not obj.is_region:  # non-region types (e.g., AlternativeImage,...) first
                return (0, 0)
            elif 'id' in obj and obj['id'] in order:  # sorted regions next
                return (1, order[obj['id']])
            else:  # unordered regions at the end
                return (2, 0)
        
        self.__elements.sort(key=sort_key)
    
    def reading_order_create(self, overwrite: bool = False) -> None:
        """
        Create a new reading order based on the current element sequence.
        Args:
            overwrite: If True, overwrites any existing reading order. If False, only creates a new reading order if 
                the current one is empty. Defaults to False.
        """
        if not self.__reading_order or overwrite:
            self.__reading_order = list([e['id'] for e in self.regions if 'id' in e])
        elif self.__reading_order:
            logger.warning('Could not create reading order: reading order already exists.')
    
    def reading_order_set(self, reading_order: list[str] | None, apply: bool = True) -> None:
        """
        Update the reading order of regions in the PAGE-XML document.
        Args:
            reading_order: A list of region IDs defining the desired reading order. If an empty list or None is 
                passed, the reading order is cleared. (Note: Validity of IDs is not checked.)
            apply: If True, reorders the elements in the `PageXML` based on the passed reading order. Defaults to True.
        """
        if reading_order:
            self.__reading_order = reading_order
            if apply:
                self.reading_order_apply()
        else:
            self.reading_order_clear()
    
    def reading_order_sort(
        self,
        reference: Literal['minimum', 'maximum', 'centroid'] = 'minimum',
        direction: Literal['top-bottom', 'bottom-top', 'left-right', 'right-left'] = 'top-bottom',
        apply: bool = True
    ) -> None:
        """
        Sort the regions in the PAGE-XML document by their location on the page.
        Args:
            reference: The method for determining the reference point used for sorting:
                - `minimum` sorts by the minimum coordinate value in the given direction,
                - `maximum` sorts by the maximum coordinate value in the given direction,
                - `centroid` sorts by the centroid position of each region.
                Defaults to 'minimum'.
            direction: The primary direction in which regions are sorted. Defaults to 'top-bottom'.
            apply: If True, also reorders the physical sequence of region elements in the PageXML. 
                If False, only updates the reading order element without changing the actual XML element order. 
                Defaults to True.
        """
        def sort_key(obj: PageElement):
            if not obj.is_region:
                return (0, 0)
            elif (coords := obj.find(pagetype=PageType.Coords)) is not None and 'points' in coords:
                points = [tuple(map(int, xy.split(','))) for xy in coords['points'].split()]
                axis = 1 if direction in ['top-bottom', 'bottom-top'] else 0
                if reference == 'minimum':
                    key = min(p[axis] for p in points)
                elif reference == 'maximum':
                    key = max(p[axis] for p in points)
                else:
                    key = sum(p[axis] for p in points) / len(points)
                if direction in ['bottom-top', 'right-left']:
                    return (1, -key)
                return (1, key) 
            else:
                return (2, 0)
        self.__elements.sort(key=sort_key)
        self.__reading_order = list([e['id'] for e in self.__elements if e.is_region and 'id' in e])
        if apply:
            self.reading_order_apply()
    
    def reading_order_clear(self) -> None:
        """
        Remove all elements from the reading order without deleting the actual elements.
        """
        self.__reading_order.clear()
