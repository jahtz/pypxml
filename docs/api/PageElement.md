# pypxml.PageElement

```python
class PageElement()
```

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

## Constructor

### \_\_init\_\_

Create a new empty `PageElement` object.

```python
def __init__(
    self,
    pagetype: PageType,
    parent: PageXML | PageElement,
    **attributes: str
) -> None:
```

#### Arguments

- `pagetype`: The type of the element.
- `parent`: The parent of the element.
- `attributes`: Named arguments that represent the attributes of the element.

#### Returns

An empty `PageElement` object.

---

### _from_etree

```python
@classmethod
def _from_etree(
    cls,
    tree: etree.Element,
    parent: PageXML | PageElement,
    raise_on_error: bool = True
) -> PageElement:
```

Create a new `PageElement` object from a lxml etree element.

#### Arguments

- `tree`: The lxml etree element.
- `parent`: The parent of this element.
- `raise_on_error`: If set to False, parsing errors are ignored. Defaults to True.

#### Returns

A `PageElement` object that represents the passed etree element.

#### Raises

- `ValueError`: If the element is not a valid PAGE-XML and raise_on_error is True.

## Properties

### pagetype

```python
@property
def pagetype(self) -> PageType:
```

The type of the `PageElement` object.

**Setter:**
```python
@pagetype.setter
def pagetype(self, pagetype: PageType | str) -> None:
```

The type of the `PageElement` object.

---

### is_region

```python
@property
def is_region(self) -> bool:
```

Check if the `PageElement` object is a region.

---

### parent

```python
@property
def parent(self) -> PageXML | PageElement:
```

The parent of the `PageElement` object. This may be a `PageXML` or `PageElement` object.

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

### elements

```python
@property
def elements(self) -> list[PageElement]:
```

A copy of the list of child elements.

---

### text

```python
@property
def text(self) -> str | None:
```

The stored text.

**Setter:**
```python
@text.setter
def text(self, value: str | None) -> None:
```

Store a text. If set to None, the text is deleted.

## Methods

### _to_etree

```python
def _to_etree(self) -> etree.Element:
```

Convert the `PageElement` object to a lxml etree element.

#### Arguments

None

#### Returns

An lxml etree object that represents this object with all its childs.

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
    **attributes: str
) -> PageElement:
```

Create a new child `PageElement` and add it to the list of elements.

#### Arguments

- `pagetype`: The PageType of the new child element.
- `i`: If set, inserts the new element at this index. Otherwise, appends it to the list. Defaults to None.
- `attributes`: Named arguments that represent the attributes of the child object.

#### Returns

The newly created `PageElement` child object.

---

### set

```python
def set(
    self,
    element: PageElement,
    i: int | None = None
) -> None:
```

Adds an existing `PageElement` object to the list of child elements.

#### Arguments

- `element`: The element to add as a child element.
- `i`: If set, inserts the element at this index. Otherwise, appends it to the list. Defaults to None.

#### Returns

None

---

### delete

```python
def delete(
    self,
    element: PageElement | None = None
) -> PageElement | None:
```

Remove an element from the list of child elements or the element itself.

#### Arguments

- `element`: The element to remove. If set to None, the current element itself is removed.

#### Returns

The `PageElement` if it was deleted. Otherwise, None.

---

### clear

```python
def clear(self) -> None:
```

Remove all elements from the list of child elements.

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

Returns a detailed string representation including pagetype, attributes, and text content if present.

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
def __getitem__(self, key: str) -> str | None:
```

Access attributes by key.

#### Arguments

- `key`: The attribute name.

#### Returns

The attribute value, or None if not found.

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
