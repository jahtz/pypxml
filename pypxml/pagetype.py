# Copyright 2025 Janik Haitz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
from typing import Union, Self


class PageType(Enum):
    """
    Reference: https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page
    """

    # ReadingOrder
    ReadingOrder = "ReadingOrder"
    """
    Definition of the reading order within the page. To express a reading order between elements they have to be 
    included in an OrderedGroup. Groups may contain further groups.
    """
    
    RegionRef = "RegionRef"
    """
    Region reference.
    """
    
    OrderedGroup = "OrderedGroup"
    """
    Numbered group (contains ordered elements).
    """
    
    UnorderedGroup = "UnorderedGroup"
    """
    Numbered group (contains ordered elements)
    """
    
    OrderedGroupIndexed = "OrderedGroupIndexed"
    """
    Indexed group containing ordered elements.
    """
    
    UnorderedGroupIndexed = "UnorderedGroupIndexed"
    """
    Indexed group containing unordered elements.
    """
    
    RegionRefIndexed = "RegionRefIndexed"
    """
    Numbered region.
    """

    # Regions
    AdvertRegion = "AdvertRegion"
    """
    Regions containing advertisements.
    """
    
    ChartRegion = "ChartRegion"
    """
    Regions containing charts or graphs of any type, should be marked as chart regions.
    """
    
    ChemRegion = "ChemRegion"
    """
    Regions containing chemical formulas.
    """
    
    CustomRegion = "CustomRegion"
    """
    Regions containing content that is not covered by the default types (text, graphic, image, line drawing, chart, 
    table, separator, maths, map, music, chem, advert, noise, unknown).
    """
    
    GraphicRegion = "GraphicRegion"
    """
    Regions containing simple graphics, such as company logo, should be marked as graphic regions.
    """
    
    ImageRegion = "ImageRegion"
    """
    An image is considered to be more intricated and complex than a graphic. These can be photos or drawings.
    """
    
    LineDrawingRegion = "LineDrawingRegion"
    """
    A line drawing is a single colour illustration without solid areas.
    """
    
    MapRegion = "MapRegion"
    """
    Regions containing maps.
    """
    
    MathsRegion = "MathsRegion"
    """
    Regions containing equations and mathematical symbols should be marked as maths regions.
    """
    
    MusicRegion = "MusicRegion"
    """
    Regions containing musical notations.
    """
    
    NoiseRegion = "NoiseRegion"
    """
    Noise regions are regions where no real data lies, only false data created by artifacts on the document or scanner 
    noise.
    """
    
    SeparatorRegion = "SeparatorRegion"
    """
    Separators are lines that lie between columns and paragraphs and can be used to logically separate different 
    articles from each other.
    """
    
    TableRegion = "TableRegion"
    """
    Tabular data in any form is represented with a table region. Rows and columns may or may not have separator lines; 
    these lines are not separator regions.
    """
    
    TextRegion = "TextRegion"
    """
    Pure text is represented as a text region. This includes drop capitals, but practically ornate text may be 
    considered as a graphic.
    """
    
    UnknownRegion = "UnknownRegion"
    """
    To be used if the region type cannot be ascertained.
    """

    # Elements
    AlternativeImage = "AlternativeImage"
    """
    Alternative region images (e.g. black-and-white)
    """
    
    Baseline = "Baseline"
    """
    Multiple connected points that mark the baseline of the glyphs.
    """
    
    Border = "Border"
    """
    Border of the actual page (if the scanned image contains parts not belonging to the page).
    """
    
    Coords = "Coords"
    """
    Polygon outline of the element as a path of points. No points may lie outside the outline of its parent, which in 
    the case of Border is the bounding rectangle of the root image. Paths are closed by convention, i.e. the last point 
    logically connects with the first (and at least 3 points are required to span an area). 
    Paths must be planar (i.e. must not self-intersect).
    """
    
    Glyph = "Glyph"
    """
    No official annotation.
    """
    
    GraphemeGroup = "GraphemeGroup"
    """
    No official annotation.
    """
    
    Grapheme = "Grapheme"
    """
    No official annotation.
    """

    Grid = "Grid"
    """
    Table grid (visible or virtual grid lines).
    """
    
    GridPoints = "GridPoints"
    """
    One row in the grid point matrix. Points with x,y coordinates.
    """
    
    Label = "Label"
    """
    A semantic label / tag
    """
    
    Labels = "Labels"
    """
    Semantic labels / tags
    """
    
    Layer = "Layer"
    """
    No official annotation.
    """
    
    Layers = "Layers"
    """
    Unassigned regions are considered to be in the (virtual) default layer which is to be treated as below any other 
    layers.
    """
    
    Metadata = "Metadata"
    """
    No official annotation.
    """
    
    NonPrintingChar = "NonPrintingChar"
    """
    A glyph component without visual representation but with Unicode code point. 
    Non-visual / non-printing / control character. Part of grapheme container (of glyph) or grapheme sub group.
    """
    
    PlainText = "PlainText"
    """
    Text in a "simple" form (ASCII or extended ASCII as mostly used for typing). I.e. no use of special characters for 
    ligatures (should be stored as two separate characters) etc.
    """
    
    PrintSpace = "PrintSpace"
    """
    Determines the effective area on the paper of a printed page. Its size is equal for all pages of a book 
    (exceptions: titlepage, multipage pictures). It contains all living elements (except marginals) like body type, 
    footnotes, headings, running titles. It does not contain pagenumber (if not part of running title), marginals, 
    signature mark, preview words.   
    """
    
    Relations = "Relations"
    """
    Container for one-to-one relations between layout objects (for example: DropCap - paragraph, caption - image).
    """
    
    Roles = "Roles"
    """
    Roles the region takes (e.g. in context of a parent region)
    """
    
    TextEquiv = "TextEquiv"
    """
    No official annotation.
    """
    
    TextLine = "TextLine"
    """
    No official annotation.
    """
    
    TextStyle = "TextStyle"
    """
    Monospace (fixed-pitch, non-proportional) or proportional font.
    """
    
    Unicode = "Unicode"
    """
    Correct encoding of the original, always using the corresponding Unicode code point. I.e. ligatures have to be 
    represented as one character etc.
    """
    
    UserAttribute = "UserAttribute"
    """
    Structured custom data defined by name, type and value.
    """
    
    UserDefined = "UserDefined"
    """
    Container for user-defined attributes.
    """
    
    Word = "Word"
    """
    No official annotation.
    """
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other: Union[str, Self]):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
    
    @property
    def is_region(self):
        return self.value in ["AdvertRegion", "ChartRegion", "ChemRegion", "CustomRegion", "GraphicRegion", 
                              "ImageRegion", "LineDrawingRegion", "MapRegion", "MathsRegion", "MusicRegion", 
                              "NoiseRegion", "SeparatorRegion", "TableRegion", "TextRegion", "UnknownRegion"]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.__members__
        