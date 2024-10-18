# This file is licensed under the MIT License.
# Copyright (c) 2024 Janik Haitz
# See the LICENSE file in the root directory for more details.

from enum import Enum


class PageType(Enum):
    """
    https://ocr-d.de/de/gt-guidelines/pagexml/pagecontent_xsd_Complex_Type_pc_PcGtsType.html#PcGtsType_Page
    """

    # ReadingOrder
    ReadingOrder = "ReadingOrder"
    OrderedGroup = "OrderedGroup"
    RegionRefIndexed = "RegionRefIndexed"

    # Regions
    AdvertRegion = "AdvertRegion"
    ChartRegion = "ChartRegion"
    ChemRegion = "ChemRegion"
    CustomRegion = "CustomRegion"
    GraphicRegion = "GraphicRegion"
    ImageRegion = "ImageRegion"
    LineDrawingRegion = "LineDrawingRegion"
    MapRegion = "MapRegion"
    MathsRegion = "MathsRegion"
    MusicRegion = "MusicRegion"
    NoiseRegion = "NoiseRegion"
    SeparatorRegion = "SeparatorRegion"
    TableRegion = "TableRegion"
    TextRegion = "TextRegion"
    UnknownRegion = "UnknownRegion"

    # Elements
    AlternativeImage = "AlternativeImage"
    Baseline = "Baseline"
    Border = "Border"
    Coords = "Coords"
    Glyph = "Glyph"
    GraphemeGroup = "GraphemeGroup"
    Graphemes = "Graphemes"
    Grid = "Grid"
    Label = "Label"
    Labels = "Labels"
    Layers = "Layers"
    Metadata = "Metadata"
    NonPrintingChar = "NonPrintingChar"
    PlainText = "PlainText"
    PrintSpace = "PrintSpace"
    Relations = "Relations"
    Roles = "Roles"
    TextEquiv = "TextEquiv"
    TextLine = "TextLine"
    TextStyle = "TextStyle"
    Unicode = "Unicode"
    UserAttribute = "UserAttribute"
    UserDefined = "UserDefined"
    Word = "Word"
