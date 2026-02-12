# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Literal

from .pageelement import PageElement
from .pagetypes import PageType


logger = logging.getLogger(__name__)


class PageUtil:
    """
    Utility helper class for common PAGE-XML operations.

    This class provides convenience methods for extracting and resolving
    textual content from `PageElement` instances, abstracting away the
    structural complexity of PAGE-XML.

    The methods are stateless and operate purely on the provided
    `PageElement`, making this class a lightweight functional helper.
    """

    @staticmethod
    def get_text(
        element: PageElement, 
        index: int | None = None, 
        source: Literal[PageType.Unicode, PageType.PlainText] = PageType.Unicode
    ) -> str | None:
        """
        Find the text of a `PageElement` object.
        Args:
            index: Selects a certain TextEquiv element index. If index is not set and multiple TextEquiv elements are 
                found, the first one with the lowest or no index is picked. Only applied if the current element is 
                a level above the TextEquivs.
            source: Selects whether the text from Unicode or PlainText is picked.
        Returns:
            The text of the current element if it was found.
        """
        if element.pagetype in [PageType.Unicode, PageType.PlainText]:
            return element.text
        
        if element.pagetype == PageType.TextEquiv:
            textequivs = [element]
        else:
            textequivs = element.find_all(pagetype=PageType.TextEquiv, index=index)
        if len(textequivs) > 1:
            logger.warning('Multiple TextEquiv elements found. Selecting the element with the lowest index')
            textequivs.sort(key = lambda x: -1 if 'index' not in x else int(x['index']))
            
        if textequivs and (textelement := textequivs[0].find(pagetype=source)) is not None:
            return textelement.text
        return None
