# pypxml
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/pypxml.svg)](https://badge.fury.io/py/pypxml)

A modern, powerful,and extremly fast Python library for reading, writing, and modifying [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) files.

PAGE-XML is the standard format for storing layout and text information from OCR and document analysis systems.

## Python API
_pypxml_ provides an intuitive Python API to interact with PAGE-XML files.

### Install
```bash
uv add pypxml
```
> [!NOTE]
> Alternatively install with pip: `pip install pypxml`

### Example
```python
from pypxml import PageXML, PageType, PageUtil

# Open an existing PAGE-XML file
page = PageXML.open('document.xml')

# Access page metadata and attributes
print(f'Creator: {page.creator}')
print(f'Image: {page["imageFilename"]}')

# Find all text regions of type marginalia and extract their text
for region in page.find_all(PageType.TextRegion, type='marginalia'):
    print(f'\nRegion {region["id"]}:')
    
    # Get all text lines in this region
    for line in region.find_all(PageType.TextLine, depth=-1):
        text = PageUtil.find_text(line)
        if text:
            print(f'\t{text}')

# Sort regions by their position
PageUtil.sort_regions(page, direction='top-bottom')

# Save with schema validation
page.save('output.xml', schema='2019')
```

## Command Line Interface
For common analytics and regularization operations, the command line interface (cli) can be installed

### Setup
```bash
uv tool install pypxml[cli]
```
> [!NOTE]
> Alternatively install with pip: `pip install pypxml[cli]`

### Usage
```text
$ pypxml --help
Usage: pypxml [OPTIONS] COMMAND [ARGS]...

  A modern, powerful,and extremly fast Python library for reading, writing,
  and modifying PAGE-XML files

Options:
  --help                          Show this message and exit.
  --version                       Show the version and exit.
  --logging [ERROR|WARNING|INFO]  Set logging level.  [default: ERROR]

Commands:
  get-codec           Extract character set from PAGE-XML files.
  get-regions         Extract region types from PAGE-XML files.
  get-text            Extract text from a PAGE-XML file.
  regularize-codec    Regularize character encodings in PAGE-XML files.
  regularize-regions  Regularize region types in PAGE-XML files.

  Developed at Centre for Philology and Digitality (ZPD), University of
  Würzburg
```

## Benchmarks
Benchmarks were aggregated over 100 randomly selected PAGE-XML files representing common book pages.
Below, the average time is listed for each operation and OCR granularity.

| Operation | Lines | Words | Glyphs | Description                                                                                 |
| --------- | ----: | ----: | -----: | ------------------------------------------------------------------------------------------- |
| `open`    | 0.8ms | 3.6ms | 20.6ms | Average time to open (and parse) a PAGE-XML file with OCR on TextLine, Word, or Glyph level |
| `search`  | 0.1ms | 0.5ms |  2.9ms | Average time to search for _all_ TextLine, Word, or Glyph elements                          |
| `write`   | 1.6ms | 3.6ms | 13.6ms | Average time to write a PAGE-XML file with OCR on TextLine, Word, or Glyph level            |

> [!NOTE]
> The experiments where conducted on an Intel 12th Gen i7-12700 

## Related Projects

- [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) - The PAGE-XML format specification
- [OCR-D](https://ocr-d.de/) - OCR framework using PAGE-XML

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).