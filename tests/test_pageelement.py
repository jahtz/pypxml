# SPDX-License-Identifier: Apache-2.0
import pytest
from pypxml import PageElement, PageType


class TestPageElementCreation:
    """
    Test PageElement creation.
    """
    
    def test_create_element(self, sample_pagexml):
        """
        Test creating a PageElement.
        """
        element = PageElement(PageType.TextRegion, sample_pagexml, id='r1')
        assert element.pagetype == PageType.TextRegion
        assert element['id'] == 'r1'
        assert element.parent == sample_pagexml
    
    def test_create_element_with_invalid_parent(self):
        """
        Test that invalid parent raises error.
        """
        with pytest.raises(TypeError):
            PageElement(PageType.TextRegion, 'invalid_parent')
    
    def test_element_attributes(self, sample_pagexml):
        """
        Test element attributes.
        """
        element = PageElement(PageType.TextRegion, sample_pagexml, id='r1', custom='test')
        assert element['id'] == 'r1'
        assert element['custom'] == 'test'


class TestPageElementSearch:
    """
    Test search methods on PageElement.
    """
    
    def test_find_all_children(self, sample_pagexml_with_regions):
        """
        Test finding all child elements.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        lines = region.find_all(pagetype=PageType.TextLine)
        assert len(lines) == 1
    
    def test_find_all_recursive(self, sample_pagexml_with_regions):
        """
        Test recursive search.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        unicodes = region.find_all(pagetype=PageType.Unicode, depth=-1)
        assert len(unicodes) == 1
    
    def test_find_single_child(self, sample_pagexml_with_regions):
        """
        Test finding a single child element.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        coords = region.find(pagetype=PageType.Coords)
        assert coords is not None


class TestPageElementManipulation:
    """
    Test element manipulation methods.
    """
    
    def test_create_child(self, sample_pagexml):
        """
        Test creating a child element.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        coords = region.create(PageType.Coords, points='100,100 200,200')
        assert len(region) == 1
        assert coords.parent == region
    
    def test_set_child(self, sample_pagexml):
        """
        Test adding an existing child element.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        coords = PageElement(PageType.Coords, region, points='100,100 200,200')
        region.set(coords)
        assert len(region) == 1
    
    def test_delete_child(self, sample_pagexml_with_regions):
        """
        Test deleting a child element.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        initial_count = len(region)
        coords = region.find(pagetype=PageType.Coords)
        region.delete(coords)
        assert len(region) == initial_count - 1
    
    def test_clear_children(self, sample_pagexml_with_regions):
        """
        Test clearing all child elements.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        region.clear()
        assert len(region) == 0


class TestPageElementText:
    """
    Test text property.
    """
    
    def test_set_text(self, sample_pagexml):
        """
        Test setting text on an element.
        """
        region = sample_pagexml.create(PageType.Unicode)
        region.text = 'Test text'
        assert region.text == 'Test text'
    
    def test_clear_text(self, sample_pagexml):
        """
        Test clearing text.
        """
        region = sample_pagexml.create(PageType.Unicode)
        region.text = 'Test text'
        region.text = None
        assert region.text is None


class TestPageElementProperties:
    """
    Test PageElement properties.
    """
    
    def test_is_region(self, sample_pagexml):
        """
        Test is_region property.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        coords = region.create(PageType.Coords)
        assert region.is_region is True
        assert coords.is_region is False
    
    def test_pagetype_property(self, sample_pagexml):
        """
        Test pagetype property getter and setter.
        """
        element = PageElement(PageType.TextRegion, sample_pagexml)
        assert element.pagetype == PageType.TextRegion
        
        element.pagetype = PageType.ImageRegion
        assert element.pagetype == PageType.ImageRegion
        
        element.pagetype = 'TableRegion'
        assert element.pagetype == PageType.TableRegion
    
    def test_invalid_pagetype(self, sample_pagexml):
        """
        Test setting invalid pagetype.
        """
        element = PageElement(PageType.TextRegion, sample_pagexml)
        with pytest.raises(ValueError):
            element.pagetype = 'InvalidType'
