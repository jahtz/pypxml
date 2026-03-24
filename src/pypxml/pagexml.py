# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Iterator

from lxml import etree

from .pageelement import PageElement
from .pageschema import PageSchema
from .pagetype import PageType


logger: logging.Logger = logging.getLogger(__name__)


class PageXML:
    """
    High-level representation of a PAGE-XML document and its top-level 'Page' element.
    
    This class models the logical and structural contents of a PAGE-XML file as 
    defined by the PAGE (Page Analysis and Ground Truth Elements) specification,
    which can be found here: https://ocr-d.de/de/gt-guidelines/trans/trPage.html
    """
    
    def __init__(
        self,
        creator: str | None = None,
        created: datetime | str | None = None,
        changed: datetime | str | None = None,
        **attributes: str | None
    ) -> None:
        """
        Create a new `PageXML` object.

        Args:
            creator: Creator of the PAGE-XML. Defaults to None.
            created: Timestamp (ISO 8601) of the creation of the PAGE-XML. Defaults to None.
            changed: Timestamp (ISO 8601) of the last change. Defaults to None.
            attributes: Named arguments that represent the optional attributes of the 'Page' element.
        """
        self.creator: str = creator  # ty:ignore[invalid-assignment]
        self.created: datetime = created  # ty:ignore[invalid-assignment]
        self.changed: datetime = changed  # ty:ignore[invalid-assignment]
        self.attributes: dict[str, str] = attributes  # ty:ignore[invalid-assignment]
        
        self.__reading_order: list[str] = []
        self.__elements: list[PageElement] = []
        
        logger.info('New PageXML object created')
    
    def __str__(self) -> str:
        return repr(self)
    
    def __repr__(self) -> str:
        return f'PAGE-XML {str(self.__attributes)}'
    
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
    def creator(self) -> str:
        """ Metadata: Creator of the PAGE-XML """
        return self.__creator
    
    @creator.setter
    def creator(self, value: str | None) -> None:
        self.__creator: str = 'pypxml' if not value else str(value)
        
    @property
    def created(self) -> datetime:
        """ Metadata: Timestamp (ISO 8601) of the creation of the PAGE-XML """
        return self.__created
    
    @created.setter
    def created(self, value: datetime | str | None) -> None:
        if isinstance(value, datetime):
            self.__created: datetime = value
        elif isinstance(value, str):
            self.__created: datetime = datetime.fromisoformat(value)
        else:
            self.__created: datetime = datetime.now(timezone.utc)
    
    @property
    def changed(self) -> datetime:
        """ Metadata: Timestamp (ISO 8601) of the last change """
        return self.__changed
    
    @changed.setter
    def changed(self, value: datetime | str | None) -> None:
        if isinstance(value, datetime):
            self.__changed: datetime = value
        elif isinstance(value, str):
            self.__changed: datetime = datetime.fromisoformat(value)
        else:
            self.__changed: datetime = datetime.now(timezone.utc)
        
    @property
    def attributes(self) -> dict[str, str]:
        """ A dictionary containing key/value pairs that represent attributes of the PAGE element (copy) """
        return self.__attributes.copy()
    
    @attributes.setter
    def attributes(self, attrs: dict[str, str] | None) -> None:
        if not attrs:
            self.__attributes: dict[str, str] = {}
        else:
            self.__attributes: dict[str, str] = {
                str(k): str(v) for k, v in attrs.items() 
                if v is not None
            }
            
    @property
    def reading_order(self) -> list[str]:
        """ List of element id's in the correct order (copy) """
        return self.__reading_order.copy()
    
    @property
    def elements(self) -> list[PageElement]:
        """ List of child `PageElement` objects (copy) """
        return self.__elements.copy()
    
    @property
    def regions(self) -> list[PageElement]:
        """ List of child `PageElement` region objects (copy) """
        return list([e for e in self.__elements if e.region])
    
    @classmethod
    def _from_etree(cls, tree: etree._Element, raise_on_error: bool = True) -> PageXML:
        page: etree._Element | None = tree.find('./{*}Page')
        if page is None:
            raise ValueError('The passed etree object does not contain a Page element')
        attrs: dict[str, str] = {k: v for k, v in page.items() if v is not None}
        
        creator,created, changed = None, None, None
        if (md := tree.find('./{*}Metadata')) is not None:
            if (e := md.find('./{*}Creator')) is not None:
                creator = e.text
            if (e := md.find('./{*}Created')) is not None:
                created = e.text
            if (e := md.find('./{*}LastChange')) is not None:
                changed = e.text
        xml: PageXML = cls(creator, created, changed, **attrs)
        
        if (ro := page.find('./{*}ReadingOrder')) is not None:
            ro_elements = ro.findall('.//{*}RegionRefIndexed')
            xml._PageXML__reading_order = [  # type: ignore[prv-type]
                str(e.get('regionRef'))
                for e in sorted(ro_elements, key=lambda x: int(x.get('index')))
            ]
            page.remove(ro)

        for element in page:
            if (pe := PageElement._from_etree(element, xml, raise_on_error)) is not None:
                xml.set(pe, reading_order=False)
        return xml

    def _to_etree(self, schema: PageSchema | str = '2019') -> etree._Element:
        PRE_RO: list[PageType] = [PageType.AlternativeImage, PageType.Border, PageType.PrintSpace]
        POST_RO: list[PageType] = [PageType.Layers, PageType.Relations, PageType.TextStyle, PageType.UserDefined, PageType.Labels]
        
        self.changed: datetime = datetime.now()
        
        if isinstance(schema, str):
            schema: PageSchema = PageSchema.get(schema)
        xsi_qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        nsmap: dict[None | str, str] = {None: schema.xmlns, 'xsi': schema.xmlns_xsi}
        
        root: etree._Element = etree.Element('PcGts', {xsi_qname: schema.xsi_schema_location}, nsmap=nsmap)
        
        metadata: etree._Element = etree.SubElement(root, 'Metadata')
        etree.SubElement(metadata, 'Creator').text = self.creator
        etree.SubElement(metadata, 'Created').text = self.created.isoformat()
        etree.SubElement(metadata, 'LastChange').text = self.changed.isoformat()
        
        page: etree._Element = etree.Element('Page', **self.__attributes)  # type: ignore[arg-type]
        root.append(page)
        
        for pt in PRE_RO:
            for element in self.find_all(pt):
                page.append(element._to_etree())
        
        if len(self.__reading_order) > 0:
            reading_order: etree._Element = etree.SubElement(page, 'ReadingOrder')
            order_group: etree._Element = etree.SubElement(reading_order, 'OrderedGroup', id='g0')
            for i, _id in enumerate(self.__reading_order):
                etree.SubElement(order_group, 'RegionRefIndexed', index=str(i), regionRef=_id)
        
        for pt in POST_RO:
            for element in self.find_all(pt):
                page.append(element._to_etree())
                
        for region in self.regions:
            page.append(region._to_etree())
            
        return root

    @classmethod
    def open(cls, xml: Path | str, encoding: str = 'utf-8', raise_on_error: bool = True) -> PageXML:
        """
        Create a `PageXml` object from a PAGE-XML file.

        Args:
            xml: The file to open.
            encoding: File encoding. Defaults to 'utf-8'.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.

        Raises:
            ValueError: If the lxml etree object is not a valid PAGE-XML and raise_on_error is True.
            
        Returns:
            A `PageXml` object that represents the passed PAGE-XML file.
        """
        parser: etree.XMLParser[etree._Element] = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        return cls._from_etree(etree.parse(xml, parser).getroot(), raise_on_error)
    
    def save(self, xml: Path | str, encoding: str = 'utf-8', schema: PageSchema | str = '2019') -> None:
        """
        Write a PAGE-XML file with the data of the current `PageXml` object.

        Args:
            xml: The file to save to.
            encoding: File encoding. Defaults to 'utf-8'.
            schema: Select a schema version (currently supported: `2017`, `2019`) or pass a custom schema. 
                Defaults to '2019'.
        """
        with open(xml, 'wb') as f:
            f.write(etree.tostring(
                self._to_etree(schema), 
                pretty_print=True, 
                encoding=encoding, 
                xml_declaration=True
            ))
            
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
    
    def create(
        self, 
        pagetype: PageType, 
        pos: int | None = None, 
        reading_order: bool = True, 
        **attributes: str
    ) -> PageElement:
        """
        Create a new child `PageElement` and add it to the list of elements.
        
        Args:
            pagetype: Type of the new child element.
            pos: If set, inserts the new element at this position (start with 0), else append. Defaults to None.
            reading_order: If set to True, add the element to the reading order at the specified index. 
                Only applies if the element is a region. Defaults to True.
            attributes: Named arguments that represent the attributes of the child object.
        Returns:
            The newly created child `PageElement`.
        """
        element = PageElement(pagetype, self, **attributes)
        self.set(element, pos, reading_order)
        return element
    
    def set(self, element: PageElement, pos: int | None = None, reading_order: bool = True) -> None:
        """
        Add an existing `PageElement` object to the list of child elements.
        
        Args:
            element: The element to add as a child element.
            pos: If set, inserts the new element at this position (start with 0), else append. Defaults to None.
            reading_order: If set to True, add the element to the reading order at the specified index. 
                Only applies if the element is a region. Defaults to True.
        """
        if reading_order and element.region and 'id' in element:
            if element['id'] in self.__reading_order:
                raise ValueError(f'Element with id {element["id"]} already exists')
            if pos is None:
                self.__reading_order.append(str(element['id']))
            else:
                self.__reading_order.insert(pos, str(element['id']))
        if pos is None:
            self.__elements.append(element)
        else:
            self.__elements.insert(pos, element)
        if element.parent is not self:
            element._PageElement__parent = self  # type: ignore[arg-type]
            
    def delete(self, element: PageElement) -> PageElement | None:
        """
        Remove an element from the list of child elements. This includes the reading order.
        
        Args:
            element: The element to remove.
        
        Returns:
            The `PageElement` if it was deleted. Otherwise, None.
        """
        if element in self.__elements:
            self.__elements.remove(element)
            if 'id' in element and element['id'] in self.__reading_order:
                self.__reading_order.remove(str(element['id']))
            return element
        return None
    
    def clear(self, only_regions: bool = False) -> None:
        """
        Remove all elements from the list of child elements.
        
        Args:
            only_regions: Only delete region elements. Defaults to False.
        """
        if only_regions:
            for element in self.regions:
                self.delete(element)
        else:
            self.clear()
        self.clear_reading_order()
    
    def apply_reading_order(self) -> None:
        """ 
        Sort the child elements based on the current reading order.

        Non-region elements are placed first, followed by regions according to the reading order.
        Regions not included in the reading order are placed last.
        """
        # improves performance over list.index()
        order: dict[str, int] = {_id: index for index, _id in enumerate(self.__reading_order) if _id}
        
        def sort_key(obj: PageElement):
            if not obj.region:  # non-region types (e.g., AlternativeImage,...) first
                return (0, 0)
            elif 'id' in obj and obj['id'] in order:  # sorted regions next
                return (1, order[obj['id']])
            else:  # unordered regions at the end
                return (2, 0)
        
        self.__elements.sort(key=sort_key)
    
    def create_reading_order(self, overwrite: bool = False) -> None:
        """
        Create a new reading order based on the current element sequence.
        
        Args:
            overwrite: If True, overwrites any existing reading order. If False, only creates a new reading order if 
                the current one is empty. Defaults to False.
        """
        if not self.__reading_order or overwrite:
            self.__reading_order = list([str(e['id']) for e in self.regions if 'id' in e])
        elif self.__reading_order:
            logger.warning('Could not create reading order: reading order already exists.')
    
    def set_reading_order(self, reading_order: list[str] | None, apply: bool = True) -> None:
        """
        Update the reading order of regions in the PAGE-XML document.
        
        Args:
            reading_order: A list of region IDs defining the desired reading order. If an empty list or None is 
                passed, the reading order is cleared. (Note: Validity of IDs is not checked.)
            apply: If True, reorders the elements in the `PageXML` based on the passed reading order. Defaults to True.
        """
        if reading_order is None:
            self.__reading_order.clear()
        else:
            self.__reading_order = reading_order
        if apply:
            self.apply_reading_order()
    
    def clear_reading_order(self) -> None:
        """
        Remove all elements from the reading order without deleting the actual elements.
        """
        self.__reading_order.clear()
