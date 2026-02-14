# pypxml
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/pypxml.svg)](https://badge.fury.io/py/pypxml)

A modern, powerful Python library for reading, writing, and modifying [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) files.

PAGE-XML is the standard format for storing layout and text information from OCR and document analysis systems. _pypxml_ makes it easy to work with these files programmatically.

## Python API
```shell
pip install pypxml
```

### Example
```python
from pypxml import PageXML, PageType, PageUtil

# Open an existing PAGE-XML file
page = PageXML.open('document.xml')

# Access page metadata
print(f'Creator: {page.creator}')
print(f'Image: {page["imageFilename"]}')

# Find all text regions of type marginalia and extract their text
for region in page.find_all(pagetype=PageType.TextRegion, type='marginalia'):
    print(f'\nRegion {region["id"]}:')
    
    # Get all text lines in this region
    for line in region.find_all(pagetype=PageType.TextLine, depth=-1):
        text = PageUtil.get_text(line)
        if text:
            print(f'\t{text}')

# Sort regions by position
page.reading_order_sort(direction='top-bottom')

# Save with schema validation
page.save('output.xml', schema='2019')
```

### Documentation
- [API Documentation](/docs/api/README.md)
- [PageXML Class Documentation](/docs/api/PageXML.md)
- [PageElement Class Documentation](/docs/api/PageElement.md)


## Command Line Interface
```shell
pip install pypxml[cli]
```

### Usage
```shell
$ pypxml --help
Usage: pypxml [OPTIONS] COMMAND [ARGS]...

  A python library for reading, writing, and modifying PageXML files.

Options:
  --help                          Show this message and exit.
  --version                       Show the version and exit.
  --logging [ERROR|WARNING|INFO]  Set logging level.  [default: ERROR]

Commands:
  get-codec           Extract character set from PAGE-XML files.
  get-regions         Extract region types from PAGE-XML files.
  get-text            Extract text from a PAGE-XML file.
  prettify            Prettify formatting of PAGE-XML files.
  regularise-codec    Regularise character encodings in PAGE-XML files.
  regularise-regions  Regularise region types in PAGE-XML files.
```

### Documentation
- [CLI Documentation](/docs/cli/README.md)

## Related Projects

- [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) - The PAGE-XML format specification
- [OCR-D](https://ocr-d.de/) - OCR framework using PAGE-XML

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).