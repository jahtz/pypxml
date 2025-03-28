# Table of Contents
- [Table of Contents](#table-of-contents)
- [pypxml.pagelement](#pypxmlpagelement)
  - [PageElement Objects](#pageelement-objects)
      - [\_\_init\_\_](#__init__)
      - [\_\_str\_\_](#__str__)
      - [\_\_repr\_\_](#__repr__)
      - [\_\_len\_\_](#__len__)
      - [\_\_iter\_\_](#__iter__)
      - [\_\_next\_\_](#__next__)
      - [\_\_getitem\_\_](#__getitem__)
      - [\_\_setitem\_\_](#__setitem__)
      - [\_\_contains\_\_](#__contains__)
      - [pagetype](#pagetype)
      - [pagetype](#pagetype-1)
      - [parent](#parent)
      - [attributes](#attributes)
      - [attributes](#attributes-1)
      - [elements](#elements)
      - [text](#text)
      - [text](#text-1)
      - [new](#new)
      - [from\_etree](#from_etree)
      - [to\_etree](#to_etree)
      - [find\_by\_id](#find_by_id)
      - [find\_by\_type](#find_by_type)
      - [create\_element](#create_element)
      - [get\_element](#get_element)
      - [set\_element](#set_element)
      - [remove\_element](#remove_element)
      - [clear\_elements](#clear_elements)
      - [get\_attribute](#get_attribute)
      - [set\_attribute](#set_attribute)
      - [remove\_attribute](#remove_attribute)
      - [clear\_attributes](#clear_attributes)
      - [is\_region](#is_region)
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
      - [Graphemes](#graphemes)
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
      - [is\_valid](#is_valid)
      - [is\_region](#is_region-1)
- [pypxml.pagexml](#pypxmlpagexml)
  - [PageXML Objects](#pagexml-objects)
      - [\_\_init\_\_](#__init__-1)
      - [\_\_str\_\_](#__str__-1)
      - [\_\_repr\_\_](#__repr__-1)
      - [\_\_len\_\_](#__len__-1)
      - [\_\_iter\_\_](#__iter__-1)
      - [\_\_next\_\_](#__next__-1)
      - [\_\_getitem\_\_](#__getitem__-1)
      - [\_\_setitem\_\_](#__setitem__-1)
      - [\_\_contains\_\_](#__contains__-1)
      - [creator](#creator)
      - [creator](#creator-1)
      - [created](#created)
      - [created](#created-1)
      - [changed](#changed)
      - [changed](#changed-1)
      - [attributes](#attributes-2)
      - [attributes](#attributes-3)
      - [elements](#elements-1)
      - [regions](#regions)
      - [reading\_order](#reading_order)
      - [reading\_order](#reading_order-1)
      - [xml](#xml)
      - [xml](#xml-1)
      - [new](#new-1)
      - [from\_etree](#from_etree-1)
      - [from\_file](#from_file)
      - [to\_etree](#to_etree-1)
      - [to\_file](#to_file)
      - [find\_by\_id](#find_by_id-1)
      - [find\_by\_type](#find_by_type-1)
      - [create\_element](#create_element-1)
      - [get\_element](#get_element-1)
      - [set\_element](#set_element-1)
      - [remove\_element](#remove_element-1)
      - [clear\_elements](#clear_elements-1)
      - [get\_attribute](#get_attribute-1)
      - [set\_attribute](#set_attribute-1)
      - [remove\_attribute](#remove_attribute-1)
      - [clear\_attributes](#clear_attributes-1)

<a id="pypxml.pagelement"></a>

# pypxml.pagelement

<a id="pypxml.pagelement.PageElement"></a>

## PageElement Objects

```python
class PageElement()
```

PageXML Element class.

<a id="pypxml.pagelement.PageElement.__init__"></a>

#### \_\_init\_\_

```python
def __init__(pagetype: PageType, parent: Union["PageXML", Self],
             **attributes: str)
```

PLEASE USE THE .new() METHOD TO CREATE A NEW PAGEELEMENT OBJECT.
This constructor is only for internal use.

**Arguments**:

- `pagetype` - The type of the page element.
- `parent` - The parent element of the page element.
- `attributes` - Named arguments which represent the attributes of the `PageElement` object.

<a id="pypxml.pagelement.PageElement.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns the string representation of the PageElement object.

<a id="pypxml.pagelement.PageElement.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Returns the string representation of the PageElement object.

<a id="pypxml.pagelement.PageElement.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number elements in this element.

<a id="pypxml.pagelement.PageElement.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Self
```

Iterate over all elements in this element.

<a id="pypxml.pagelement.PageElement.__next__"></a>

#### \_\_next\_\_

```python
def __next__() -> Self
```

Yield next element.

<a id="pypxml.pagelement.PageElement.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Union[int, str]) -> Optional[Union[Self, str]]
```

Get an PageElement object by its index or an attribute value by its key

**Arguments**:

- `key` - Index (integer) of an PageElement object or a key (string) of an attribute.

**Returns**:

  The PageElement of passed index (returns last object if the key is out of range) or the value of the
  selected attribute. Returns None, if no match was found.

<a id="pypxml.pagelement.PageElement.__setitem__"></a>

#### \_\_setitem\_\_

```python
def __setitem__(key: Union[int, str], value: Union[Self, str]) -> None
```

Set an PageElement object or an attribute value.

**Arguments**:

- `key` - Index (integer) for an PageElement object or a key (string) for an attribute.
- `value` - PageElement object (if key is of type integer) or a string (if key is of type string).

<a id="pypxml.pagelement.PageElement.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(key: Union[Self, str]) -> bool
```

Checks if an PageElement object or an attribute exists.

**Arguments**:

- `key` - PageElement object or attribute key.

**Returns**:

  True, if either the passed PageElement object or the attribute exists. Else return False.

<a id="pypxml.pagelement.PageElement.pagetype"></a>

#### pagetype

```python
@property
def pagetype() -> PageType
```

Get the type of the page element.

<a id="pypxml.pagelement.PageElement.pagetype"></a>

#### pagetype

```python
@pagetype.setter
def pagetype(pagetype: PageType) -> None
```

Set the type of the page element.

<a id="pypxml.pagelement.PageElement.parent"></a>

#### parent

```python
@property
def parent() -> Union["PageXML", Self]
```

Get the parent of the page element.

<a id="pypxml.pagelement.PageElement.attributes"></a>

#### attributes

```python
@property
def attributes() -> dict[str, str]
```

Get the attributes of the page element.

<a id="pypxml.pagelement.PageElement.attributes"></a>

#### attributes

```python
@attributes.setter
def attributes(attributes: dict[str, str]) -> None
```

Set the attributes of the page element.

<a id="pypxml.pagelement.PageElement.elements"></a>

#### elements

```python
@property
def elements() -> list[Self]
```

Returns a copy of the elements list.

<a id="pypxml.pagelement.PageElement.text"></a>

#### text

```python
@property
def text() -> Optional[str]
```

XML element text.

<a id="pypxml.pagelement.PageElement.text"></a>

#### text

```python
@text.setter
def text(value: Optional[str]) -> None
```

XML element text.

<a id="pypxml.pagelement.PageElement.new"></a>

#### new

```python
@classmethod
def new(cls,
        pagetype: PageType,
        parent: Optional[Union["PageXML", Self]] = None,
        **attributes: str) -> Self
```

Create a new empty PageElement object.

**Arguments**:

- `creator` - Set a custom PageXML `Metadata` creator. Defaults to "pypxml".
- `parent` - The parent element of the page element.
- `attributes` - Named arguments which represent the attributes of the `PageElement` object.

**Returns**:

  A empty PageXML object.

<a id="pypxml.pagelement.PageElement.from_etree"></a>

#### from\_etree

```python
@classmethod
def from_etree(cls,
               tree: etree.Element,
               parent: Union["PageXML", Self],
               skip_unknown: bool = False) -> Self
```

Create a new PageElement object from an etree element.

**Arguments**:

- `tree` - lxml etree object.
- `parent` - The parent element of this page element.
- `skip_unknown` - Skip unknown elements. Else raise ValueError. Defaults to False.

**Raises**:

- `ValueError` - If the element is not a valid PageXML element and skip_unknown is False.

**Returns**:

  PageElement object that represents the passed etree element.

<a id="pypxml.pagelement.PageElement.to_etree"></a>

#### to\_etree

```python
def to_etree() -> etree.Element
```

Convert the PageElement object to an etree element.

**Returns**:

  A lxml etree object that represents this PageElement object.

<a id="pypxml.pagelement.PageElement.find_by_id"></a>

#### find\_by\_id

```python
def find_by_id(id: str, recursive: bool = False) -> Optional[Self]
```

Find an element by its id.

**Arguments**:

- `id` - ID of the element to find.
- `recursive` - If set, search in all child elements. Defaults to False.

**Returns**:

  The PageElement object with the given ID. Returns None, if no match was found.

<a id="pypxml.pagelement.PageElement.find_by_type"></a>

#### find\_by\_type

```python
def find_by_type(pagetype: Union[PageType, list[PageType]],
                 recursive: bool = False) -> list[Self]
```

Find all elements by their type.

**Arguments**:

- `pagetype` - Type of the elements to find.
- `recursive` - If set, search in all child elements. Defaults to False.

**Returns**:

  A list of PageElement objects with the given type. Returns an empty list, if no match was found.

<a id="pypxml.pagelement.PageElement.create_element"></a>

#### create\_element

```python
def create_element(pagetype: PageType,
                   index: Optional[int] = None,
                   **attributes: str) -> Self
```

Create a new PageElement object and add it to the list of elements.

**Arguments**:

- `pagetype` - PageType of the new PageElement object.
- `index` - If set, insert the new element at this index. Else append to the list. Defaults to None.
- `attributes` - Named arguments which represent the attributes of the `PageElement` object.

**Returns**:

  The new PageElement object.

<a id="pypxml.pagelement.PageElement.get_element"></a>

#### get\_element

```python
def get_element(index: int) -> Optional[Self]
```

Get an PageElement object by its index.

**Arguments**:

- `index` - Index of the PageElement object.

**Returns**:

  The PageElement object of passed index (returns None if the index is out of range).

<a id="pypxml.pagelement.PageElement.set_element"></a>

#### set\_element

```python
def set_element(element: Self, index: Optional[int] = None) -> None
```

Add an existing PageElement object to the list of elements.

**Arguments**:

- `element` - The PageElement to add.
- `index` - If set, insert the element at this index. Else append to the list. Defaults to None.

<a id="pypxml.pagelement.PageElement.remove_element"></a>

#### remove\_element

```python
def remove_element(element: Union[Self, int]) -> Optional[Self]
```

Remove an element from the list of elements.

**Arguments**:

- `element` - The PageElement or the index of the PageElement to remove.

**Returns**:

  The removed element, if it was found. Else None.

<a id="pypxml.pagelement.PageElement.clear_elements"></a>

#### clear\_elements

```python
def clear_elements() -> None
```

Remove all elements from the list of elements. This will not remove the element itself.

<a id="pypxml.pagelement.PageElement.get_attribute"></a>

#### get\_attribute

```python
def get_attribute(key: str) -> Optional[str]
```

Get an attribute value by its key.

**Arguments**:

- `key` - Key of the attribute.

**Returns**:

  The value of the attribute. Returns None, if no match was found.

<a id="pypxml.pagelement.PageElement.set_attribute"></a>

#### set\_attribute

```python
def set_attribute(key: str, value: Optional[str]) -> None
```

Set an attribute value.

**Arguments**:

- `key` - Key of the attribute. Creates a new attribute if it does not exist.
- `value` - Value of the attribute. If None, remove the attribute.

<a id="pypxml.pagelement.PageElement.remove_attribute"></a>

#### remove\_attribute

```python
def remove_attribute(key: str) -> Optional[str]
```

Remove an attribute by its key.

**Arguments**:

- `key` - Key of the attribute.

**Returns**:

  The value of the removedattribute. Returns None, if no match was found.

<a id="pypxml.pagelement.PageElement.clear_attributes"></a>

#### clear\_attributes

```python
def clear_attributes() -> None
```

Remove all attributes from the PageElement object.

<a id="pypxml.pagelement.PageElement.is_region"></a>

#### is\_region

```python
def is_region() -> bool
```

Check if the page element is a region.

**Returns**:

  True, if the page element is a region. Else return False.

<a id="pypxml.pagetype"></a>

# pypxml.pagetype

<a id="pypxml.pagetype.PageType"></a>

## PageType Objects

```python
class PageType(Enum)
```

https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page

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

<a id="pypxml.pagetype.PageType.Graphemes"></a>

#### Graphemes

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

<a id="pypxml.pagetype.is_valid"></a>

#### is\_valid

```python
def is_valid(value: str) -> bool
```

Returns true if string is a valid PageXML type.

<a id="pypxml.pagetype.is_region"></a>

#### is\_region

```python
def is_region(value: str) -> bool
```

Returns true if string is a valid PageXML region type

<a id="pypxml.pagexml"></a>

# pypxml.pagexml

<a id="pypxml.pagexml.PageXML"></a>

## PageXML Objects

```python
class PageXML()
```

PageXML Root and Page element class.

<a id="pypxml.pagexml.PageXML.__init__"></a>

#### \_\_init\_\_

```python
def __init__(creator: Optional[str] = None,
             created: Optional[Union[datetime, str]] = None,
             changed: Optional[Union[datetime, str]] = None,
             xml: Optional[Path] = None,
             **attributes: str) -> None
```

PLEASE USE THE .new() METHOD TO CREATE A NEW PAGEXML OBJECT.
This constructor is only for internal use.

**Arguments**:

- `creator` - Metadata `Creator`. Defaults to None.
- `created` - Metadata `Created` in UTC, not local time. Defaults to None.
- `changed` - Metadata `LastChange` in UTC, not local time. Defaults to None.
- `file` - Path of the PageXML file, if the object was created from a file. Defaults to None.
- `attributes` - Named arguments which represent the attributes of the PageXML object.

<a id="pypxml.pagexml.PageXML.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns the string representation of the PageXML object.

<a id="pypxml.pagexml.PageXML.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Returns the string representation of the PageXML object.

<a id="pypxml.pagexml.PageXML.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of region elements in the PageXML object.

<a id="pypxml.pagexml.PageXML.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Self
```

Iterate over all elements of the page.

<a id="pypxml.pagexml.PageXML.__next__"></a>

#### \_\_next\_\_

```python
def __next__() -> PageElement
```

Yield next element of the page.

<a id="pypxml.pagexml.PageXML.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Union[int, str]) -> Optional[Union[PageElement, str]]
```

Get an PageElement object by its index or an attribute value by its key

**Arguments**:

- `key` - Index (integer) of an PageElement object or a key (string) of an attribute.

**Returns**:

  The PageElement of passed index (returns last object if the key is out of range) or the value of the
  selected attribute. Returns None, if no match was found.

<a id="pypxml.pagexml.PageXML.__setitem__"></a>

#### \_\_setitem\_\_

```python
def __setitem__(key: Union[int, str], value: Union[PageElement, str]) -> None
```

Set an PageElement object or an attribute value.

**Arguments**:

- `key` - Index (integer) for an PageElement object or a key (string) for an attribute.
- `value` - PageElement object (if key is of type integer) or a string (if key is of type string).

<a id="pypxml.pagexml.PageXML.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(key: Union[PageElement, str]) -> bool
```

Checks if an PageElement object or an attribute exists.

**Arguments**:

- `key` - PageElement object or attribute key.

**Returns**:

  True, if either the passed PageElement object or the attribute exists. Else return False.

<a id="pypxml.pagexml.PageXML.creator"></a>

#### creator

```python
@property
def creator() -> Optional[str]
```

Returns the metadata `Creator`.

<a id="pypxml.pagexml.PageXML.creator"></a>

#### creator

```python
@creator.setter
def creator(value: str) -> None
```

Set the metadata `Creator`.

<a id="pypxml.pagexml.PageXML.created"></a>

#### created

```python
@property
def created() -> Optional[str]
```

Returns the metadata `Created`.

<a id="pypxml.pagexml.PageXML.created"></a>

#### created

```python
@created.setter
def created(value: Union[datetime, str]) -> None
```

Set the metadata `Created`.

<a id="pypxml.pagexml.PageXML.changed"></a>

#### changed

```python
@property
def changed() -> Optional[str]
```

Returns the metadata `LastChange`.

<a id="pypxml.pagexml.PageXML.changed"></a>

#### changed

```python
@changed.setter
def changed(value: Union[datetime, str]) -> None
```

Set the metadata `LastChange`.

<a id="pypxml.pagexml.PageXML.attributes"></a>

#### attributes

```python
@property
def attributes() -> dict[str, str]
```

Get the attributes of the page element.

<a id="pypxml.pagexml.PageXML.attributes"></a>

#### attributes

```python
@attributes.setter
def attributes(attributes: dict[str, str]) -> None
```

Set the attributes of the page element.

<a id="pypxml.pagexml.PageXML.elements"></a>

#### elements

```python
@property
def elements() -> list[PageElement]
```

Returns a copy of the elements list.

<a id="pypxml.pagexml.PageXML.regions"></a>

#### regions

```python
@property
def regions() -> list[PageElement]
```

Returns a copy of the regions list.

<a id="pypxml.pagexml.PageXML.reading_order"></a>

#### reading\_order

```python
@property
def reading_order() -> list[str]
```

Returns the reading order of the page.

<a id="pypxml.pagexml.PageXML.reading_order"></a>

#### reading\_order

```python
@reading_order.setter
def reading_order(order: Optional[list[str]]) -> None
```

Set the reading order of the page.

<a id="pypxml.pagexml.PageXML.xml"></a>

#### xml

```python
@property
def xml() -> Optional[Path]
```

Returns the file path of the PageXML file.

<a id="pypxml.pagexml.PageXML.xml"></a>

#### xml

```python
@xml.setter
def xml(file: Union[Path, str]) -> None
```

Set the file path of the PageXML file.

<a id="pypxml.pagexml.PageXML.new"></a>

#### new

```python
@classmethod
def new(cls, creator: str = "pypxml", **attributes: str) -> Self
```

Create a new empty PageXML object.

**Arguments**:

- `creator` - Set a custom PageXML `Metadata` creator. Defaults to "pypxml".
- `attributes` - Named arguments which represent the attributes of the `Page` object.

**Returns**:

  A empty PageXML object.

<a id="pypxml.pagexml.PageXML.from_etree"></a>

#### from\_etree

```python
@classmethod
def from_etree(cls, tree: etree.Element, skip_unknown: bool = False) -> Self
```

Create a new PageXML object from an lxml etree object.

**Arguments**:

- `tree` - lxml etree object.
- `skip_unknown` - Skip unknown elements. Else raise ValueError. Defaults to False.

**Raises**:

- `ValueError` - If the etree object does not contain a Page element.

**Returns**:

  PageXML object that represents the passed etree element.

<a id="pypxml.pagexml.PageXML.from_file"></a>

#### from\_file

```python
@classmethod
def from_file(cls,
              file: Union[Path, str],
              encoding: str = "utf-8",
              skip_unknown: bool = False) -> Self
```

Create a new PageXML object from a PageXML file.

**Arguments**:

- `file` - Path of the PageXML file.
- `encoding` - Set custom encoding. Defaults to "utf-8".
- `skip_unknown` - Skip unknown elements. Else raise ValueError. Defaults to False.

**Returns**:

  PageXML object that represents the passed PageXML file.

<a id="pypxml.pagexml.PageXML.to_etree"></a>

#### to\_etree

```python
def to_etree(schema_version: str = "2019",
             schema_file: Optional[Union[Path, str]] = None) -> etree.Element
```

Returns the PageXML object as an lxml etree object.

**Arguments**:

- `schema_version` - Which schema version to use. Available by default: "2017", "2019". Defaults to "2019".
- `schema_file` - Set a custom schema json file (see documentation for further information). Defaults to None.

**Returns**:

  A lxml etree object that represents the PageXML object.

**Schema File Example**

```json
{
    "2017": {
        "xmlns": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15",
        "xmlns_xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi_schema_location": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd"
    },
    "2019": {
        "xmlns": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15",
        "xmlns_xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi_schema_location": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15/pagecontent.xsd"
    }
}
```

<a id="pypxml.pagexml.PageXML.to_file"></a>

#### to\_file

```python
def to_file(file: Union[Path, str],
            encoding="utf-8",
            schema_version: str = "2019",
            schema_file: Optional[Union[Path, str]] = None) -> None
```

Write the PageXML object to a file.

**Arguments**:

- `file` - File path to write the PageXML object to.
- `encoding` - Set custom encoding. Defaults to "utf-8".
- `schema_version` - Which schema version to use. Available by default: "2017", "2019". Defaults to "2019".
- `schema_file` - Set a custom schema json file (see documentation for further information). Defaults to None.

**Schema File Example**

See above

<a id="pypxml.pagexml.PageXML.find_by_id"></a>

#### find\_by\_id

```python
def find_by_id(id: str, recursive: bool = False) -> Optional[PageElement]
```

Find an element by its id.

**Arguments**:

- `id` - ID of the element to find.
- `recursive` - If set, search in all child elements. Defaults to False.

**Returns**:

  The PageElement object with the given ID. Returns None, if no match was found.

<a id="pypxml.pagexml.PageXML.find_by_type"></a>

#### find\_by\_type

```python
def find_by_type(pagetype: Union[PageType, list[PageType]],
                 recursive: bool = False) -> list[PageElement]
```

Find all elements by their type.

**Arguments**:

- `pagetype` - Type of the elements to find.
- `recursive` - If set, search in all child elements. Defaults to False.

**Returns**:

  A list of PageElement objects with the given type. Returns an empty list, if no match was found.

<a id="pypxml.pagexml.PageXML.create_element"></a>

#### create\_element

```python
def create_element(pagetype: PageType,
                   index: Optional[int] = None,
                   **attributes: str) -> PageElement
```

Create a new PageElement object and add it to the list of elements.

**Arguments**:

- `pagetype` - PageType of the new PageElement object.
- `index` - If set, insert the new element at this index. Else append to the list. Defaults to None.
- `attributes` - Named arguments which represent the attributes of the `PageElement` object.

**Returns**:

  The new PageElement object.

<a id="pypxml.pagexml.PageXML.get_element"></a>

#### get\_element

```python
def get_element(index: int) -> Optional[PageElement]
```

Get an PageElement object by its index.

**Arguments**:

- `index` - Index of the PageElement object.

**Returns**:

  The PageElement object of passed index (returns None if the index is out of range).

<a id="pypxml.pagexml.PageXML.set_element"></a>

#### set\_element

```python
def set_element(element: PageElement,
                index: Optional[int] = None,
                ro: bool = True) -> None
```

Add an existing PageElement object to the list of elements.

**Arguments**:

- `element` - The PageElement to add.
- `index` - If set, insert the element at this index. Else append to the list. Defaults to None.
- `ro` - If set to true, add the element to the reading order at the specified index.
  Only if the element is a region.

<a id="pypxml.pagexml.PageXML.remove_element"></a>

#### remove\_element

```python
def remove_element(element: Union[PageElement, int]) -> Optional[PageElement]
```

Remove an element from the list of elements.

**Arguments**:

- `element` - The PageElement or the index of the PageElement to remove.

**Returns**:

  The removed element, if it was found. Else None.

<a id="pypxml.pagexml.PageXML.clear_elements"></a>

#### clear\_elements

```python
def clear_elements() -> None
```

Remove all elements from the list of elements. This will not remove the element itself.

<a id="pypxml.pagexml.PageXML.get_attribute"></a>

#### get\_attribute

```python
def get_attribute(key: str) -> Optional[str]
```

Get an attribute value by its key.

**Arguments**:

- `key` - Key of the attribute.

**Returns**:

  The value of the attribute. Returns None, if no match was found.

<a id="pypxml.pagexml.PageXML.set_attribute"></a>

#### set\_attribute

```python
def set_attribute(key: str, value: Optional[str]) -> None
```

Set an attribute value.

**Arguments**:

- `key` - Key of the attribute. Creates a new attribute if it does not exist.
- `value` - Value of the attribute. If None, remove the attribute.

<a id="pypxml.pagexml.PageXML.remove_attribute"></a>

#### remove\_attribute

```python
def remove_attribute(key: str) -> Optional[str]
```

Remove an attribute by its key.

**Arguments**:

- `key` - Key of the attribute.

**Returns**:

  The value of the removedattribute. Returns None, if no match was found.

<a id="pypxml.pagexml.PageXML.clear_attributes"></a>

#### clear\_attributes

```python
def clear_attributes() -> None
```

Remove all attributes from the PageXML object.
