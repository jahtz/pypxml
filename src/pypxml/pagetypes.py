# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from enum import Enum


class PageType(Enum):
    """
    Enumeration of PAGE-XML element and region types.

    This enum mirrors the element and region names defined in the PAGE-XML schema (PcGtsType / Page content model) as 
    specified by the OCR-D ground truth guidelines:

    https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page

    It provides a typed representation of PAGE-XML node names and structural elements.
    """
    
    Metadata = 'Metadata'
    """
    No official annotation.
    """
    
    UserDefined = 'UserDefined'
    """
    Container for user-defined attributes.
    """
    
    UserAttribute = 'UserAttribute'
    """
    Structured custom data defined by name, type and value.
    """
    
    MetadataItem = 'MetadataItem'
    """
    No official annotation.
    """
    
    Labels = 'Labels'
    """
    Semantic labels
    """
    
    Label = 'Label'
    """
    A semantic label
    """
    
    AlternativeImage = 'AlternativeImage'
    """
    Alternative region images (e.g. black-and-white)
    """
    
    Border = 'Border'
    """
    Border of the actual page (if the scanned image contains parts not belonging to the page).
    """
    
    Coords = 'Coords'
    """
    No official annotation.
    """
    
    PrintSpace = 'PrintSpace'
    """
    Determines the effective area on the paper of a printed page. Its size is equal for all pages of a book 
    (exceptions: titlepage, multipage pictures). It contains all living elements (except marginals) like body type, 
    footnotes, headings, running titles. It does not contain pagenumber (if not part of running title), marginals, 
    signature mark, preview words.   
    """
    
    ReadingOrder = 'ReadingOrder'
    """
    Definition of the reading order within the page. To express a reading order between elements they have to be 
    included in an OrderedGroup. Groups may contain further groups.
    """
    
    OrderedGroup = 'OrderedGroup'
    """
    Numbered group (contains ordered elements).
    """
    
    RegionRefIndexed = 'RegionRefIndexed'
    """
    Numbered region.
    """
    
    OrderedGroupIndexed = 'OrderedGroupIndexed'
    """
    Indexed group containing ordered elements.
    """
    
    UnorderedGroupIndexed = 'UnorderedGroupIndexed'
    """
    Indexed group containing unordered elements.
    """
    
    RegionRef = 'RegionRef'
    """
    No official annotation.
    """
    
    UnorderedGroup = 'UnorderedGroup'
    """
    Numbered group (contains ordered elements)
    """
    
    Layers = 'Layers'
    """
    Can be used to express the z-index of overlapping regions. An element with a greater z-index is always in
    front of another element with lower z-index.
    """
    
    Layer = 'Layer'
    """
    No official annotation.
    """
    
    Relations = 'Relations'
    """
    Container for one-to-one relations between layout objects (for example: DropCap - paragraph, caption - image).
    """
    
    Relation = 'Relation'
    """
    One-to-one relation between to layout object. Use 'link' for loose relations and 'join' for strong relations
    (where something is fragmented for instance). Examples for 'link': caption - image floating - paragraph paragraph - 
    paragraph (when a paragraph is split across columns and the last word of the first paragraph DOES NOT continue in 
    the second paragraph) drop-cap - paragraph (when the drop-cap is a whole word) Examples for 'join': word - word 
    (separated word at the end of a line) drop-cap - paragraph (when the drop-cap is not a whole word) paragraph - 
    paragraph (when a pragraph is split across columns and the last word of the first paragraph DOES continue in the 
    second paragraph)
    """
    
    TextStyle = 'TextStyle'
    """
    Monospace (fixed-pitch, non-proportional) or proportional font.
    """
    
    TextRegion = 'TextRegion'
    """
    Pure text is represented as a text region. This includes drop capitals, but practically ornate text may be 
    considered as a graphic.
    """
    
    Roles = 'Roles'
    """
    No official annotation.
    """
    
    TableCellRole = 'TableCellRole'
    """
    Data for a region that takes on the role of a table cell within a parent table region.
    """
    
    ImageRegion = 'ImageRegion'
    """
    An image is considered to be more intricated and complex than a graphic. These can be photos or drawings.
    """
    
    LineDrawingRegion = 'LineDrawingRegion'
    """
    A line drawing is a single colour illustration without solid areas.
    """
    
    GraphicRegion = 'GraphicRegion'
    """
    Regions containing simple graphics, such as company logo, should be marked as graphic regions.
    """
    
    TableRegion = 'TableRegion'
    """
    Tabular data in any form is represented with a table region. Rows and columns may or may not have separator lines; 
    these lines are not separator regions.
    """
    
    ChartRegion = 'ChartRegion'
    """
    Regions containing charts or graphs of any type, should be marked as chart regions.
    """
    
    SeparatorRegion = 'SeparatorRegion'
    """
    Separators are lines that lie between columns and paragraphs and can be used to logically separate different 
    articles from each other.
    """
    
    MathsRegion = 'MathsRegion'
    """
    Regions containing equations and mathematical symbols should be marked as maths regions.
    """
    
    ChemRegion = 'ChemRegion'
    """
    Regions containing chemical formulas.
    """
    
    MusicRegion = 'MusicRegion'
    """
    Regions containing musical notations.
    """
    
    AdvertRegion = 'AdvertRegion'
    """
    Regions containing advertisements.
    """
    
    NoiseRegion = 'NoiseRegion'
    """
    Noise regions are regions where no real data lies, only false data created by artifacts on the document or scanner 
    noise.
    """
    
    UnknownRegion = 'UnknownRegion'
    """
    To be used if the region type cannot be ascertained.
    """
    
    CustomRegion = 'CustomRegion'
    """
    Regions containing content that is not covered by the default types (text, graphic, image, line drawing, chart, 
    table, separator, maths, map, music, chem, advert, noise, unknown).
    """
    
    Grid = 'Grid'
    """
    Matrix of grid points defining the table grid on the page.
    """
    
    GridPoints = 'GridPoints'
    """
    Points with x,y coordinates.
    """
    
    TextLine = 'TextLine'
    """
    No official annotation.
    """
    
    Baseline = 'Baseline'
    """
    No official annotation.
    """
    
    Word = 'Word'
    """
    No official annotation.
    """
    
    Glyph = 'Glyph'
    """
    No official annotation.
    """
    
    Graphemes = 'Graphemes'
    """
    Container for graphemes, grapheme groups and non-printing characters.
    """
    
    Grapheme = 'Grapheme'
    """
    Represents a sub-element of a glyph. Smallest graphical unit that can be assigned a Unicode code point.
    """
    
    TextEquiv = 'TextEquiv'
    """
    No official annotation.
    """
    
    NonPrintingChar = 'NonPrintingChar'
    """
    A glyph component without visual representation but with Unicode code point. 
    Non-visual / non-printing / control character. Part of grapheme container (of glyph) or grapheme sub group.
    """
    
    GraphemeGroup = 'GraphemeGroup'
    """
    No official annotation.
    """
    
    MapRegion = 'MapRegion'
    """
    Regions containing maps.
    """
 
    PlainText = 'PlainText'
    """
    Text in a 'simple' form (ASCII or extended ASCII as mostly used for typing). I.e. no use of special characters for 
    ligatures (should be stored as two separate characters) etc.
    """

    Unicode = 'Unicode'
    """
    Correct encoding of the original, always using the corresponding Unicode code point. I.e. ligatures have to be 
    represented as one character etc.
    """
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other: PageType | str):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
    
    @property
    def is_region(self):
        return self.value in [
            'AdvertRegion', 'ChartRegion', 'ChemRegion', 'CustomRegion', 'GraphicRegion', 'ImageRegion', 
            'LineDrawingRegion', 'MapRegion', 'MathsRegion', 'MusicRegion', 'NoiseRegion', 'SeparatorRegion', 
            'TableRegion', 'TextRegion', 'UnknownRegion'
        ]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.__members__
