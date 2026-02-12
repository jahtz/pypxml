# SPDX-License-Identifier: Apache-2.0
import pytest
from pypxml import PageSchema


class TestPageSchema:
    """
    Test PageSchema functionality.
    """
    
    def test_get_schema_2019(self):
        """
        Test getting 2019 schema.
        """
        schema = PageSchema.get('2019')
        assert schema.xmlns == 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'
        assert schema.xmlns_xsi == 'http://www.w3.org/2001/XMLSchema-instance'
    
    def test_get_schema_2017(self):
        """
        Test getting 2017 schema.
        """
        schema = PageSchema.get('2017')
        assert schema.xmlns == 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15'
    
    def test_get_invalid_schema(self):
        """
        Test getting an invalid schema raises error.
        """
        with pytest.raises(ValueError):
            PageSchema.get('invalid_version')
    
    def test_custom_schema(self):
        """
        Test creating a custom schema.
        """
        schema = PageSchema.custom(
            xmlns='http://custom.namespace',
            xmlns_xsi='http://www.w3.org/2001/XMLSchema-instance',
            xsi_schema_location='http://custom.namespace http://custom.xsd'
        )
        assert schema.xmlns == 'http://custom.namespace'
    
    def test_schema_immutable(self):
        """
        Test that schema instances are immutable.
        """
        schema = PageSchema.get('2019')
        with pytest.raises(Exception):
            schema.xmlns = 'modified'
