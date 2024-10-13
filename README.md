from src.pypxml import XMLSchema

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

### PageXML class
```python
from pypxml import PageXML

# open file
pxml = PageXML.from_xml('path_to.xml')
# or create new PageXML
pxml = PageXML.new()

# edit metadata
pxml.creator = 'yourname'
...

# create a page
page = pxml.create_page(imageFilename='0001.png',
                        imageWidth=1000,
                        imageHeight='2500')
# or add existing page
pxml.add_page(page)  # see below

# iterate over pages
for page in pxml:
    ...

# delete or modify pages
pxml[0] = ...
pxml.remove_page(pxml[1])

# save object to file
pxml.to_xml('output.xml')
...
```

### Page class
```python
from pypxml import Page, XMLType

# create a page
page = Page.new(imageFilename='0001.png',
                imageWidth=1000,
                imageHeight=2500)

# modify attributes
page['imageFilename'] = '0002.png'
# or get element by index
element = page[3]

# add elements (automatically added to reading order if it is a region)
text_region = page.create_element(XMLType.TextRegion, id='tr1')
# or add existing element
page.add_element(element)

# iterate over regions
for region in page:
    ...
...
```

### Element class
```python
from pypxml import Element, XMLType

# create an element
coords = Element.new(XMLType.Coords, 
                     points='1,2 3,4 5,6 7,8')
# modify attributes
coords['points'] = 'some other coords'
# or get element by index
baseline = text_region[2]

# check if element is a region
if text_region.is_region():
    ...

# get coords and baseline, if they exist
coords = text_line.get_coords()
baseline = text_line.get_baseline()
...
```

## ZPD
Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).