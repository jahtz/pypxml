# Table of Contents

- [Table of Contents](#table-of-contents)
- [pypxml.pagexml](#pypxmlpagexml)
  - [PageXML Objects](#pagexml-objects)
      - [\_\_init\_\_](#__init__)
      - [\_\_repr\_\_](#__repr__)
      - [\_\_str\_\_](#__str__)
      - [\_\_len\_\_](#__len__)
      - [\_\_iter\_\_](#__iter__)
      - [\_\_next\_\_](#__next__)
      - [\_\_getitem\_\_](#__getitem__)
      - [\_\_setitem\_\_](#__setitem__)
      - [\_\_contains\_\_](#__contains__)
      - [imageHeight](#imageheight)
      - [imageHeight](#imageheight-1)
      - [imageWidth](#imagewidth)
      - [imageWidth](#imagewidth-1)
      - [imageFilename](#imagefilename)
      - [imageFilename](#imagefilename-1)
      - [xml](#xml)
      - [xml](#xml-1)
      - [created](#created)
      - [created](#created-1)
      - [last\_change](#last_change)
      - [last\_change](#last_change-1)
      - [attributes](#attributes)
      - [attributes](#attributes-1)
      - [reading\_order](#reading_order)
      - [elements](#elements)
      - [regions](#regions)
      - [from\_etree](#from_etree)
      - [to\_etree](#to_etree)
      - [from\_file](#from_file)
      - [to\_file](#to_file)
      - [find\_by\_id](#find_by_id)
      - [find\_by\_type](#find_by_type)
      - [create\_element](#create_element)
      - [set\_element](#set_element)
      - [delete\_element](#delete_element)
      - [clear\_elements](#clear_elements)
      - [apply\_reading\_order](#apply_reading_order)
      - [create\_reading\_order](#create_reading_order)
      - [clear\_reading\_order](#clear_reading_order)
      - [set\_reading\_order](#set_reading_order)
      - [sort\_reading\_order](#sort_reading_order)
- [pypxml.pageelement](#pypxmlpageelement)
  - [PageElement Objects](#pageelement-objects)
      - [\_\_init\_\_](#__init__-1)
      - [\_\_repr\_\_](#__repr__-1)
      - [\_\_str\_\_](#__str__-1)
      - [\_\_len\_\_](#__len__-1)
      - [\_\_iter\_\_](#__iter__-1)
      - [\_\_next\_\_](#__next__-1)
      - [\_\_getitem\_\_](#__getitem__-1)
      - [\_\_setitem\_\_](#__setitem__-1)
      - [\_\_contains\_\_](#__contains__-1)
      - [pagetype](#pagetype)
      - [pagetype](#pagetype-1)
      - [is\_region](#is_region)
      - [parent](#parent)
      - [attributes](#attributes-2)
      - [attributes](#attributes-3)
      - [elements](#elements-1)
      - [text](#text)
      - [text](#text-1)
      - [from\_etree](#from_etree-1)
      - [to\_etree](#to_etree-1)
      - [find\_by\_id](#find_by_id-1)
      - [find\_by\_type](#find_by_type-1)
      - [find\_coords](#find_coords)
      - [find\_baseline](#find_baseline)
      - [find\_text](#find_text)
      - [create\_element](#create_element-1)
      - [set\_element](#set_element-1)
      - [delete\_element](#delete_element-1)
      - [clear\_elements](#clear_elements-1)
- [pypxml.pagetype](#pypxmlpagetype)
  - [PageType Objects](#pagetype-objects)
      - [ReadingOrder](#readingorder)
      - [RegionRef](#regionref)
      - [OrderedGroup](#orderedgroup)
      - [UnorderedGroup](#unorderedgroup)
      - [OrderedGroupIndexed](#orderedgroupindexed)
      - [UnorderedGroupIndexed](#unorderedgroupindexed)
      - [RegionRefIndexed](#regionrefindexed)
      - [AdvertRegion](#advertregion)
      - [ChartRegion](#chartregion)
      - [ChemRegion](#chemregion)
      - [CustomRegion](#customregion)
      - [GraphicRegion](#graphicregion)
      - [ImageRegion](#imageregion)
      - [LineDrawingRegion](#linedrawingregion)
      - [MapRegion](#mapregion)
      - [MathsRegion](#mathsregion)
      - [MusicRegion](#musicregion)
      - [NoiseRegion](#noiseregion)
      - [SeparatorRegion](#separatorregion)
      - [TableRegion](#tableregion)
      - [TextRegion](#textregion)
      - [UnknownRegion](#unknownregion)
      - [AlternativeImage](#alternativeimage)
      - [Baseline](#baseline)
      - [Border](#border)
      - [Coords](#coords)
      - [Glyph](#glyph)
      - [GraphemeGroup](#graphemegroup)
      - [Grapheme](#grapheme)
      - [Grid](#grid)
      - [GridPoints](#gridpoints)
      - [Label](#label)
      - [Labels](#labels)
      - [Layer](#layer)
      - [Layers](#layers)
      - [Metadata](#metadata)
      - [NonPrintingChar](#nonprintingchar)
      - [PlainText](#plaintext)
      - [PrintSpace](#printspace)
      - [Relations](#relations)
      - [Roles](#roles)
      - [TextEquiv](#textequiv)
      - [TextLine](#textline)
      - [TextStyle](#textstyle)
      - [Unicode](#unicode)
      - [UserAttribute](#userattribute)
      - [UserDefined](#userdefined)
      - [Word](#word)

<a id="pypxml.pagexml"></a>

# pypxml.pagexml

<a id="pypxml.pagexml.PageXML"></a>

## PageXML Objects

```python
class PageXML()
```

Represents a PageXML file and the "Page" element.

<a id="pypxml.pagexml.PageXML.__init__"></a>

#### \_\_init\_\_

```python
def __init__(xml: Optional[Union[str, Path]] = None,
             creator: str = "pypxml",
             created: Optional[Union[str, datetime]] = None,
             last_change: Optional[Union[str, datetime]] = None,
             **attributes: str) -> Self
```

Create a new empty PageXML object.

**Arguments**:

  If a Path object is provided, only the filename is used.
- `xml` - Optionally, the path to the matching XML file can be provided. Defaults to None.
- `creator` - The creator of the PageXML. Defaults to "pypxml".
- `created` - The timestamp (ISO 8601) of the creation of the PageXML file. The timestamp must be in UTC
  (Coordinated Universal Time) and not local time. Defaults to the current time.
- `last_change` - The timestamp (ISO 8601) of the last change. The timestamp must be in UTC
  (Coordinated Universal Time) and not local time. Defaults to the current time.
- `attributes` - Named arguments that represent the optional attributes of the "Page" element.

**Returns**:

  An empty PageXML object.

<a id="pypxml.pagexml.PageXML.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Returns a text representation of the object for debugging.

<a id="pypxml.pagexml.PageXML.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a text representation of the object for printing.

<a id="pypxml.pagexml.PageXML.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of child elements of this object (excluding the reading order).

<a id="pypxml.pagexml.PageXML.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> PageElement
```

Iterates over all child elements of this object.

<a id="pypxml.pagexml.PageXML.__next__"></a>

#### \_\_next\_\_

```python
def __next__() -> PageElement
```

Yields the next element.

<a id="pypxml.pagexml.PageXML.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: str) -> Optional[str]
```

Gets an attribute value by its key.

**Arguments**:

- `key` - The key of an attribute.

**Returns**:

  The value of the selected attribute. Returns None if no match is found.

<a id="pypxml.pagexml.PageXML.__setitem__"></a>

#### \_\_setitem\_\_

```python
def __setitem__(key: str, value: Optional[str]) -> None
```

Sets an attribute value.

**Arguments**:

- `key` - The key of the attribute.
- `value` - The value of the attribute. If the value is None, the attribute is removed.

<a id="pypxml.pagexml.PageXML.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(key: Union[PageElement, str]) -> bool
```

Checks if a child element or an attribute exists.

**Arguments**:

- `key` - A child element or attribute key.

**Returns**:

  True if the passed child element or attribute exists.

<a id="pypxml.pagexml.PageXML.height"></a>

#### imageHeight

```python
@property
def imageHeight() -> int
```

The height of the image in pixels.

<a id="pypxml.pagexml.PageXML.height"></a>

#### imageHeight

```python
@imageHeight.setter
def imageHeight(value: Union[str, int]) -> None
```

Sets the height of the image in pixels.

<a id="pypxml.pagexml.PageXML.width"></a>

#### imageWidth

```python
@property
def imageWidth() -> int
```

The width of the image in pixels.

<a id="pypxml.pagexml.PageXML.width"></a>

#### imageWidth

```python
@imageWidth.setter
def imageWidth(value: Union[str, int]) -> None
```

Sets the width of the image in pixels.

<a id="pypxml.pagexml.PageXML.filename"></a>

#### imageFilename

```python
@property
def imageFilename() -> str
```

The name of the image file, including the file extension.

<a id="pypxml.pagexml.PageXML.filename"></a>

#### imageFilename

```python
@imageFilename.setter
def imageFilename(value: Union[Path, str]) -> None
```

Sets the name of the image file, including the file extension.

<a id="pypxml.pagexml.PageXML.xml"></a>

#### xml

```python
@property
def xml() -> Optional[Path]
```

Optionally, the path to the matching XML file.

<a id="pypxml.pagexml.PageXML.xml"></a>

#### xml

```python
@xml.setter
def xml(value: Optional[Union[Path, str]]) -> None
```

Sets the path to the matching XML file.

<a id="pypxml.pagexml.PageXML.created"></a>

#### created

```python
@property
def created() -> str
```

The timestamp (ISO 8601) of the creation of the PageXML file.

<a id="pypxml.pagexml.PageXML.created"></a>

#### created

```python
@created.setter
def created(value: Optional[Union[str, datetime]]) -> None
```

Sets the timestamp (ISO 8601) of the creation of the PageXML file.

<a id="pypxml.pagexml.PageXML.last_change"></a>

#### last\_change

```python
@property
def last_change() -> str
```

The timestamp (ISO 8601) of the last change.

<a id="pypxml.pagexml.PageXML.last_change"></a>

#### last\_change

```python
@last_change.setter
def last_change(value: Optional[Union[str, datetime]]) -> None
```

Sets the timestamp (ISO 8601) of the last change.

<a id="pypxml.pagexml.PageXML.attributes"></a>

#### attributes

```python
@property
def attributes() -> dict[str, str]
```

Gets a copy of the attributes of the page element.

<a id="pypxml.pagexml.PageXML.attributes"></a>

#### attributes

```python
@attributes.setter
def attributes(attributes: Optional[dict[str, str]]) -> None
```

Sets the attributes of the page element.

<a id="pypxml.pagexml.PageXML.reading_order"></a>

#### reading\_order

```python
@property
def reading_order() -> list[str]
```

Returns a copy of the reading order of the page.

<a id="pypxml.pagexml.PageXML.elements"></a>

#### elements

```python
@property
def elements() -> list[PageElement]
```

Returns a copy of the list of child elements.

<a id="pypxml.pagexml.PageXML.regions"></a>

#### regions

```python
@property
def regions() -> list[PageElement]
```

Returns a copy of the list of child regions.

<a id="pypxml.pagexml.PageXML.from_etree"></a>

#### from\_etree

```python
@classmethod
def from_etree(cls, tree: etree.Element, raise_on_error: bool = True) -> Self
```

Creates a new PageXML object from an lxml etree object.

**Arguments**:

- `tree` - An lxml etree object.
- `raise_on_error` - If set to False, parsing errors are ignored. Defaults to True.

**Raises**:

- `ValueError` - If the element is not a valid PageXML element and raise_on_error is True.

**Returns**:

  A PageXML object that represents the passed etree element.

<a id="pypxml.pagexml.PageXML.to_etree"></a>

#### to\_etree

```python
def to_etree(schema_version: str = "2019",
             schema_file: Optional[Union[Path, str]] = None) -> etree.Element
```

Returns the PageXML object as an lxml etree object.

**Arguments**:

- `schema_version` - The schema version to use. Available by default: "2017", "2019". Defaults to "2019".
- `schema_file` - A custom schema JSON file (see documentation for further information). Defaults to None.

**Returns**:

  An lxml etree object that represents the PageXML object.

<a id="pypxml.pagexml.PageXML.from_file"></a>

#### from\_file

```python
@classmethod
def from_file(cls,
              file: Union[Path, str],
              encoding: str = "utf-8",
              raise_on_error: bool = True) -> Self
```

Creates a new PageXML object from a PageXML file.

**Arguments**:

- `file` - The path of the PageXML file.
- `encoding` - Custom encoding. Defaults to "utf-8".
- `raise_on_error` - If set to False, parsing errors are ignored. Defaults to True.

**Returns**:

  A PageXML object that represents the passed PageXML file.

<a id="pypxml.pagexml.PageXML.to_file"></a>

#### to\_file

```python
def to_file(file: Union[Path, str],
            encoding="utf-8",
            schema_version: str = "2019",
            schema_file: Optional[Union[Path, str]] = None) -> None
```

Writes the PageXML object to a file.

**Arguments**:

- `file` - The file path to write the PageXML object to.
- `encoding` - Custom encoding. Defaults to "utf-8".
- `schema_version` - The schema version to use. Available by default: "2017", "2019". Defaults to "2019".
- `schema_file` - A custom schema JSON file (see documentation for further information). Defaults to None.

<a id="pypxml.pagexml.PageXML.find_by_id"></a>

#### find\_by\_id

```python
def find_by_id(id: str, depth: int = 0) -> Optional[PageElement]
```

Finds a child element by its ID.

**Arguments**:

- `id` - The ID of the element to find.
- `depth` - The depth level of the search.
  "0" searches only the current level.
  "-1" searches all levels recursively (no depth limit).
  ">0" limits the search to the specified number of levels deep.

**Returns**:

  The PageElement object with the given ID. Returns None if no match is found.

<a id="pypxml.pagexml.PageXML.find_by_type"></a>

#### find\_by\_type

```python
def find_by_type(pagetype: Union[PageType, list[PageType]],
                 depth: int = 0,
                 **attributes: str) -> list[PageElement]
```

Finds elements by their type.

**Arguments**:

- `pagetype` - The type of the elements to find.
- `depth` - The depth level of the search.
  "0" searches only the current level.
  "-1" searches all levels recursively (no depth limit).
  ">0" limits the search to the specified number of levels deep.
- `attributes` - Named arguments representing the attributes that the found elements must have.

**Returns**:

  A list of PageElement objects with the given type. Returns an empty list if no match is found.

<a id="pypxml.pagexml.PageXML.create_element"></a>

#### create\_element

```python
def create_element(pagetype: PageType,
                   index: Optional[int] = None,
                   **attributes: str) -> PageElement
```

Creates a new child element and adds it to the list of elements.

**Arguments**:

- `pagetype` - The PageType of the new child element.
- `index` - If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
- `attributes` - Named arguments that represent the attributes of the "PageElement" object.

**Returns**:

  The newly created child element.

<a id="pypxml.pagexml.PageXML.set_element"></a>

#### set\_element

```python
def set_element(element: PageElement,
                index: Optional[int] = None,
                ro: bool = True) -> None
```

Adds an existing PageElement object to the list of elements.

**Arguments**:

- `element` - The PageElement to add.
- `index` - If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.
- `ro` - If set to True, adds the element to the reading order at the specified index.
  Only applies if the element is a region.

<a id="pypxml.pagexml.PageXML.delete_element"></a>

#### delete\_element

```python
def delete_element(element: PageElement) -> Optional[PageElement]
```

Removes an element from the list of child elements.

**Arguments**:

- `element` - The PageElement to remove.

**Returns**:

  The removed element if it was found. Otherwise, None.

<a id="pypxml.pagexml.PageXML.clear_elements"></a>

#### clear\_elements

```python
def clear_elements() -> None
```

Removes all elements from the list of child elements. This also clears the reading order.

<a id="pypxml.pagexml.PageXML.apply_reading_order"></a>

#### apply\_reading\_order

```python
def apply_reading_order() -> None
```

Sorts the child elements based on the current reading order.

Non-region elements are placed first, followed by regions according to the reading order.
Regions not included in the reading order are placed last.

<a id="pypxml.pagexml.PageXML.create_reading_order"></a>

#### create\_reading\_order

```python
def create_reading_order(force: bool = False) -> None
```

Creates a new reading order based on the current element sequence.

**Arguments**:

- `force` - If True, overwrites any existing reading order. If False, only creates a new reading order if none
  currently exists. Defaults to False.

<a id="pypxml.pagexml.PageXML.clear_reading_order"></a>

#### clear\_reading\_order

```python
def clear_reading_order() -> None
```

Removes all elements from the reading order without deleting the actual elements.

<a id="pypxml.pagexml.PageXML.set_reading_order"></a>

#### set\_reading\_order

```python
def set_reading_order(reading_order: Optional[list[str]],
                      sync: bool = True) -> None
```

Updates the reading order of regions in the PageXML document.

**Arguments**:

- `reading_order` - A list of region IDs defining the desired reading order. If an empty list or None is
  provided, the reading order is cleared. (Note: Validity of IDs is not checked.)
- `sync` - If True, orders the elements in the PageXML based on the passed reading order. Defaults to True.

<a id="pypxml.pagexml.PageXML.sort_reading_order"></a>

#### sort\_reading\_order

```python
def sort_reading_order(base: Literal["minimum", "maximum",
                                     "centroid"] = "minimum",
                       direction: Literal["top-bottom", "bottom-top",
                                          "left-right",
                                          "right-left"] = "top-bottom",
                       sync: bool = True) -> None
```

Sorts the regions in the PageXML document by their location on the page.

**Arguments**:

- `base` - The method for determining the reference point used for sorting:
  "minimum" sorts by the minimum coordinate value in the given direction.
  "maximum" sorts by the maximum coordinate value in the given direction.
  "centroid" sorts by the centroid position of each region. Defaults to "minimum".
- `direction` - The primary direction in which regions are sorted. Defaults to "top-bottom".
- `sync` - If True, also reorders the physical sequence of region elements in the PageXML. If False, only updates
  the reading order element without changing the actual XML element order. Defaults to True.

<a id="pypxml.pageelement"></a>

# pypxml.pageelement

<a id="pypxml.pageelement.PageElement"></a>

## PageElement Objects

```python
class PageElement()
```

Represents a PageXML element within the "Page" element.

<a id="pypxml.pageelement.PageElement.__init__"></a>

#### \_\_init\_\_

```python
def __init__(pagetype: PageType, parent: Union["PageXML", Self],
             **attributes: str) -> Self
```

Creates a new empty PageElement object.

**Arguments**:

- `pagetype` - The type of the PageElement.
- `parent` - The parent element of the page element.
- `attributes` - Named arguments that represent the attributes of the "PageElement" object.

**Returns**:

  An empty PageElement object.

<a id="pypxml.pageelement.PageElement.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Returns a text representation of the object for debugging.

<a id="pypxml.pageelement.PageElement.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a text representation of the object for printing.

<a id="pypxml.pageelement.PageElement.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of child elements of this object.

<a id="pypxml.pageelement.PageElement.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Self
```

Iterates over all child elements of this object.

<a id="pypxml.pageelement.PageElement.__next__"></a>

#### \_\_next\_\_

```python
def __next__() -> Self
```

Yields the next element.

<a id="pypxml.pageelement.PageElement.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: str) -> Optional[str]
```

Gets an attribute value by its key.

**Arguments**:

- `key` - The key of an attribute.

**Returns**:

  The value of the selected attribute. Returns None if no match is found.

<a id="pypxml.pageelement.PageElement.__setitem__"></a>

#### \_\_setitem\_\_

```python
def __setitem__(key: str, value: Optional[str]) -> None
```

Sets an attribute value.

**Arguments**:

- `key` - The key of the attribute.
- `value` - The value of the attribute. If the value is None, the attribute is removed.

<a id="pypxml.pageelement.PageElement.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(key: Union[Self, str]) -> bool
```

Checks if a child element or an attribute exists.

**Arguments**:

- `key` - A child element or attribute key.

**Returns**:

  True if the passed child element or attribute exists.

<a id="pypxml.pageelement.PageElement.pagetype"></a>

#### pagetype

```python
@property
def pagetype() -> PageType
```

The type of the PageElement object.

<a id="pypxml.pageelement.PageElement.pagetype"></a>

#### pagetype

```python
@pagetype.setter
def pagetype(pagetype: Union[PageType, str]) -> None
```

Sets the type of the PageElement object.

<a id="pypxml.pageelement.PageElement.is_region"></a>

#### is\_region

```python
@property
def is_region() -> bool
```

Checks if the PageElement object is a region.

<a id="pypxml.pageelement.PageElement.parent"></a>

#### parent

```python
@property
def parent() -> Union["PageXML", Self]
```

The parent of the PageElement object. This may be a PageXML or PageElement object.

<a id="pypxml.pageelement.PageElement.attributes"></a>

#### attributes

```python
@property
def attributes() -> dict[str, str]
```

A dictionary containing key/value pairs that represent XML attributes.

<a id="pypxml.pageelement.PageElement.attributes"></a>

#### attributes

```python
@attributes.setter
def attributes(attributes: Optional[dict[str, str]]) -> None
```

Sets the dictionary containing key/value pairs that represent XML attributes.

<a id="pypxml.pageelement.PageElement.elements"></a>

#### elements

```python
@property
def elements() -> list[Self]
```

Returns a copy of the list of child elements.

<a id="pypxml.pageelement.PageElement.text"></a>

#### text

```python
@property
def text() -> Optional[str]
```

The stored text.

<a id="pypxml.pageelement.PageElement.text"></a>

#### text

```python
@text.setter
def text(value: Optional[str]) -> None
```

Sets the stored text.

<a id="pypxml.pageelement.PageElement.from_etree"></a>

#### from\_etree

```python
@classmethod
def from_etree(cls,
               tree: etree.Element,
               parent: Union["PageXML", Self],
               raise_on_error: bool = True) -> Self
```

Creates a new PageElement object from an etree element.

**Arguments**:

- `tree` - An lxml etree object.
- `parent` - The parent element of this page element.
- `raise_on_error` - If set to False, parsing errors are ignored. Defaults to True.

**Raises**:

- `ValueError` - If the element is not a valid PageXML element and raise_on_error is True.

**Returns**:

  A PageElement object that represents the passed etree element.

<a id="pypxml.pageelement.PageElement.to_etree"></a>

#### to\_etree

```python
def to_etree() -> etree.Element
```

Converts the PageElement object to an etree element.

**Returns**:

  An lxml etree object that represents this PageElement object.

<a id="pypxml.pageelement.PageElement.find_by_id"></a>

#### find\_by\_id

```python
def find_by_id(id: str, depth: int = 0) -> Optional[Self]
```

Finds a child element by its ID.

**Arguments**:

- `id` - The ID of the element to find.
- `depth` - The depth level of the search.
  "0" searches only the current level.
  "-1" searches all levels recursively (no depth limit).
  ">0" limits the search to the specified number of levels deep.

**Returns**:

  The PageElement object with the given ID. Returns None if no match is found.

<a id="pypxml.pageelement.PageElement.find_by_type"></a>

#### find\_by\_type

```python
def find_by_type(pagetype: Union[PageType, list[PageType]],
                 depth: int = 0,
                 **attributes: str) -> list[Self]
```

Finds elements by their type.

**Arguments**:

- `pagetype` - The type of the elements to find.
- `depth` - The depth level of the search.
  "0" searches only the current level.
  "-1" searches all levels recursively (no depth limit).
  ">0" limits the search to the specified number of levels deep.
- `attributes` - Named arguments representing the attributes that the found elements must have.

**Returns**:

  A list of PageElement objects with the given type. Returns an empty list if no match is found.

<a id="pypxml.pageelement.PageElement.find_coords"></a>

#### find\_coords

```python
def find_coords() -> Optional[Self]
```

Finds the coords element of the current element.

**Returns**:

  The PageType.Coords element of the current object if it exists as a direct child.

<a id="pypxml.pageelement.PageElement.find_baseline"></a>

#### find\_baseline

```python
def find_baseline() -> Optional[Self]
```

Finds the baseline element of the current element.

**Returns**:

  The PageType.Baseline element of the current object if it exists as a direct child.

<a id="pypxml.pageelement.PageElement.find_text"></a>

#### find\_text

```python
def find_text(
    index: Optional[int] = None,
    source: Literal[PageType.Unicode, PageType.PlainText] = PageType.Unicode
) -> Optional[str]
```

Finds the text of the current element.

**Arguments**:

- `index` - Selects a certain TextEquiv element index. If index is not set and multiple TextEquiv elements are
  found, the first one with the lowest or no index is picked. Only applied if the current element is
  a level above the TextEquivs.
- `source` - Selects whether the text from Unicode or PlainText is picked.

**Returns**:

  The text of the current element if it was found.

<a id="pypxml.pageelement.PageElement.create_element"></a>

#### create\_element

```python
def create_element(pagetype: PageType,
                   index: Optional[int] = None,
                   **attributes: str) -> Self
```

Creates a new child element and adds it to the list of elements.

**Arguments**:

- `pagetype` - The PageType of the new child element.
- `index` - If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
- `attributes` - Named arguments that represent the attributes of the "PageElement" object.

**Returns**:

  The newly created child element.

<a id="pypxml.pageelement.PageElement.set_element"></a>

#### set\_element

```python
def set_element(element: Self, index: Optional[int] = None) -> None
```

Adds an existing PageElement object to the list of child elements.

**Arguments**:

- `element` - The PageElement to add as a child element.
- `index` - If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.

<a id="pypxml.pageelement.PageElement.delete_element"></a>

#### delete\_element

```python
def delete_element(element: Self) -> Optional[Self]
```

Removes an element from the list of child elements.

**Arguments**:

- `element` - The PageElement to remove.

**Returns**:

  The removed element if it was found. Otherwise, None.

<a id="pypxml.pageelement.PageElement.clear_elements"></a>

#### clear\_elements

```python
def clear_elements() -> None
```

Removes all elements from the list of child elements.

<a id="pypxml.pagetype"></a>

# pypxml.pagetype

<a id="pypxml.pagetype.PageType"></a>

## PageType Objects

```python
class PageType(Enum)
```

Reference: https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page

<a id="pypxml.pagetype.PageType.ReadingOrder"></a>

#### ReadingOrder

Definition of the reading order within the page. To express a reading order between elements they have to be 
included in an OrderedGroup. Groups may contain further groups.

<a id="pypxml.pagetype.PageType.RegionRef"></a>

#### RegionRef

Region reference.

<a id="pypxml.pagetype.PageType.OrderedGroup"></a>

#### OrderedGroup

Numbered group (contains ordered elements).

<a id="pypxml.pagetype.PageType.UnorderedGroup"></a>

#### UnorderedGroup

Numbered group (contains ordered elements)

<a id="pypxml.pagetype.PageType.OrderedGroupIndexed"></a>

#### OrderedGroupIndexed

Indexed group containing ordered elements.

<a id="pypxml.pagetype.PageType.UnorderedGroupIndexed"></a>

#### UnorderedGroupIndexed

Indexed group containing unordered elements.

<a id="pypxml.pagetype.PageType.RegionRefIndexed"></a>

#### RegionRefIndexed

Numbered region.

<a id="pypxml.pagetype.PageType.AdvertRegion"></a>

#### AdvertRegion

Regions containing advertisements.

<a id="pypxml.pagetype.PageType.ChartRegion"></a>

#### ChartRegion

Regions containing charts or graphs of any type, should be marked as chart regions.

<a id="pypxml.pagetype.PageType.ChemRegion"></a>

#### ChemRegion

Regions containing chemical formulas.

<a id="pypxml.pagetype.PageType.CustomRegion"></a>

#### CustomRegion

Regions containing content that is not covered by the default types (text, graphic, image, line drawing, chart, 
table, separator, maths, map, music, chem, advert, noise, unknown).

<a id="pypxml.pagetype.PageType.GraphicRegion"></a>

#### GraphicRegion

Regions containing simple graphics, such as company logo, should be marked as graphic regions.

<a id="pypxml.pagetype.PageType.ImageRegion"></a>

#### ImageRegion

An image is considered to be more intricated and complex than a graphic. These can be photos or drawings.

<a id="pypxml.pagetype.PageType.LineDrawingRegion"></a>

#### LineDrawingRegion

A line drawing is a single colour illustration without solid areas.

<a id="pypxml.pagetype.PageType.MapRegion"></a>

#### MapRegion

Regions containing maps.

<a id="pypxml.pagetype.PageType.MathsRegion"></a>

#### MathsRegion

Regions containing equations and mathematical symbols should be marked as maths regions.

<a id="pypxml.pagetype.PageType.MusicRegion"></a>

#### MusicRegion

Regions containing musical notations.

<a id="pypxml.pagetype.PageType.NoiseRegion"></a>

#### NoiseRegion

Noise regions are regions where no real data lies, only false data created by artifacts on the document or scanner 
noise.

<a id="pypxml.pagetype.PageType.SeparatorRegion"></a>

#### SeparatorRegion

Separators are lines that lie between columns and paragraphs and can be used to logically separate different 
articles from each other.

<a id="pypxml.pagetype.PageType.TableRegion"></a>

#### TableRegion

Tabular data in any form is represented with a table region. Rows and columns may or may not have separator lines; 
these lines are not separator regions.

<a id="pypxml.pagetype.PageType.TextRegion"></a>

#### TextRegion

Pure text is represented as a text region. This includes drop capitals, but practically ornate text may be 
considered as a graphic.

<a id="pypxml.pagetype.PageType.UnknownRegion"></a>

#### UnknownRegion

To be used if the region type cannot be ascertained.

<a id="pypxml.pagetype.PageType.AlternativeImage"></a>

#### AlternativeImage

Alternative region images (e.g. black-and-white)

<a id="pypxml.pagetype.PageType.Baseline"></a>

#### Baseline

Multiple connected points that mark the baseline of the glyphs.

<a id="pypxml.pagetype.PageType.Border"></a>

#### Border

Border of the actual page (if the scanned image contains parts not belonging to the page).

<a id="pypxml.pagetype.PageType.Coords"></a>

#### Coords

Polygon outline of the element as a path of points. No points may lie outside the outline of its parent, which in 
the case of Border is the bounding rectangle of the root image. Paths are closed by convention, i.e. the last point 
logically connects with the first (and at least 3 points are required to span an area). 
Paths must be planar (i.e. must not self-intersect).

<a id="pypxml.pagetype.PageType.Glyph"></a>

#### Glyph

No official annotation.

<a id="pypxml.pagetype.PageType.GraphemeGroup"></a>

#### GraphemeGroup

No official annotation.

<a id="pypxml.pagetype.PageType.Grapheme"></a>

#### Grapheme

No official annotation.

<a id="pypxml.pagetype.PageType.Grid"></a>

#### Grid

Table grid (visible or virtual grid lines).

<a id="pypxml.pagetype.PageType.GridPoints"></a>

#### GridPoints

One row in the grid point matrix. Points with x,y coordinates.

<a id="pypxml.pagetype.PageType.Label"></a>

#### Label

A semantic label / tag

<a id="pypxml.pagetype.PageType.Labels"></a>

#### Labels

Semantic labels / tags

<a id="pypxml.pagetype.PageType.Layer"></a>

#### Layer

No official annotation.

<a id="pypxml.pagetype.PageType.Layers"></a>

#### Layers

Unassigned regions are considered to be in the (virtual) default layer which is to be treated as below any other 
layers.

<a id="pypxml.pagetype.PageType.Metadata"></a>

#### Metadata

No official annotation.

<a id="pypxml.pagetype.PageType.NonPrintingChar"></a>

#### NonPrintingChar

A glyph component without visual representation but with Unicode code point. 
Non-visual / non-printing / control character. Part of grapheme container (of glyph) or grapheme sub group.

<a id="pypxml.pagetype.PageType.PlainText"></a>

#### PlainText

Text in a "simple" form (ASCII or extended ASCII as mostly used for typing). I.e. no use of special characters for 
ligatures (should be stored as two separate characters) etc.

<a id="pypxml.pagetype.PageType.PrintSpace"></a>

#### PrintSpace

Determines the effective area on the paper of a printed page. Its size is equal for all pages of a book 
(exceptions: titlepage, multipage pictures). It contains all living elements (except marginals) like body type, 
footnotes, headings, running titles. It does not contain pagenumber (if not part of running title), marginals, 
signature mark, preview words.

<a id="pypxml.pagetype.PageType.Relations"></a>

#### Relations

Container for one-to-one relations between layout objects (for example: DropCap - paragraph, caption - image).

<a id="pypxml.pagetype.PageType.Roles"></a>

#### Roles

Roles the region takes (e.g. in context of a parent region)

<a id="pypxml.pagetype.PageType.TextEquiv"></a>

#### TextEquiv

No official annotation.

<a id="pypxml.pagetype.PageType.TextLine"></a>

#### TextLine

No official annotation.

<a id="pypxml.pagetype.PageType.TextStyle"></a>

#### TextStyle

Monospace (fixed-pitch, non-proportional) or proportional font.

<a id="pypxml.pagetype.PageType.Unicode"></a>

#### Unicode

Correct encoding of the original, always using the corresponding Unicode code point. I.e. ligatures have to be 
represented as one character etc.

<a id="pypxml.pagetype.PageType.UserAttribute"></a>

#### UserAttribute

Structured custom data defined by name, type and value.

<a id="pypxml.pagetype.PageType.UserDefined"></a>

#### UserDefined

Container for user-defined attributes.

<a id="pypxml.pagetype.PageType.Word"></a>

#### Word

No official annotation.

