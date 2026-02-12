# SPDX-License-Identifier: Apache-2.0
import pytest
from pypxml import PageXML, PageType, PageUtil


class TestIntegration:
    """
    End-to-end integration tests.
    """
    
    def test_create_modify_save_reload(self, temp_xml_file):
        """
        Test full workflow: create, modify, save, reload.
        """
        # Create
        pagexml = PageXML(
            creator='integration_test',
            imageFilename='test.jpg',
            imageWidth='1000',
            imageHeight='800'
        )
        
        # Add regions
        region = pagexml.create(PageType.TextRegion, id='r1', custom='paragraph')
        region.create(PageType.Coords, points='100,100 500,100 500,200 100,200')
        
        line = region.create(PageType.TextLine, id='l1')
        line.create(PageType.Coords, points='100,100 500,100 500,120 100,120')
        
        textequiv = line.create(PageType.TextEquiv, index='0')
        unicode_elem = textequiv.create(PageType.Unicode)
        unicode_elem.text = 'Integration test text'
        
        # Create reading order
        pagexml.reading_order_create()
        
        # Save
        pagexml.save(temp_xml_file)
        
        # Reload
        reloaded = PageXML.open(temp_xml_file)
        
        # Verify
        assert reloaded.creator == 'integration_test'
        assert len(reloaded.regions) == 1
        
        reloaded_line = reloaded.find(id='l1', depth=-1)
        text = PageUtil.get_text(reloaded_line)
        assert text == 'Integration test text'
        
        assert len(reloaded.reading_order) == 1
    
    def test_complex_document_structure(self, temp_xml_file):
        """
        Test creating a complex document with multiple regions and reading order.
        """
        pagexml = PageXML(imageFilename='complex.jpg', imageWidth=2000, imageHeight='3000')
        
        # Create multiple regions
        for i in range(5):
            y_offset = i * 200
            region = pagexml.create(
                PageType.TextRegion,
                id=f'r{i+1}',
                custom='paragraph'
            )
            region.create(
                PageType.Coords,
                points=f'100,{100+y_offset} 500,{100+y_offset} 500,{200+y_offset} 100,{200+y_offset}'
            )
            
            # Add text lines
            for j in range(3):
                line_y = 100 + y_offset + (j * 30)
                line = region.create(PageType.TextLine, id=f'r{i+1}_l{j+1}')
                line.create(
                    PageType.Coords,
                    points=f'100,{line_y} 500,{line_y} 500,{line_y+20} 100,{line_y+20}'
                )
                textequiv = line.create(PageType.TextEquiv, index='0')
                unicode_elem = textequiv.create(PageType.Unicode)
                unicode_elem.text = f'Region {i+1}, Line {j+1}'
        
        # Sort reading order
        pagexml.reading_order_sort(direction='top-bottom')
        
        # Save and reload
        pagexml.save(temp_xml_file)
        reloaded = PageXML.open(temp_xml_file)
        
        # Verify structure
        assert len(reloaded.regions) == 5
        assert len(reloaded.reading_order) == 5
        
        # Verify reading order is correct (top to bottom)
        assert reloaded.reading_order == ['r1', 'r2', 'r3', 'r4', 'r5']
        
        # Verify text extraction
        all_lines = reloaded.find_all(pagetype=PageType.TextLine, depth=-1)
        assert len(all_lines) == 15  # 5 regions * 3 lines each
    
    def test_error_handling(self, invalid_xml_file):
        """
        Test that invalid XML is handled gracefully.
        """
        with pytest.raises(Exception):
            PageXML.open(invalid_xml_file)
    
    def test_modification_workflow(self, sample_xml_file, temp_xml_file):
        """
        Test opening, modifying, and saving a document.
        """
        # Open
        pagexml = PageXML.open(sample_xml_file)
        
        # Modify: add new region
        new_region = pagexml.create(PageType.TextRegion, id='r_new', custom='new')
        new_region.create(PageType.Coords, points='300,300 400,300 400,400 300,400')
        
        # Modify: update existing element
        existing = pagexml.find(id='r1')
        existing['custom'] = 'modified_paragraph'
        
        # Save
        pagexml.save(temp_xml_file)
        
        # Reload and verify
        reloaded = PageXML.open(temp_xml_file)
        assert reloaded.find(id='r_new') is not None
        assert reloaded.find(id='r1')['custom'] == 'modified_paragraph'
