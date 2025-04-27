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
    Represents a PageXML file and the `Page` element.
    """
    
    def __init__(self, 
                 height: Union[str, int], 
                 width: Union[str, int], 
                 filename: Union[Path, str],
                 xml: Optional[Union[str, Path]] = None,
                 creator: str = "pypxml", 
                 created: Optional[Union[str, datetime]] = None, 
                 last_change: Optional[Union[str, datetime]] = None,
                 **attributes: str) -> Self:
        """
        reate a new empty PageXML object.
        Args:
            height: The height of the image in pixels.
            width: The width of the image in pixels.
            filename: The name of the image file including the file extension. 
                      If a Path object is provided, only the filename is used.
            xml: Optionally, the path to the matching xml file can be provided. Defaults to None.
            creator: The creator of the PageXML. Defaults to "pypxml".
            created: The timestamp  (ISO 8601) of the creation of the PageXML file. The timestamp has to be in UTC
                     (Coordinated Universal Time) and not local time. Defaults to current time.
            last_change: The timestamp (ISO 8601) of the last change. The timestamp has to be in UTC (Coordinated 
                         Universal Time) and not local time. Defaults to current time.
            attributes: Named arguments which represent the optional attributes of the `Page` element.
        Returns:
            An empty PageXML object.
        """
        self.creator: str = "pypxml" if creator is None else str(creator)
        
        # class setters for the equivalent private values
        self.attributes = attributes  # height, width and filename have higher priority
        self.height = height
        self.width = width
        self.filename = filename
        self.xml = xml
        self.created = created
        self.last_change = last_change
        
        # initialize containers
        self.__reading_order: list[str] = []  # list of region id's in correct order
        self.__elements: list[PageElement] = []
        
    def __repr__(self) -> str:
        """ Returns a text representation of the object for debugging """
        return (f"PageXML(filename={self.__filename}, height={self.__height}, width={self.__width}, "
                f"attributes={str(self.__attributes)}, childs={len(self.__elements)}")
        
    def __str__(self) -> str:
        """ Returns a text representation of the object for printing """
        return f"<PageXML ({self.__filename})>"
    
    def __len__(self) -> int:
        """ Returns the number of child elements of this object (without reading order) """
        return len(self.__elements)
    
    def __iter__(self) -> PageElement:
        """ Iterate over all child elements of this object """
        self.__n = 0
        return self

    def __next__(self) -> PageElement:
        """ Yield next element """
        if self.__n < len(self.__elements):
            self.__n += 1
            return self.__elements[self.__n - 1]
        else:
            raise StopIteration
        
    def __getitem__(self, key: str) -> Optional[str]:
        """
        Get an attribute value by its key.
        Args:
            key: Key of an attribute.
        Returns:
            The value of the selected attribute. Returns None, if no match was found.
        """
        return self.__attributes.get(str(key), None)

    def __setitem__(self, key: str, value: Optional[str]) -> None:
        """
        Set an attribute value.
        Args:
            key: Key of the attribute.
            value: Value of the attribute. If the value is None, remove the attribute.
        """
        if value is None:
            self.__attributes.pop(str(key), None)
        else:
            self.__attributes[str(key)] = str(value)
        
    def __contains__(self, key: Union[PageElement, str]) -> bool:
        """
        Checks if an child element or an attribute exists.
        Args:
            key: Child element or attribute key.
        Returns:
            True, if either the passed child element or the attribute exists.
        """
        if isinstance(key, PageElement):
            return key in self.__elements
        else:
            key = str(key)
            return key in self.__attributes or key in ["imageFilename", "imageHeight", "imageWidth"]
        
    @property
    def height(self) -> int:
        """ The height of the image in pixels """
        return self.__height
    
    @height.setter
    def height(self, value: Union[str, int]) -> None:
        """ The height of the image in pixels """
        if isinstance(value, (str, int)):
            value = int(value)
            if value < 0:
                logger.warning("Negative imageWidth attribute was set to 0")
            self.__height = max(0, value)
        else:
            raise TypeError(f"Expected a integer or string, got {type(value).__name__}")
    
    @property
    def width(self) -> int:
        """ The width of the image in pixels """
        return self.__width
    
    @width.setter
    def width(self, value: Union[str, int]) -> None:
        """ The width of the image in pixels """
        if isinstance(value, (str, int)):
            value = int(value)
            if value < 0:
                logger.warning("Negative imageWidth attribute was set to 0")
            self.__width = max(0, value)
        else:
            raise TypeError(f"Expected a integer or string, got {type(value).__name__}")
        
    @property
    def filename(self) -> str:
        """ The name of the image file including the file extension """
        return self.__filename
    
    @filename.setter
    def filename(self, value: Union[Path, str]) -> None:
        """ The name of the image file including the file extension """
        if isinstance(value, (Path, str)):
            self.__filename = value if isinstance(value, str) else value.name
        else:
            raise TypeError(f"Expected a Path or string, got {type(value).__name__}") 
        
    @property
    def xml(self) -> Optional[Path]:
        """ Optionally, the path to the matching xml file """
        return self.__xml
    
    @xml.setter
    def xml(self, value: Optional[Union[Path, str]]) -> None:
        """ Optionally, the path to the matching xml file """
        if value is None:
            self.__xml = None
        elif isinstance(value, (Path, str)):
            self.__xml = Path(value).absolute()
        else:
            raise TypeError(f"Expected a Path or string, got {type(value).__name__}") 
    
    @property
    def created(self) -> str:
        """ The timestamp  (ISO 8601) of the creation of the PageXML file """
        return self.__created
    
    @created.setter
    def created(self, value: Optional[Union[str, datetime]]) -> None:
        """ The timestamp  (ISO 8601) of the creation of the PageXML file """
        if isinstance(value, datetime):
            self.__created: str = value.isoformat()
        elif isinstance(value, str):
            self.__created: str = value
        else:
            self.__created: str = datetime.now(timezone.utc).isoformat()
    
    @property
    def last_change(self) -> str:
        """ The timestamp (ISO 8601) of the last change """
        return self.__last_change
    
    @last_change.setter
    def last_change(self, value: Optional[Union[str, datetime]]) -> None:
        """ The timestamp (ISO 8601) of the last change """
        if isinstance(value, datetime):
            self.__last_change: str = value.isoformat()
        elif isinstance(value, str):
            self.__last_change: str = value
        else:
            self.__last_change: str = datetime.now(timezone.utc).isoformat()
    
    @property
    def attributes(self) -> dict[str, str]:
        """ Get a copy of the attributes of the page element """
        attribs = self.__attributes.copy()
        attribs["imageFilename"] = self.__filename
        attribs["imageHeight"] = str(self.__height)
        attribs["imageWidth"] = str(self.__width)
        return attribs
    
    @attributes.setter
    def attributes(self, attributes: Optional[dict[str, str]]) -> None:
        """ Set the attributes of the page element """
        self.__attributes = {} if attributes is None else {str(k): str(v) 
                                                           for k, v in attributes.items() if v is not None 
                                                           and k not in ["imageFilename", "imageHeight", "imageWidth"]}
        if "imageFilename" in attributes and attributes["imageFilename"] is not None:
            self.__filename = attributes["imageFilename"]
        if "imageHeight" in attributes and attributes["imageHeight"] is not None:
            self.__height = attributes["imageHeight"]
        if "imageWidth" in attributes and attributes["imageWidth"] is not None:
            self.__width = attributes["imageWidth"]
            
    @property
    def reading_order(self) -> list[str]:
        """ Returns a copy of the reading order of the page """
        return self.__reading_order.copy()
    
    @property
    def elements(self) -> list[PageElement]:
        """ A copy of the list of child elements """
        return self.__elements.copy()
    
    @property
    def regions(self) -> list[PageElement]:
        """ A copy of the list of child regions """
        return list([e for e in self.__elements if e.is_region])
    
    @classmethod
    def from_etree(cls, tree: etree.Element, raise_on_error: bool = True) -> Self:
        """
        Create a new PageXML object from an lxml etree object.
        Args:
            tree: lxml etree object.
            raise_on_error: If set to False, ignore parsing errors. Defaults to True.
        Raises:
            ValueError: If the element is not a valid PageXML element and raise_on_error is True.
        Returns:
            PageXML object that represents the passed etree element.
        """
        if (page := tree.find("./{*}Page")) is not None:
            attributes = {str(k): str(v) for k, v in dict(page.items()).items() 
                          if v is not None and k not in ["imageFilename", "imageHeight", "imageWidth"]}
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
            pagexml = cls(page.get("imageHeight"), page.get("imageWidth"), page.get("imageFilename"),
                          creator=creator, created=created, last_change=last_change, **attributes)
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
            schema_version: Which schema version to use. Available by default: "2017", "2019". Defaults to "2019".
            schema_file: Set a custom schema json file (see documentation for further information). Defaults to None.
        Returns:
            A lxml etree object that represents the PageXML object.
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
        page = etree.Element("Page", imageFilename=self.__filename, imageWidth=str(self.__width), 
                             imageHeight=str(self.__height), **self.__attributes)
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
        Create a new PageXML object from a PageXML file.
        Args:
            file: Path of the PageXML file.
            encoding: Set custom encoding. Defaults to "utf-8".
            raise_on_error: If set to False, ignore parsing errors. Defaults to True.
        Returns:
            PageXML object that represents the passed PageXML file.
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
        logger.info(f"PageXML written to {file}")
            
    def find_by_id(self, id: str, depth: int = 0) -> Optional[PageElement]:
        """
        Find a child element by its id.
        Args:
            id: Id of the element to find.
            depth: Depth level of the search. 
                   `0`: Search only the current level. 
                   `-1`: Search all levels recursively (no depth limit). 
                   `>0`: Limit the search to the specified number of levels deep.
        Returns:
            The PageElement object with the given ID. Returns None, if no match was found.
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
        Find elements by their type.
        Args:
            pagetype: Type of the elements to find.
            depth: Depth level of the search. 
                   `0`: Search only the current level. 
                   `-1`: Search all levels recursively (no depth limit). 
                   `>0`: Limit the search to the specified number of levels deep.
            attributes: Named arguments representing the attributes that the found elements must have.
        Returns:
            A list of PageElement objects with the given type. Returns an empty list, if no match was found.
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
        Create a new child element and add it to the list of elements.
        Args:
            pagetype: PageType of the new child element.
            index: If set, insert the new element at this index. Else append to the list. Defaults to None.
            attributes: Named arguments which represent the attributes of the `PageElement` object.
        Returns:
            The newly created child element.
        """
        element = PageElement(pagetype, parent=self, **attributes)
        self.set_element(element, index)
        return element
    
    def set_element(self, element: PageElement, index: Optional[int] = None, ro: bool = True) -> None:
        """
        Add an existing PageElement object to the list of elements.
        Args:
            element: The PageElement to add.
            index: If set, insert the element at this index. Else append to the list. Defaults to None.
            ro: If set to true, add the element to the reading order at the specified index.
                Only if the element is a region.
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
        Remove an element from the list of child elements.
        Args:
            element: The PageElement to remove.
        Returns:
            The removed element, if it was found. Else None.
        """
        if element in self.__elements:
            self.__elements.remove(element)
            if "id" in element and element["id"] in self.__reading_order:
                self.__reading_order.remove(element["id"])
            return element
        return None
    
    def clear_elements(self) -> None:
        """ Remove all elements from the list of child elements. This will also clear the reading order """
        self.__elements.clear()
        self.__reading_order.clear()
        
    def apply_reading_order(self) -> None:
        """ 
        Sorts the child elements based on the reading order. Non-region types are placed before regions and regions 
        not in the reading order are placed after the ordered regions
        """
        order = {_id: index for index, _id in enumerate(self.__reading_order)}  # improves performance over list.index()
        def sort_key(obj: PageElement):
            if not obj.is_region:  # non.region types (Such as AlternativeImage, ...) come first
                return (0, 0)
            elif "id" in obj and obj["id"] in order:  # the sorted regions come next
                return (1, order[obj["id"]])
            else:  # unordered regions at the end
                return (2, 0)
        self.__elements.sort(key=sort_key)

    def create_reading_order(self, overwrite: bool = False) -> None:
        """
        Creates a new reading order based on the current element order.
        Args:
            overwrite: If set to True, overwrites an existing reading order. 
                       False will only create an reading order if the current one is empty. Defaults to False.
        """
        if not self.__reading_order or overwrite:
            self.__reading_order = list([e["id"] for e in self.regions if "id" in e])
            
    def clear_reading_order(self) -> None:
        """ Remove all elements from the reading order without deleting the actual elements """
        self.__reading_order.clear()
        
    def set_reading_order(self, reading_order: Optional[list[str]], sync: bool = True) -> None:
        """
        Set the reading order of the PageXML.
        Args:
            reading_order: A list of region id's (Does not check for valid id's!). If an empty list or None is passed, 
                           clear the reading order.
            sync: Order the elements in the PageXML based on the passed reading order. Defaults to True.
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
        Sort the regions of the PageXML.
        Args:
            base: If set to `centroid`, the regions are sorted based on the direction and their centroid. 
                  If set to `minimum`, the minimum coordinate value in the sort direction is used. 
                  `Maximum` uses the maximum coordinate value in sort direction. Defaults to "minimum".
            direction: In which direction the regions are sorted. Defaults to "top-bottom".
            sync: Order the actual element order in the PageXML. If set to False, only write to the reading order.
                  Defaults to True.
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
            