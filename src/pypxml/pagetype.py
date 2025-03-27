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


class PageType(Enum):
    """
    https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page
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
    
    """
    
    Border = "Border"
    """
    
    """
    
    Coords = "Coords"
    """
    
    """
    
    Glyph = "Glyph"
    """
    
    """
    
    GraphemeGroup = "GraphemeGroup"
    """
    
    """
    
    Graphemes = "Graphemes"
    """
    
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
    
    """
    
    Layers = "Layers"
    """
    Unassigned regions are considered to be in the (virtual) default layer which is to be treated as below any other 
    layers.
    """
    
    Metadata = "Metadata"
    """
    
    """
    
    NonPrintingChar = "NonPrintingChar"
    """
    
    """
    
    PlainText = "PlainText"
    """
    
    """
    
    PrintSpace = "PrintSpace"
    """
    
    """
    
    Relations = "Relations"
    """
    
    """
    
    Roles = "Roles"
    """
    Roles the region takes (e.g. in context of a parent region)
    """
    
    TextEquiv = "TextEquiv"
    """
    
    """
    
    TextLine = "TextLine"
    """
    
    """
    
    TextStyle = "TextStyle"
    """
    Default text style.
    """
    
    Unicode = "Unicode"
    """
    
    """
    
    UserAttribute = "UserAttribute"
    """
    
    """
    
    UserDefined = "UserDefined"
    """
    
    """
    
    Word = "Word"
    """
    
    """


def is_valid(value: str) -> bool:
    """ Returns true if string is a valid XML type """
    return value in PageType.__members__


def is_region(value: str) -> bool:
    """ Returns true if string is a valid XML region type """
    return value in [PageType.AdvertRegion,
                     PageType.ChartRegion,
                     PageType.ChemRegion,
                     PageType.CustomRegion,
                     PageType.GraphicRegion,
                     PageType.ImageRegion,
                     PageType.LineDrawingRegion,
                     PageType.MapRegion,
                     PageType.MathsRegion,
                     PageType.MusicRegion,
                     PageType.NoiseRegion,
                     PageType.SeparatorRegion,
                     PageType.TableRegion,
                     PageType.TextRegion,
                     PageType.UnknownRegion]
