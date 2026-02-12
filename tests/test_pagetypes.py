# SPDX-License-Identifier: Apache-2.0
from pypxml import PageType


class TestPageType:
    """
    Test PageType enum functionality.
    """

    def test_is_region(self):
        """
        Test is_region property.
        """
        assert PageType.TextRegion.is_region is True
        assert PageType.ImageRegion.is_region is True
        assert PageType.TextLine.is_region is False
        assert PageType.Unicode.is_region is False
    
    def test_is_valid(self):
        """
        Test is_valid class method.
        """
        assert PageType.is_valid('TextRegion') is True
        assert PageType.is_valid('InvalidType') is False
    
    def test_equality_with_string(self):
        """
        Test equality comparison with strings.
        """
        assert PageType.TextRegion == 'TextRegion'
        assert PageType.TextRegion != 'TextLine'
