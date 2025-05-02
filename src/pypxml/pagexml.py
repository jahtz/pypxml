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

from datetime import datetime, timezone
import importlib.resources as resources
import json
import logging
from pathlib import Path
from typing import Union, Optional, Literal, Self

from lxml import etree
from rich.logging import RichHandler

from .pageelement import PageElement
from .pagetype import PageType


logging.basicConfig(level=logging.ERROR, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(markup=True)])
logger = logging.getLogger("pagexml")


class PageXML:
    """
    Represents a PageXML file and the "Page" element.
    """
    
    def __init__(self, 
                 creator: str = "pypxml", 
                 created: Optional[Union[str, datetime]] = None, 
                 last_change: Optional[Union[str, datetime]] = None,
                 xml: Optional[Union[str, Path]] = None,
                 **attributes: str) -> Self:
        """
        Create a new empty PageXML object.
        Args:
            creator: The creator of the PageXML. Defaults to "pypxml".
            created: The timestamp (ISO 8601) of the creation of the PageXML file. The timestamp must be in UTC
                (Coordinated Universal Time) and not local time. Defaults to the current time.
            last_change: The timestamp (ISO 8601) of the last change. The timestamp must be in UTC 
                (Coordinated Universal Time) and not local time. Defaults to the current time.
            xml: Optionally, the path to the matching XML file can be provided. Defaults to None.
            attributes: Named arguments that represent the optional attributes of the "Page" element.
        Returns:
            An empty PageXML object.
        """
        self.creator: str = "pypxml" if creator is None else str(creator)
        
        # class setters for the equivalent private values
        self.attributes = attributes
        self.xml = xml
        self.created = created
        self.last_change = last_change
        
        # initialize containers
        self.__reading_order: list[str] = []  # list of region id"s in correct order
        self.__elements: list[PageElement] = []
        
    def __repr__(self) -> str:
        """ Returns a text representation of the object for debugging. """
        return (f"PageXML(filename={self.__filename}, height={self.__height}, width={self.__width}, "
                f"attributes={str(self.__attributes)}, childs={len(self.__elements)}")
        
    def __str__(self) -> str:
        """ Returns a text representation of the object for printing. """
        return f"<PageXML ({self.__filename})>"
    
    def __len__(self) -> int:
        """ Returns the number of child elements of this object (excluding the reading order). """
        return len(self.__elements)
    
    def __iter__(self) -> PageElement:
        """ Iterates over all child elements of this object. """
        self.__n = 0
        return self

    def __next__(self) -> PageElement:
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
        
    def __contains__(self, key: Union[PageElement, str]) -> bool:
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
            key = str(key)
            return key in self.__attributes
        
    @property
    def imageHeight(self) -> int:
        """ The height of the image in pixels. """
        return int(self.__attributes["imageHeight"])
    
    @imageHeight.setter
    def imageHeight(self, value: Union[str, int]) -> None:
        """ Sets the height of the image in pixels. """
        if isinstance(value, (str, int)):
            value = int(value)
            if value < 0:
                logger.warning("Negative imageWidth attribute was set to 0")
            self.__attributes["imageHeight"] = str(max(0, value))
        else:
            raise TypeError(f"Expected an integer or string, got {type(value).__name__}")
    
    @property
    def imageWidth(self) -> int:
        """ The width of the image in pixels. """
        return int(self.__attributes["imageWidth"])
    
    @imageWidth.setter
    def imageWidth(self, value: Union[str, int]) -> None:
        """ Sets the width of the image in pixels. """
        if isinstance(value, (str, int)):
            value = int(value)
            if value < 0:
                logger.warning("Negative imageWidth attribute was set to 0")
            self.__attributes["imageWidth"] = str(max(0, value))
        else:
            raise TypeError(f"Expected an integer or string, got {type(value).__name__}")
        
    @property
    def imageFilename(self) -> str:
        """ The name of the image file, including the file extension. """
        return self.__attributes["imageFilename"]
    
    @imageFilename.setter
    def imageFilename(self, value: Union[Path, str]) -> None:
        """ Sets the name of the image file, including the file extension. """
        if isinstance(value, (Path, str)):
            self.__attributes["imageFilename"] = value if isinstance(value, str) else value.name
        else:
            raise TypeError(f"Expected a Path or string, got {type(value).__name__}") 
        
    @property
    def xml(self) -> Optional[Path]:
        """ Optionally, the path to the matching XML file. """
        return self.__xml
    
    @xml.setter
    def xml(self, value: Optional[Union[Path, str]]) -> None:
        """ Sets the path to the matching XML file. """
        if value is None:
            self.__xml = None
        elif isinstance(value, (Path, str)):
            self.__xml = Path(value).absolute()
        else:
            raise TypeError(f"Expected a Path or string, got {type(value).__name__}") 
    
    @property
    def created(self) -> str:
        """ The timestamp (ISO 8601) of the creation of the PageXML file. """
        return self.__created
    
    @created.setter
    def created(self, value: Optional[Union[str, datetime]]) -> None:
        """ Sets the timestamp (ISO 8601) of the creation of the PageXML file. """
        if isinstance(value, datetime):
            self.__created: str = value.isoformat()
        elif isinstance(value, str):
            self.__created: str = value
        else:
            self.__created: str = datetime.now(timezone.utc).isoformat()
    
    @property
    def last_change(self) -> str:
        """ The timestamp (ISO 8601) of the last change. """
        return self.__last_change
    
    @last_change.setter
    def last_change(self, value: Optional[Union[str, datetime]]) -> None:
        """ Sets the timestamp (ISO 8601) of the last change. """
        if isinstance(value, datetime):
            self.__last_change: str = value.isoformat()
        elif isinstance(value, str):
            self.__last_change: str = value
        else:
            self.__last_change: str = datetime.now(timezone.utc).isoformat()
            
    @property
    def xml(self) -> Optional[Path]:
        """ Optionally, the path to the matching XML file. """
        return self.__xml
    
    @xml.setter
    def xml(self, value: Optional[Union[Path, str]]) -> None:
        """ Sets the path to the matching XML file. """
        if value is None:
            self.__xml = None
        elif isinstance(value, (Path, str)):
            self.__xml = Path(value).absolute()
        else:
            raise TypeError(f"Expected a Path or string, got {type(value).__name__}") 
    
    @property
    def attributes(self) -> dict[str, str]:
        """ Gets a copy of the attributes of the page element. """
        return self.__attributes
    
    @attributes.setter
    def attributes(self, value: Optional[dict[str, str]]) -> None:
        """ Sets the attributes of the page element. """
        if any(k not in value for k in ["imageFilename", "imageHeight", "imageWidth"]):
            raise ValueError(f"A PageXML requires 'imageFilename', 'imageHeight' and 'imageWidth' attributes, got {value}")
        self.__attributes = {} if value is None else {str(k): str(v) for k, v in value.items() if v is not None}
            
    @property
    def reading_order(self) -> list[str]:
        """ Returns a copy of the reading order of the page. """
        return self.__reading_order.copy()
    
    @property
    def elements(self) -> list[PageElement]:
        """ Returns a copy of the list of child elements. """
        return self.__elements.copy()
    
    @property
    def regions(self) -> list[PageElement]:
        """ Returns a copy of the list of child regions. """
        return list([e for e in self.__elements if e.is_region])
    
    @classmethod
    def from_etree(cls, tree: etree.Element, raise_on_error: bool = True) -> Self:
        """
        Creates a new PageXML object from an lxml etree object.
        Args:
            tree: An lxml etree object.
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Raises:
            ValueError: If the element is not a valid PageXML element and raise_on_error is True.
        Returns:
            A PageXML object that represents the passed etree element.
        """
        if (page := tree.find("./{*}Page")) is not None:
            attributes = {str(k): str(v) for k, v in dict(page.items()).items() if v is not None}
            # Metadata
            creator = None
            created = None
            last_change = None
            if (md_tree := tree.find("./{*}Metadata")) is not None:
                if (creator := md_tree.find("./{*}Creator")) is not None:
                    creator = creator.text
                if (created := md_tree.find("./{*}Created")) is not None:
                    created = created.text
                if (last_change := md_tree.find("./{*}LastChange")) is not None:
                    last_change = last_change.text
            pagexml = cls(creator=creator, created=created, last_change=last_change, **attributes)
            # ReadingOrder
            if (ro := page.find("./{*}ReadingOrder")) is not None:
                if (ro_elements := ro.findall(".//{*}RegionRefIndexed")) is not None:
                    pagexml._PageXML__reading_order = list([e.get("regionRef") 
                                                            for e in sorted(list(ro_elements), 
                                                                            key=lambda x: int(x.get("index")))])
                page.remove(ro)
            # PageElements
            for element in page:
                if (pe := PageElement.from_etree(element, parent=pagexml, raise_on_error=raise_on_error)) is not None:
                    pagexml.set_element(pe, ro=False)
            return pagexml
        raise ValueError("The passed etree object does not contain a Page element.")
    
    def to_etree(self, schema_version: str = "2019", schema_file: Optional[Union[Path, str]] = None) -> etree.Element:
        """
        Returns the PageXML object as an lxml etree object.
        Args:
            schema_version: The schema version to use. Available by default: "2017", "2019". Defaults to "2019".
            schema_file: A custom schema JSON file (see documentation for further information). Defaults to None.
        Returns:
            An lxml etree object that represents the PageXML object.
        """
        self.__last_change = datetime.now().isoformat()
        if schema_file is None:
            schema_file = resources.files("pypxml").parent.joinpath("resources", "schema.json")
        with open(schema_file) as stream:
            schema = json.load(stream)[schema_version]
        xsi_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        nsmap = {None: schema["xmlns"], "xsi": schema["xmlns_xsi"]}
        root = etree.Element( "PcGts", {xsi_qname: schema["xsi_schema_location"]}, nsmap=nsmap)
        # Metadata
        metadata = etree.SubElement(root, "Metadata")
        etree.SubElement(metadata, "Creator").text = self.creator
        etree.SubElement(metadata, "Created").text = self.__created
        etree.SubElement(metadata, "LastChange").text = self.__last_change
        # Page
        page = etree.Element("Page", **self.__attributes)
        root.append(page)
        # ReadingOrder
        if len(self.__reading_order) > 0:
            reading_order = etree.SubElement(page, "ReadingOrder")
            order_group = etree.SubElement(reading_order, "OrderedGroup", id="g0")
            for i, rid in enumerate(self.__reading_order):
                etree.SubElement(order_group, "RegionRefIndexed", index=str(i), regionRef=rid)
        # PageElements
        for element in self.__elements:
            page.append(element.to_etree())
        return root
    
    @classmethod
    def from_file(cls, file: Union[Path, str], encoding: str = "utf-8", raise_on_error: bool = True) -> Self:
        """
        Creates a new PageXML object from a PageXML file.
        Args:
            file: The path of the PageXML file.
            encoding: Custom encoding. Defaults to "utf-8".
            raise_on_error: If set to False, parsing errors are ignored. Defaults to True.
        Returns:
            A PageXML object that represents the passed PageXML file.
        """
        logger.info(f"Parsing {file}")
        parser = etree.XMLParser(remove_blank_text=True, encoding=encoding)
        tree = etree.parse(file, parser).getroot()
        pagexml = cls.from_etree(tree, raise_on_error)
        pagexml.xml = Path(file)
        return pagexml
    
    def to_file(self, file: Union[Path, str], encoding="utf-8", schema_version: str = "2019", 
                schema_file: Optional[Union[Path, str]] = None) -> None:
        """
        Writes the PageXML object to a file.
        Args:
            file: The file path to write the PageXML object to.
            encoding: Custom encoding. Defaults to "utf-8".
            schema_version: The schema version to use. Available by default: "2017", "2019". Defaults to "2019".
            schema_file: A custom schema JSON file (see documentation for further information). Defaults to None.
        """
        with open(file, "wb") as f:
            tree = etree.tostring(self.to_etree(schema_version, schema_file), pretty_print=True, encoding=encoding, 
                                  xml_declaration=True)
            f.write(tree)
        logger.info(f"PageXML written to {file}")
            
    def find_by_id(self, id: str, depth: int = 0) -> Optional[PageElement]:
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
    
    def find_by_type(self, pagetype: Union[PageType, list[PageType]], depth: int = 0, 
                     **attributes: str) -> list[PageElement]:
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
        
    def create_element(self, pagetype: PageType, index: Optional[int] = None, **attributes: str) -> PageElement:
        """
        Creates a new child element and adds it to the list of elements.
        Args:
            pagetype: The PageType of the new child element.
            index: If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
            attributes: Named arguments that represent the attributes of the "PageElement" object.
        Returns:
            The newly created child element.
        """
        element = PageElement(pagetype, parent=self, **attributes)
        self.set_element(element, index)
        return element
    
    def set_element(self, element: PageElement, index: Optional[int] = None, ro: bool = True) -> None:
        """
        Adds an existing PageElement object to the list of elements.
        Args:
            element: The PageElement to add.
            index: If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.
            ro: If set to True, adds the element to the reading order at the specified index.
                Only applies if the element is a region.
        """
        if ro and element.is_region and element["id"]:
            if element["id"] in self.__reading_order:
                raise ValueError(f"id {element['id']} is already in reading order")
            self.__reading_order.insert(index if index is not None else len(self.__reading_order), element["id"])
        self.__elements.insert(index if index is not None else len(self.__elements), element)
        if element.parent is not self:
            element._PageElement__parent = self
    
    def delete_element(self, element: PageElement) -> Optional[PageElement]:
        """
        Removes an element from the list of child elements.
        Args:
            element: The PageElement to remove.
        Returns:
            The removed element if it was found. Otherwise, None.
        """
        if element in self.__elements:
            self.__elements.remove(element)
            if "id" in element and element["id"] in self.__reading_order:
                self.__reading_order.remove(element["id"])
            return element
        return None
    
    def clear_elements(self) -> None:
        """ Removes all elements from the list of child elements. This also clears the reading order. """
        self.__elements.clear()
        self.__reading_order.clear()
        
    def apply_reading_order(self) -> None:
        """ 
        Sorts the child elements based on the current reading order.

        Non-region elements are placed first, followed by regions according to the reading order.
        Regions not included in the reading order are placed last.
        """
        order = {_id: index for index, _id in enumerate(self.__reading_order)}  # improves performance over list.index()
        def sort_key(obj: PageElement):
            if not obj.is_region:  # non-region types (Such as AlternativeImage, ...) come first
                return (0, 0)
            elif "id" in obj and obj["id"] in order:  # the sorted regions come next
                return (1, order[obj["id"]])
            else:  # unordered regions at the end
                return (2, 0)
        self.__elements.sort(key=sort_key)

    def create_reading_order(self, force: bool = False) -> None:
        """
        Creates a new reading order based on the current element sequence.
        Args:
            force: If True, overwrites any existing reading order. If False, only creates a new reading order if none 
                currently exists. Defaults to False.
        """
        if not self.__reading_order or force:
            self.__reading_order = list([e["id"] for e in self.regions if "id" in e])
            
    def clear_reading_order(self) -> None:
        """ Removes all elements from the reading order without deleting the actual elements. """
        self.__reading_order.clear()
        
    def set_reading_order(self, reading_order: Optional[list[str]], sync: bool = True) -> None:
        """
        Updates the reading order of regions in the PageXML document.
        Args:
            reading_order: A list of region IDs defining the desired reading order. If an empty list or None is 
                provided, the reading order is cleared. (Note: Validity of IDs is not checked.)
            sync: If True, orders the elements in the PageXML based on the passed reading order. Defaults to True.
        """
        if reading_order:
            self.__reading_order = reading_order
            if sync:
                self.apply_reading_order()
        else:
            self.clear_reading_order()
            
    def sort_reading_order(self, base: Literal["minimum", "maximum", "centroid"] = "minimum",
                           direction: Literal["top-bottom", "bottom-top", "left-right", "right-left"] = "top-bottom",
                           sync: bool = True) -> None:
        """
        Sorts the regions in the PageXML document by their location on the page.
        Args:
            base: The method for determining the reference point used for sorting: 
                "minimum" sorts by the minimum coordinate value in the given direction. 
                "maximum" sorts by the maximum coordinate value in the given direction.
                "centroid" sorts by the centroid position of each region. Defaults to "minimum".
            direction: The primary direction in which regions are sorted. Defaults to "top-bottom".
            sync: If True, also reorders the physical sequence of region elements in the PageXML. If False, only updates 
                the reading order element without changing the actual XML element order. Defaults to True.
        """
        def sort_key(obj: PageElement):
            if not obj.is_region:
                return (0, 0)
            elif (coords := obj.find_coords()) is not None and "points" in coords:
                points = [tuple(map(int, xy.split(','))) for xy in coords["points"].split()]
                axis = 1 if direction in ["top-bottom", "bottom-top"] else 0
                if base == "minimum":
                    key = min(p[axis] for p in points)
                elif base == "maximum":
                    key = max(p[axis] for p in points)
                else:
                    key = sum(p[axis] for p in points) / len(points)
                if direction in ["bottom-top", "right-left"]:
                    return (1, -key)
                return (1, key) 
            else:
                return (2, 0)
        self.__elements.sort(key=sort_key)
        self.__reading_order = list([e["id"] for e in self.__elements if e.is_region and "id" in e])
        if sync:
            self.apply_reading_order()
