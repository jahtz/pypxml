# pypxml API Overview

For detailed documentation on the main classes, see:
- [PageXML](/docs/api/PageXML.md) - Root container for PAGE-XML documents
- [PageElement](/docs/apiPageElement.md) - Individual elements within the hierarchy

## PageType
Enumeration of PAGE-XML element and region types.

This enum mirrors the element and region names defined in the PAGE-XML schema as specified by the [OCR-D ground truth guidelines](https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page). It provides a typed and Pythonic representation of PAGE-XML node names and structural elements.

The enum values correspond exactly to the XML tag names.

### Region Types

- `TextRegion` - Pure text content
- `ImageRegion` - Images and photos
- `TableRegion` - Tabular data
- `GraphicRegion` - Simple graphics and logos
- `LineDrawingRegion` - Single color illustrations
- `SeparatorRegion` - Column and paragraph separators
- `ChartRegion` - Charts and graphs
- `MathsRegion` - Mathematical formulas and equations
- `ChemRegion` - Chemical formulas
- `MusicRegion` - Musical notations
- `MapRegion` - Maps
- `AdvertRegion` - Advertisements
- `NoiseRegion` - Noise and artifacts
- `UnknownRegion` - Unknown region type
- `CustomRegion` - Custom region types

### Structural Elements

- `ReadingOrder` - Reading order container
- `OrderedGroup` / `UnorderedGroup` - Element grouping
- `OrderedGroupIndexed` / `UnorderedGroupIndexed` - Indexed grouping
- `RegionRef` / `RegionRefIndexed` - Region references
- `Border` - Page border
- `PrintSpace` - Printable area of the page
- `Coords` - Polygon coordinates
- `Baseline` - Text baseline coordinates
- `TextLine` - Text line element
- `Word` - Word element
- `Glyph` - Character glyph
- `Grapheme` / `GraphemeGroup` - Grapheme elements
- `TextEquiv` - Text equivalent container
- `Unicode` - Unicode text content
- `PlainText` - Plain ASCII text
- `Grid` / `GridPoints` - Table grid structure
- `AlternativeImage` - Alternative image representation
- `Layer` / `Layers` - Layer structure
- `Roles` - Region roles
- `Label` / `Labels` - Semantic labels
- `Relations` - Inter-element relations
- `TextStyle` - Text styling information
- `UserDefined` / `UserAttribute` - Custom data
- `Metadata` - Metadata container
- `NonPrintingChar` - Non-visual characters


## PageSchema
Immutable representation of a PAGE-XML schema definition.

This class encapsulates the XML namespace declarations and schema location required for a PAGE-XML document root. It maintains a class-level registry of predefined schema versions for convenient lookup, while allowing the creation of custom schema definitions.

### Properties

- `xmlns`: XML namespace URI
- `xmlns_xsi`: XSI namespace URI
- `xsi_schema_location`: Schema location string

### Predefined Schemas

Two schema versions are registered by default:

- `2017` - PAGE-XML 2017-07-15 schema
- `2019` - PAGE-XML 2019-07-15 schema (recommended)

### Create Custom Schema

```python
from pypxml import PageXML, PageSchema

custom_schema = PageSchema.custom(
    xmlns='http://example.com/custom/pagexml',
    xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
    xsi_schema_location='http://example.com/custom/pagexml schema.xsd'
)

# Use custom schema directly without registration
page.save('output.xml', schema=custom_schema)

# Register schema for global usage
PageSchema.register('custom', custom_schema)
page.save('output.xml', schema='custom')
```

## PageUtil
Utility helper class for common PAGE-XML operations.

This class provides convenience methods for extracting and resolving textual content from PageElement instances, abstracting away the structural complexity of PAGE-XML. The methods are stateless and operate purely on the provided PageElement.

### Methods

#### get_text

```python
@staticmethod
def get_text(
    element: PageElement,
    index: int | None = None,
    source: Literal[PageType.Unicode, PageType.PlainText] = PageType.Unicode
) -> str | None:
```

Find and extract the text content of a PageElement.

This method handles the TextEquiv structure automatically, navigating through the element hierarchy to find the appropriate text content.

##### Arguments

- `element`: The PageElement to extract text from.
- `index`: Selects a specific TextEquiv element by index. If not set and multiple TextEquiv elements are found, the first one with the lowest or no index is picked. Only applied if the element is a level above the TextEquivs.
- `source`: Selects whether to extract text from Unicode or PlainText elements. Defaults to PageType.Unicode.

##### Returns

The text content as a string, or None if no text was found.

##### Behavior

- If the element itself is a Unicode or PlainText element, returns its text directly.
- If the element is a TextEquiv, searches for the specified source within it.
- Otherwise, searches for TextEquiv children and extracts text from them.
- When multiple TextEquiv elements exist without specifying an index, selects the one with the lowest index value.
