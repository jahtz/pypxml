# SPDX-License-Identifier: Apache-2.0
from pypxml import PageType, PageUtil


class TestPageUtil:
    """
    Test PageUtil functionality.
    """
    
    def test_get_text_from_unicode(self, sample_pagexml_with_regions):
        """
        Test extracting text from Unicode element
        ."""
        line = sample_pagexml_with_regions.find(id='l1', depth=-1)
        text = PageUtil.get_text(line)
        assert text == 'Hello World'
    
    def test_get_text_from_textequiv(self, sample_pagexml_with_regions):
        """
        Test extracting text from TextEquiv.
        """
        line = sample_pagexml_with_regions.find(id='l1', depth=-1)
        textequiv = line.find(pagetype=PageType.TextEquiv)
        text = PageUtil.get_text(textequiv)
        assert text == 'Hello World'
    
    def test_get_text_with_plaintext(self, sample_pagexml):
        """
        Test extracting PlainText instead of Unicode.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        line = region.create(PageType.TextLine, id='l1')
        textequiv = line.create(PageType.TextEquiv)
        plaintext = textequiv.create(PageType.PlainText)
        plaintext.text = 'Plain text content'
        
        text = PageUtil.get_text(line, source=PageType.PlainText)
        assert text == 'Plain text content'
    
    def test_get_text_returns_none_when_not_found(self, sample_pagexml):
        """
        Test that get_text returns None when no text found.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        text = PageUtil.get_text(region)
        assert text is None
