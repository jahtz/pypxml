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
Coming in version 2.x

## API
PyXML provides a feature rich Python API for working with PageXML files.

### Basics
```python
from pypxml import PageXML, Page, Element, XMLType

pxml = PageXML.from_xml('path_to_pagexml.xml')
page1 = pxml.create_page(imageFilename='0001.png', 
                         imageWidth=1000, 
                         imageHeight=2500)
page1.create_element(XMLType.TextRegion, id='ir01')
pxml.to_xml('path_to_output.xml')
```
Full API documentation coming soon


## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).