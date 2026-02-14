# pypxml.PageXML

```python
class PageXML()
```

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

## Constructor

### \_\_init\_\_

Create a new empty `PageXML` object.

```python
def __init__(
    self,
    creator: str = 'pypxml',
    created: datetime | str | None = None,
    last_change: datetime | str | None = None,
    **attributes: str
) -> None:
```

---

### open

```python
@classmethod
def open(
    cls,
    file: Path | str,
    encoding: str = 'utf-8',
    raise_on_error: bool = True
) -> PageXML:
```

Create a new `PageXML` object from a PAGE-XML file.

#### Arguments

- `file`: The path of the PAGE-XML file.
- `encoding`: Custom encoding. Defaults to 'utf-8'.
- `raise_on_error`: If set to False, parsing errors are ignored. Defaults to True.

#### Returns

A `PageXML` object that represents the passed PAGE-XML file.

#### Arguments

- `creator`: The creator of the PAGE-XML object. Defaults to 'pypxml'.
- `created`: The timestamp (ISO 8601) of the creation of the PAGE-XML. The timestamp must be in UTC (Coordinated Universal Time) and not local time. Defaults to None.
- `last_change`: The timestamp (ISO 8601) of the last change. The timestamp must be in UTC (Coordinated Universal Time) and not local time. Defaults to None.
- `attributes`: Named arguments that represent the optional attributes of the 'Page' element.

#### Returns

None

---

### _from_etree

```python
@classmethod
def _from_etree(
    cls,
    tree: etree.Element,
    raise_on_error: bool = True
) -> PageXML:
```

Create a new `PageXML` object from a lxml etree element.

#### Arguments

- `tree`: The lxml etree element.
- `raise_on_error`: If set to False, parsing errors are ignored. Defaults to True.

#### Returns

A `PageXML` object that represents the passed etree element.

#### Raises

- `ValueError`: If the element is not a valid PageXML and raise_on_error is True.


## Properties

### creator

```python
@property
def creator(self) -> str:
```

The creator of the PAGE-XML.

**Setter:**
```python
@creator.setter
def creator(self, value: str | None) -> None:
```

The creator of the PAGE-XML file.

---

### created

```python
@property
def created(self) -> str:
```

The timestamp (ISO 8601) of the creation of the PAGE-XML file.

**Setter:**
```python
@created.setter
def created(self, value: datetime | str | None) -> None:
```

The timestamp (ISO 8601) of the creation of the PAGE-XML file.

---

### last_change

```python
@property
def last_change(self) -> str:
```

The timestamp (ISO 8601) of the last change.

**Setter:**
```python
@last_change.setter
def last_change(self, value: datetime | str | None) -> None:
```

The timestamp (ISO 8601) of the last change.

---

### attributes

```python
@property
def attributes(self) -> dict[str, str]:
```

A dictionary (copy) containing key/value pairs that represent XML attributes.

**Setter:**
```python
@attributes.setter
def attributes(self, attributes: dict[str, str] | None) -> None:
```

Sets the dictionary containing key/value pairs that represent XML attributes.

---

### reading_order

```python
@property
def reading_order(self) -> list[str]:
```

Returns a copy of the reading order of the page.

---

### elements

```python
@property
def elements(self) -> list[PageElement]:
```

A copy of the list of child elements.

---

### regions

```python
@property
def regions(self) -> list[PageElement]:
```

Returns a copy of the list of child regions.

## Methods

### _to_etree

```python
def _to_etree(
    self,
    schema: PageSchema | str | None = None
) -> etree.Element:
```

Convert the `PageXML` object to a lxml etree element.

#### Arguments

- `schema`: Select a schema version (currently supported: `2017`, `2019`) or pass a custom schema. Defaults to None.

#### Returns

A lxml etree object that represents the `PageXML` object.

---

### save

```python
def save(
    self,
    file: Path | str,
    encoding: str = 'utf-8',
    schema: PageSchema | str = '2019'
) -> None:
```

Write the `PageXML` object to a file.

#### Arguments

- `file`: The file path to write the object to.
- `encoding`: Set file encoding. Defaults to 'utf-8'.
- `schema`: Select a schema version (currently supported: `2017`, `2019`) or pass a custom schema.

#### Returns

None

---

### find_all

```python
def find_all(
    self,
    id: str | list[str] | None = None,
    pagetype: PageType | list[PageType] | None = None,
    depth: int = 0,
    **attributes: str
) -> list[PageElement]:
```

Find `PageElements` by their type, id and attributes.

#### Arguments

- `id`: One or more element IDs to look for. If not set, no ID filter is applied.
- `pagetype`: One or more element types to look for. If not set, no type filter is applied.
- `depth`: The depth level of the search.
  - `0` (default) searches only the current level.
  - `-1` searches all levels recursively (no depth limit, may be slow).
  - `>0` limits the search to the specified number of levels deep.
- `attributes`: Named arguments representing the attributes that the found elements must have. If not set, no attribute filter is applied.

#### Returns

A (possibly empty) list of found `PageElements`.

---

### find

```python
def find(
    self,
    id: str | list[str] | None = None,
    pagetype: PageType | list[PageType] | None = None,
    depth: int = 0,
    **attributes: str
) -> PageElement | None:
```

Find a `PageElement` by their type, id and attributes.

#### Arguments

- `id`: One or more element IDs to look for. If not set, no ID filter is applied.
- `pagetype`: One or more element types to look for. If not set, no type filter is applied.
- `depth`: The depth level of the search.
  - `0` (default) searches only the current level.
  - `-1` searches all levels recursively (no depth limit, may be slow).
  - `>0` limits the search to the specified number of levels.
- `attributes`: Named arguments representing the attributes that the found elements must have. If not set, no attribute filter is applied.

#### Returns

The first found `PageElement` or None if no match was found.

---

### create

```python
def create(
    self,
    pagetype: PageType,
    i: int | None = None,
    reading_order: bool = True,
    **attributes: str
) -> PageElement:
```

Create a new child `PageElement` and add it to the list of elements.

#### Arguments

- `pagetype`: The `PageType` of the new child element.
- `i`: If set, insert the new element at this index. Otherwise, append it to the list. Defaults to None.
- `reading_order`: If set to True, add the element to the reading order at the specified index. Only applies if the element is a region. Defaults to True.
- `attributes`: Named arguments that represent the attributes of the child object.

#### Returns

The newly created `PageElement` child object.

---

### set

```python
def set(
    self,
    element: PageElement,
    i: int | None = None,
    reading_order: bool = True
) -> None:
```

Add an existing `PageElement` object to the list of child elements.

#### Arguments

- `element`: The element to add as a child element.
- `i`: If set, insert the element at this index. Otherwise, append it to the list. Defaults to None.
- `reading_order`: If set to True, add the element to the reading order at the specified index. Only applies if the element is a region. Defaults to True.

#### Returns

None

---

### delete

```python
def delete(
    self,
    element: PageElement
) -> PageElement | None:
```

Remove an element from the list of child elements. This includes occurrences in the reading order.

#### Arguments

- `element`: The element to remove.

#### Returns

The `PageElement` if it was deleted. Otherwise, None.

---

### clear

```python
def clear(
    self,
    regions_only: bool = False
) -> None:
```

Remove all elements from the list of child elements.

#### Arguments

- `regions_only`: Only delete region elements. Defaults to False.

#### Returns

None

---

### reading_order_apply

```python
def reading_order_apply(self) -> None:
```

Sort the child elements based on the current reading order.

Non-region elements are placed first, followed by regions according to the reading order.
Regions not included in the reading order are placed last.

#### Arguments

None

#### Returns

None

---

### reading_order_create

```python
def reading_order_create(
    self,
    overwrite: bool = False
) -> None:
```

Create a new reading order based on the current element sequence.

#### Arguments

- `overwrite`: If True, overwrites any existing reading order. If False, only creates a new reading order if the current one is empty. Defaults to False.

#### Returns

None

---

### reading_order_set

```python
def reading_order_set(
    self,
    reading_order: list[str] | None,
    apply: bool = True
) -> None:
```

Update the reading order of regions in the PAGE-XML document.

#### Arguments

- `reading_order`: A list of region IDs defining the desired reading order. If an empty list or None is passed, the reading order is cleared. (Note: Validity of IDs is not checked.)
- `apply`: If True, reorders the elements in the `PageXML` based on the passed reading order. Defaults to True.

#### Returns

None

---

### reading_order_sort

```python
def reading_order_sort(
    self,
    reference: Literal['minimum', 'maximum', 'centroid'] = 'minimum',
    direction: Literal['top-bottom', 'bottom-top', 'left-right', 'right-left'] = 'top-bottom',
    apply: bool = True
) -> None:
```

Sort the regions in the PAGE-XML document by their location on the page.

#### Arguments

- `reference`: The method for determining the reference point used for sorting:
  - `minimum` sorts by the minimum coordinate value in the given direction,
  - `maximum` sorts by the maximum coordinate value in the given direction,
  - `centroid` sorts by the centroid position of each region.
  
  Defaults to 'minimum'.
- `direction`: The primary direction in which regions are sorted. Defaults to 'top-bottom'.
- `apply`: If True, also reorders the physical sequence of region elements in the PageXML. If False, only updates the reading order element without changing the actual XML element order. Defaults to True.

#### Returns

None

---

### reading_order_clear

```python
def reading_order_clear(self) -> None:
```

Remove all elements from the reading order without deleting the actual elements.

#### Arguments

None

#### Returns

None


## Magic Methods

### \_\_str\_\_

```python
def __str__(self) -> str:
```

Returns a string representation of the object.

---

### \_\_repr\_\_

```python
def __repr__(self) -> str:
```

Returns a detailed string representation including PcGts metadata and Page attributes.

---

### \_\_len\_\_

```python
def __len__(self) -> int:
```

Returns the number of child elements.

---

### \_\_iter\_\_

```python
def __iter__(self) -> PageElement:
```

Initializes iteration over child elements.

---

### \_\_next\_\_

```python
def __next__(self) -> PageElement:
```

Returns the next child element during iteration.

---

### \_\_getitem\_\_

```python
def __getitem__(self, key: int | str) -> PageElement | str | None:
```

Access child elements by index or attributes by key.

#### Arguments

- `key`: If int, returns the element at that index. If str, returns the attribute value for that key.

#### Returns

`PageElement` (if key is int) or attribute value (if key is str), or None if not found.

---

### \_\_setitem\_\_

```python
def __setitem__(self, key: str, value: str | None) -> None:
```

Set or remove an attribute.

#### Arguments

- `key`: The attribute name.
- `value`: The attribute value. If None, removes the attribute.

---

### \_\_contains\_\_

```python
def __contains__(self, key: PageElement | str) -> bool:
```

Check if an element or attribute exists.

#### Arguments

- `key`: If `PageElement`, checks if it's in the elements list. If str, checks if the attribute exists.

#### Returns

True if the element or attribute exists, False otherwise.
