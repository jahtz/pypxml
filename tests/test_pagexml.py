# SPDX-License-Identifier: Apache-2.0
import pytest
from datetime import datetime
from pypxml import PageXML, PageElement, PageType, PageSchema


class TestPageXMLCreation:
    """
    Test PageXML object creation and initialization.
    """
    
    def test_create_empty(self):
        """
        Test creating PageXML with custom metadata.
        """
        now = datetime.now()
        pagexml = PageXML(
            creator='test_creator',
            created=now,
            last_change=now
        )
        assert pagexml.creator == 'test_creator'
        assert pagexml.created == now.isoformat()
        assert pagexml.last_change == now.isoformat()
    
    def test_create_with_attributes(self):
        """
        Test creating PageXML with Page attributes.
        """
        pagexml = PageXML(
            imageFilename='test.jpg',
            imageWidth='1000',
            imageHeight='800'
        )
        assert pagexml['imageFilename'] == 'test.jpg'
        assert pagexml['imageWidth'] == '1000'
        assert pagexml['imageHeight'] == '800'


class TestPageXMLFileOperations:
    """
    Test file I/O operations.
    """
    
    def test_open_valid_file(self, sample_xml_file):
        """
        Test opening a valid PageXML file.
        """
        pagexml = PageXML.open(sample_xml_file)
        assert pagexml is not None
        assert pagexml.creator == 'pytest'
        assert len(pagexml) > 0
    
    def test_open_nonexistent_file(self):
        """
        Test opening a file that doesn't exist.
        """
        with pytest.raises(Exception):
            PageXML.open('nonexistent.xml')
    
    def test_save_and_reload(self, sample_pagexml_with_regions, temp_xml_file):
        """
        Test saving and reloading a PageXML file.
        """
        sample_pagexml_with_regions.save(temp_xml_file)
        assert temp_xml_file.exists()
        
        reloaded = PageXML.open(temp_xml_file)
        assert len(reloaded) == len(sample_pagexml_with_regions)
        assert reloaded.creator == sample_pagexml_with_regions.creator
    
    def test_save_with_schema_2019(self, sample_pagexml, temp_xml_file):
        """
        Test saving with 2019 schema.
        """
        sample_pagexml.save(temp_xml_file, schema='2019')
        content = temp_xml_file.read_text()
        assert '2019-07-15' in content
    
    def test_save_with_schema_2017(self, sample_pagexml, temp_xml_file):
        """
        Test saving with 2017 schema.
        """
        sample_pagexml.save(temp_xml_file, schema='2017')
        content = temp_xml_file.read_text()
        assert '2017-07-15' in content


class TestPageXMLSearch:
    """
    Test search functionality (find, find_all).
    """
    
    def test_find_all_by_type(self, sample_pagexml_with_regions):
        """
        Test finding all elements by type.
        """
        regions = sample_pagexml_with_regions.find_all(pagetype=PageType.TextRegion)
        assert len(regions) == 2
        assert all(r.pagetype == PageType.TextRegion for r in regions)
    
    def test_find_all_by_id(self, sample_pagexml_with_regions):
        """
        Test finding elements by ID.
        """
        result = sample_pagexml_with_regions.find_all(id='r1')
        assert len(result) == 1
        assert result[0]['id'] == 'r1'
    
    def test_find_all_with_depth(self, sample_pagexml_with_regions):
        """
        Test depth-limited search.
        """
        # Depth 0: only direct children
        regions = sample_pagexml_with_regions.find_all(pagetype=PageType.TextLine, depth=0)
        assert len(regions) == 0
        
        # Depth -1: unlimited depth
        lines = sample_pagexml_with_regions.find_all(pagetype=PageType.TextLine, depth=-1)
        assert len(lines) == 2
    
    def test_find_single_element(self, sample_pagexml_with_regions):
        """
        Test finding a single element.
        """
        region = sample_pagexml_with_regions.find(id='r1')
        assert region is not None
        assert region['id'] == 'r1'
    
    def test_find_returns_none_when_not_found(self, sample_pagexml_with_regions):
        """
        Test that find returns None when element not found.
        """
        result = sample_pagexml_with_regions.find(id='nonexistent')
        assert result is None
    
    def test_find_all_by_attributes(self, sample_pagexml_with_regions):
        """
        Test finding by custom attributes.
        """
        result = sample_pagexml_with_regions.find_all(
            pagetype=PageType.TextRegion, 
            depth=-1, 
            custom='paragraph'
        )
        assert len(result) == 1


class TestPageXMLElementManagement:
    """
    Test creating, setting, and deleting elements.
    """
    
    def test_create_element(self, sample_pagexml):
        """
        Test creating a new element.
        """
        region = sample_pagexml.create(PageType.TextRegion, id='r1')
        assert region is not None
        assert region.pagetype == PageType.TextRegion
        assert len(sample_pagexml) == 1
    
    def test_set_element(self, sample_pagexml):
        """
        Test adding an existing element.
        """
        region = PageElement(PageType.TextRegion, sample_pagexml, id='r1')
        sample_pagexml.set(region)
        assert len(sample_pagexml) == 1
        assert region in sample_pagexml
    
    def test_delete_element(self, sample_pagexml_with_regions):
        """
        Test deleting an element.
        """
        initial_count = len(sample_pagexml_with_regions)
        region = sample_pagexml_with_regions.find(id='r1')
        sample_pagexml_with_regions.delete(region)
        assert len(sample_pagexml_with_regions) == initial_count - 1
    
    def test_clear_elements(self, sample_pagexml_with_regions):
        """
        Test clearing all elements.
        """
        sample_pagexml_with_regions.clear()
        assert len(sample_pagexml_with_regions) == 0
    
    def test_clear_regions_only(self, sample_pagexml_with_regions):
        """
        Test clearing only regions.
        """
        sample_pagexml_with_regions.clear(regions_only=True)
        assert len(sample_pagexml_with_regions.regions) == 0


class TestReadingOrder:
    """
    Test reading order functionality.
    """
    
    def test_reading_order_create(self, sample_pagexml_with_regions):
        """
        Test creating reading order.
        """
        sample_pagexml_with_regions.reading_order_create()
        ro = sample_pagexml_with_regions.reading_order
        assert len(ro) == 2
        assert 'r1' in ro
        assert 'r2' in ro
    
    def test_reading_order_set(self, sample_pagexml_with_regions):
        """
        Test setting reading order manually.
        """
        sample_pagexml_with_regions.reading_order_set(['r2', 'r1'])
        ro = sample_pagexml_with_regions.reading_order
        assert ro == ['r2', 'r1']
    
    def test_reading_order_clear(self, sample_pagexml_with_regions):
        """
        Test clearing reading order.
        """
        sample_pagexml_with_regions.reading_order_create()
        sample_pagexml_with_regions.reading_order_clear()
        assert len(sample_pagexml_with_regions.reading_order) == 0
    
    def test_reading_order_sort_top_bottom(self, sample_pagexml_with_regions):
        """
        Test sorting reading order by position.
        """
        sample_pagexml_with_regions.reading_order_sort(direction='top-bottom')
        ro = sample_pagexml_with_regions.reading_order
        # r1 is at y=100, r2 is at y=300, so r1 should come first
        assert ro[0] == 'r1'
        assert ro[1] == 'r2'
    
    def test_reading_order_apply(self, sample_pagexml_with_regions):
        """
        Test applying reading order to element sequence.
        """
        sample_pagexml_with_regions.reading_order_set(['r2', 'r1'])
        sample_pagexml_with_regions.reading_order_apply()
        regions = sample_pagexml_with_regions.regions
        assert regions[0]['id'] == 'r2'
        assert regions[1]['id'] == 'r1'
