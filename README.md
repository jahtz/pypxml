# pypxml
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/pypxml.svg)](https://badge.fury.io/py/pypxml)

A modern, powerful Python library for reading, writing, and modifying [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) files.

PAGE-XML is the standard format for storing layout and text information from OCR and document analysis systems. _pypxml_ makes it easy to work with these files programmatically.

## Installation
### From PyPI (Recommended)
```bash
pip install pypxml  # pypxml[cli] for cli support
```

### From Source
```bash
git clone https://github.com/jahtz/pypxml
cd pypxml
pip install .  # .[cli] for cli support
```

## CLI
```bash
pypxml --help
```
- `get-codec` Extract the character set from PAGE-XML files.
- `get-regions` List all regions in PageXML files.
- `get-text` Extract text from PageXML files.
- `regularize-codec` Regularize character encodings in PAGE-XML files.
- `regularize-regions` Regularize region types in PAGE-XML files.


## API Demo
### Reading a PAGE-XML File

```python
from pypxml import PageXML, PageType, PageUtil

# Open and parse a PAGE-XML file
pagexml = PageXML.open("document.xml")

# Access metadata
print(f"Creator: {pagexml.creator}")
print(f"Created: {pagexml.created}")

# Get all text regions
regions = pagexml.find_all(pagetype=PageType.TextRegion, type=)
print(f"Found {len(regions)} text regions")

# Extract text from the document
for region in pagexml.regions:
    lines = region.find_all(pagetype=PageType.TextLine)
    for line in lines:
        text = PageUtil.get_text(line)
        print(text)
```

### Creating a New PAGE-XML Document

```python
from pypxml import PageXML, PageType

# Create a new PAGE-XML document
pagexml = PageXML(
    creator="MyApplication",
    imageFilename="scan_001.jpg",
    imageWidth="2000",
    imageHeight="3000"
)

# Add a text region
region = pagexml.create(
    PageType.TextRegion,
    id="r1",
    custom="paragraph"
)

# Add coordinates
region.create(
    PageType.Coords,
    points="100,100 500,100 500,300 100,300"
)

# Add a text line with content
line = region.create(PageType.TextLine, id="l1")
line.create(PageType.Coords, points="100,100 500,100 500,130 100,130")

textequiv = line.create(PageType.TextEquiv, index="0")
unicode_elem = textequiv.create(PageType.Unicode)
unicode_elem.text = "Hello, PAGE-XML!"

# Save the document
pagexml.save("output.xml", schema="2019")
```

### Searching and Filtering

```python
from pypxml import PageXML, PageType

pagexml = PageXML.open("document.xml")

# Find elements by ID
region = pagexml.find(id="r1")

# Find all elements of a specific type
text_regions = pagexml.find_all(pagetype=PageType.TextRegion)

# Search with depth control
# depth=0: only direct children
# depth=-1: unlimited depth (recursive)
# depth=2: search 2 levels deep
all_lines = pagexml.find_all(
    pagetype=PageType.TextLine,
    depth=-1  # Search recursively
)

# Find by custom attributes
paragraphs = pagexml.find_all(
    pagetype=PageType.TextRegion,
    depth=-1,
    custom="paragraph"
)

# Find multiple types at once
elements = pagexml.find_all(
    pagetype=[PageType.TextRegion, PageType.ImageRegion]
)
```

### Working with Reading Order

```python
from pypxml import PageXML

pagexml = PageXML.open("document.xml")

# Create reading order from current element sequence
pagexml.reading_order_create()

# Sort reading order by position (top to bottom)
pagexml.reading_order_sort(
    reference='centroid',    # or 'minimum', 'maximum'
    direction='top-bottom'   # or 'bottom-top', 'left-right', 'right-left'
)

# Manually set reading order
pagexml.reading_order_set(["r3", "r1", "r2"])

# Apply reading order to element sequence
pagexml.reading_order_apply()

# Clear reading order
pagexml.reading_order_clear()

# Get current reading order
ro = pagexml.reading_order
print(f"Reading order: {ro}")
```

## Related Projects

- [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) - The PAGE-XML format specification
- [OCR-D](https://ocr-d.de/) - OCR framework using PAGE-XML

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).