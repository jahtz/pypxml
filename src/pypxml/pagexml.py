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

from typing import Self, Optional, Union
from datetime import datetime
from pathlib import Path
import importlib.resources
import json

from lxml import etree

from .pagelement import PageElement
from .pagetype import PageType


class PageXML:
    """
    PageXML Root and Page element class.
    """
    
    def __init__(self, creator: Optional[str] = None, created: Optional[Union[datetime, str]] = None,
                 changed: Optional[Union[datetime, str]] = None, xml: Optional[Path] = None, 
                 **attributes: str) -> None:
        """
        PLEASE USE THE .new() METHOD TO CREATE A NEW PAGEXML OBJECT.
        This constructor is only for internal use.
        Args:
            creator: Metadata `Creator`. Defaults to None.
            created: Metadata `Created` in UTC, not local time. Defaults to None.
            changed: Metadata `LastChange` in UTC, not local time. Defaults to None.
            file: Path of the PageXML file, if the object was created from a file. Defaults to None.
            attributes: Named arguments which represent the attributes of the PageXML object.
        """
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
            
        self.__attributes: dict[str, str] = attributes if attributes else {}
        self.__reading_order: list[str] = []  # list of region id's in correct order
        self.__elements: list[PageElement] = []  # content of page
        self.__xml: Optional[Path] = xml  # file path of the pagexml file if it was loaded from a file
    
    def __str__(self) -> str:
        """ Returns the string representation of the PageXML object. """
        return f"<PageXML {self.__attributes}>"
    
    def __repr__(self) -> str:
        """ Returns the string representation of the PageXML object. """
        return self.__str__()
        
    def __len__(self) -> int:
        """ Returns the number of region elements in the PageXML object. """
        return len([element for element in self.__elements if element.is_region()])
    
    def __iter__(self) -> Self:
        """ Iterate over all elements of the page. """
        self.__n = 0
        return self

    def __next__(self) -> PageElement:
        """ Yield next element of the page. """
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration
    
    def __getitem__(self, key: Union[int, str]) -> Optional[Union[PageElement, str]]:
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

    def __setitem__(self, key: Union[int, str], value: Union[PageElement, str]) -> None:
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

    def __contains__(self, key: Union[PageElement, str]) -> bool:
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
    def creator(self) -> Optional[str]:
        """ Returns the metadata `Creator`. """
        return self.__creator
    
    @creator.setter
    def creator(self, value: str) -> None:
        """ Set the metadata `Creator`. """
        self.__creator = str(value)
        
    @property
    def created(self) -> Optional[str]:
        """ Returns the metadata `Created`. """
        return self.__created
    
    @created.setter
    def created(self, value: Union[datetime, str]) -> None:
        """ Set the metadata `Created`. """
        if isinstance(value, datetime):
            self.__created = value.isoformat()
        elif isinstance(value, str):
            self.__created = value
        else:
            raise ValueError("Invalid type for created")
        
    @property
    def changed(self) -> Optional[str]:
        """ Returns the metadata `LastChange`. """
        return self.__changed
    
    @changed.setter
    def changed(self, value: Union[datetime, str]) -> None:
        """ Set the metadata `LastChange`. """
        if isinstance(value, datetime):
            self.__changed = value.isoformat()
        elif isinstance(value, str):
            self.__changed = value
        else:
            raise ValueError("Invalid type for last change")
        
    @property
    def attributes(self) -> dict[str, str]:
        """ Get the attributes of the page element. """
        return self.__attributes
    
    @attributes.setter
    def attributes(self, attributes: dict[str, str]) -> None:
        """ Set the attributes of the page element. """
        self.__attributes = {} if not attributes else {str(k): str(v) for k, v in attributes.items() if v is not None}
        
    @property
    def elements(self) -> list[PageElement]:
        """ Returns a copy of the elements list. """
        return self.__elements.copy()
    
    @property
    def regions(self) -> list[PageElement]:
        """ Returns a copy of the regions list. """
        return [element for element in self.__elements if element.is_region()]
    
    @property
    def reading_order(self) -> list[str]:
        """ Returns the reading order of the page. """
        return self.__reading_order
    
    @reading_order.setter
    def reading_order(self, order: Optional[list[str]]) -> None:
        """ Set the reading order of the page. """
        self.__reading_order = [] if not order else [str(i) for i in order if i is not None]
        
    @property
    def xml(self) -> Optional[Path]:
        """ Returns the file path of the PageXML file. """
        return self.__xml
    
    @xml.setter
    def xml(self, file: Union[Path, str]) -> None:
        """ Set the file path of the PageXML file. """
        if isinstance(file, Path) or isinstance(file, str):
            self.__xml = Path(file)
        else:
            raise ValueError("Invalid type for xml")
    
    @classmethod
    def new(cls, creator: str = "pypxml", **attributes: str) -> Self:
        """
        Create a new empty PageXML object.
        Args:
            creator: Set a custom PageXML `Metadata` creator. Defaults to "pypxml".
            attributes: Named arguments which represent the attributes of the `Page` object.
        Returns:
            A empty PageXML object.
        """
        attributes = {str(k): str(v) for k, v in attributes.items() if v is not None}
        return cls(creator=creator, created=datetime.now().isoformat(), changed=datetime.now().isoformat(), 
                   **attributes)
        
    @classmethod
    def from_etree(cls, tree: etree.Element, skip_unknown: bool = False) -> Self:
        """
        Create a new PageXML object from an lxml etree object.
        Args:
            tree: lxml etree object.
            skip_unknown: Skip unknown elements. Else raise ValueError. Defaults to False.
        Raises:
            ValueError: If the etree object does not contain a Page element.
        Returns:
            PageXML object that represents the passed etree element.
        """
        if (page := tree.find("./{*}Page")) is not None:
            attributes = {str(k): str(v) for k, v in dict(page.items()).items() if v is not None}
            
            # Metadata
            if (md_tree := tree.find("./{*}Metadata")) is not None:
                if (creator := md_tree.find("./{*}Creator")) is not None:
                    creator = creator.text
                if (created := md_tree.find("./{*}Created")) is not None:
                    created = created.text
                if (last_change := md_tree.find("./{*}LastChange")) is not None:
                    last_change = last_change.text
                pagexml = cls(creator=creator, created=created, changed=last_change, **attributes)
            else:
                pagexml = cls.new(**attributes)
            
            # ReadingOrder
            if (ro := tree.find("./{*}ReadingOrder")) is not None:
                if (ro_elements := tree.findall("../{*}RegionRefIndexed")) is not None:
                    page._ro = list([i.get("regionRef") for i in sorted(list(ro_elements),
                                                                        key=lambda i: i.get("index"))])
                tree.remove(ro)
                
            # PageElements
            for element in page:
                if (pe := PageElement.from_etree(element, pagexml, skip_unknown)) is not None:
                    pagexml.set_element(pe, ro=False)
            return pagexml
        raise ValueError("The passed etree object does not contain a Page element.")

    @classmethod
    def from_file(cls, file: Union[Path, str], encoding: str = "utf-8", skip_unknown: bool = False) -> Self:
        """
        Create a new PageXML object from a PageXML file.
        Args:
            file: Path of the PageXML file.
            encoding: Set custom encoding. Defaults to "utf-8".
            skip_unknown: Skip unknown elements. Else raise ValueError. Defaults to False.
        Returns:
            PageXML object that represents the passed PageXML file.
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        tree = etree.parse(file, parser).getroot()
        pagexml = cls.from_etree(tree, skip_unknown=skip_unknown)
        pagexml.xml = Path(file)
        return pagexml
    
    def to_etree(self, schema_version: str = "2019", schema_file: Optional[Union[Path, str]] = None) -> etree.Element:
        """
        Returns the PageXML object as an lxml etree object.
        Args:
            schema_version: Which schema version to use. Available by default: "2017", "2019". Defaults to "2019".
            schema_file: Set a custom schema json file (see documentation for further information). Defaults to None.
        Returns:
            A lxml etree object that represents the PageXML object.
        """
        self.__changed = datetime.now().isoformat()
        if schema_file is None:
            schema_file = importlib.resources.files("pypxml").parent.joinpath("resources", "schema.json")
        with open(schema_file) as stream:
            schema = json.load(stream)[schema_version]
        
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
        
        # PageElements
        for element in self.__elements:
            page.append(element.to_etree())
            
        return root
    
    def to_file(self, file: Union[Path, str], encoding="utf-8", schema_version: str = "2019", 
                schema_file: Optional[Union[Path, str]] = None) -> None:
        """
        Write the PageXML object to a file.

        Args:
            file: File path to write the PageXML object to.
            encoding: Set custom encoding. Defaults to "utf-8".
            schema_version: Which schema version to use. Available by default: "2017", "2019". Defaults to "2019".
            schema_file: Set a custom schema json file (see documentation for further information). Defaults to None.
        """
        with open(file, "wb") as f:
            tree = etree.tostring(self.to_etree(schema_version, schema_file), pretty_print=True, encoding=encoding, 
                                  xml_declaration=True)
            f.write(tree)
    
    def find_by_id(self, id: str, recursive: bool = False) -> Optional[PageElement]:
        """
        Find an element by its id.
        Args:
            id: ID of the element to find.
            recursive: If set, search in all child elements. Defaults to False.
        Returns:
            The PageElement object with the given ID. Returns None, if no match was found.
        """
        for element in self.__elements:
            if element.get_attribute("id") == id:
                return element
            if recursive:
                if (found := element.find_by_id(id, recursive)) is not None:
                    return found
        return None
   
    def find_by_type(self, pagetype: Union[PageType, list[PageType]], recursive: bool = False) -> list[PageElement]:
        """
        Find all elements by their type.
        Args:
            pagetype: Type of the elements to find.
            recursive: If set, search in all child elements. Defaults to False.
        Returns:
            A list of PageElement objects with the given type. Returns an empty list, if no match was found.
        """
        if isinstance(pagetype, PageType):
            pagetype = [pagetype]
        found_elements: list[PageElement] = []
        for element in self.__elements:
            if element.pagetype in pagetype:
                found_elements.append(element)
            if recursive:
                found_elements.extend(element.find_by_type(pagetype, recursive))
        return found_elements
    
    def create_element(self, pagetype: PageType, index: Optional[int] = None, **attributes: str) -> PageElement:
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
    
    def get_element(self, index: int) -> Optional[PageElement]:
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
    
    def set_element(self, element: PageElement, index: Optional[int] = None, ro: bool = True) -> None:
        """
        Add an existing PageElement object to the list of elements.
        Args:
            element: The PageElement to add.
            index: If set, insert the element at this index. Else append to the list. Defaults to None.
            ro: If set to true, add the element to the reading order at the specified index.
                Only if the element is a region.
        """
        if index is None:
            self.__elements.append(element)
            if ro and element.is_region() and element["id"]:
                self.__reading_order.append(element["id"])
        else:
            self.__elements.insert(min(index, len(self.__elements) - 1), element)
            if ro and element.is_region() and element["id"]:
                self.__reading_order.insert(min(index, len(self.__elements) - 1), element["id"])
        if element.parent is not self:
            element._PageElement__parent = self
    
    def remove_element(self, element: Union[PageElement, int]) -> Optional[PageElement]:
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
        """ Remove all attributes from the PageXML object. """
        self.__attributes = {}
        