# PyPXML
A python library for parsing, converting and modifying PageXML files.

## Setup
```shell
pip install pypxml
```

### Install from source
1. Clone repository: `git clone https://github.com/jahtz/pypxml`
2. Install package: `cd pypxml && pip install .`
3. Test with `pypxml --version`

## CLI
```
pypxml [OPTIONS] COMMAND [ARGS]...
```

## API
PyXML provides a feature rich Python API for working with PageXML files.

### Example: Edit existing PageXML
```python
from pypxml import PageXML, PageType

pxml = PageXML.from_xml('path_to_pagexml.xml')
text_region = pxml.create_element(PageType.TextRegion, type='paragraph', id='tr_001')
text_region.create_element(PageType.Coords, points='1,2 3,4 5,6 ...')

for region in pxml.regions:
    print(region.type)

pxml.to_xml('path_to_output.xml')
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).
