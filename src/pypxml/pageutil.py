# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Literal

from .pageelement import PageElement
from .pagetype import PageType
from .pagexml import PageXML


logger: logging.Logger = logging.getLogger(__name__)


class PageUtil:
    """
    Utility helper class for common PAGE-XML operations.

    This class provides convenience methods for extracting and resolving textual content 
    from `PageElement` instances, abstracting away the structural complexity of PAGE-XML.
    """

    @staticmethod
    def find_text(
        element: PageElement,
        index: int | None = None,
        source: Literal[PageType.Unicode, PageType.PlainText] = PageType.Unicode
    ) -> str | None:
        """
        Find the text of a `PageElement`.

        Args:
            element: Element used for the search.
            index: Choose the `index` attribute of the TextEquiv element. If the index is not set and multiple TextEquiv
                elements are found, the lowest (or no) index is picked. Only applied if the passed element is at least
                one level above the TextEquiv elements. Defaults to None.
            source: Use either Unicode or PlainText as the text source. Defaults to PageType.Unicode.

        Returns:
            The text of the passed `PageElement` if it was found.
        """
        if element.pagetype in [PageType.Unicode, PageType.PlainText]:
            return element.text
        
        if element.pagetype == PageType.TextEquiv:
            textequivs: list[PageElement] = [element]
        else:
            args: dict[str, str] = {'index': str(index)} if index is not None else {}
            textequivs: list[PageElement] = list(element.find_all(PageType.TextEquiv, 0, **args))
        if len(textequivs) > 1:
            logger.warning('Multiple TextEquiv elements found. Selecting the element with the lowest index')
            textequivs.sort(key = lambda x: -1 if 'index' not in x else int(x['index']))
        
        if textequivs and (textelement := textequivs[0].find(source)) is not None:
            return textelement.text
        return None
    
    @staticmethod
    def sort_regions(
        pagexml: PageXML,
        reference: Literal['minimum', 'maximum', 'centroid'] = 'minimum',
        direction: Literal['top-bottom', 'bottom-top', 'left-right', 'right-left'] = 'top-bottom',
        apply: bool = True
    ) -> None:
        """
        Sort the regions in the PAGE-XML document by their relative location on the page.
        
        Args:
            reference: The method for determining the reference point used for sorting:
                - `minimum` sorts by the minimum coordinate value in the given direction,
                - `maximum` sorts by the maximum coordinate value in the given direction,
                - `centroid` sorts by the centroid position of each region.
                Defaults to 'minimum'.
            direction: The primary direction in which regions are sorted. Defaults to 'top-bottom'.
            apply: If True, also reorders the sequence of region elements in the PAGE-XML document. If False, only 
                updates the reading order element without changing the actual element order. Defaults to True.
        """
        def sort_key(obj: PageElement):
            if not obj.is_region:
                return (0, 0)
            elif (coords := obj.find(PageType.Coords)) is not None and 'points' in coords:
                points: list[tuple[int, ...]] = [tuple(map(int, xy.split(','))) for xy in str(coords['points']).split()]
                axis: Literal[0, 1] = 1 if direction in ['top-bottom', 'bottom-top'] else 0  # 0: x, 1: y
                if reference == 'minimum':
                    key: int | float = min(p[axis] for p in points)
                elif reference == 'maximum':
                    key: int | float = max(p[axis] for p in points)
                else:
                    key: int | float = sum(p[axis] for p in points) / len(points)
                if direction in ['bottom-top', 'right-left']:
                    return (1, -key)
                return (1, key) 
            else:
                return (2, 0)
    
        pagexml.elements.sort(key=sort_key)
        pagexml.set_reading_order(
            [str(e['id']) for e in pagexml.elements if e.is_region and 'id' in e],
            apply
        )
