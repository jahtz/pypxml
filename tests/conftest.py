# SPDX-License-Identifier: Apache-2.0
import pytest
from pypxml import PageXML, PageType


@pytest.fixture
def temp_xml_file(tmp_path):
    """
    Creates a temporary XML file path for testing.
    """
    return tmp_path / 'test_page.xml'


@pytest.fixture
def sample_pagexml():
    """
    Creates a simple PageXML object for testing.
    """
    pagexml = PageXML(
        creator='pytest',
        created='2026-01-01T12:00:00Z',
        last_change='2026-01-01T12:00:00Z',
        imageFilename='test.jpg',
        imageWidth='1000',
        imageHeight='800'
    )
    return pagexml


@pytest.fixture
def sample_pagexml_with_regions(sample_pagexml):
    """
    Creates a PageXML object with text regions.
    """
    pagexml = sample_pagexml
    
    # Create first text region
    region1 = pagexml.create(
        PageType.TextRegion,
        id='r1',
        custom='paragraph'
    )
    coords1 = region1.create(PageType.Coords, points='100,100 200,100 200,200 100,200')
    
    textline1 = region1.create(PageType.TextLine, id='l1')
    coords_line1 = textline1.create(PageType.Coords, points='100,100 200,100 200,120 100,120')
    textequiv1 = textline1.create(PageType.TextEquiv, i=0)
    unicode1 = textequiv1.create(PageType.Unicode)
    unicode1.text = 'Hello World'
    
    # Create second text region
    region2 = pagexml.create(PageType.TextRegion, id='r2', custom='heading')
    coords2 = region2.create(PageType.Coords, points='100,300 200,300 200,400 100,400')
    
    textline2 = region2.create(PageType.TextLine, id='l2')
    coords_line2 = textline2.create(PageType.Coords, points='100,300 200,300 200,320 100,320')
    textequiv2 = textline2.create(PageType.TextEquiv, i=0)
    unicode2 = textequiv2.create(PageType.Unicode)
    unicode2.text = 'Test Heading'
    
    return pagexml


@pytest.fixture
def sample_xml_string():
    """
    Returns a valid PageXML string for parsing tests.
    """
    return '''<?xml version="1.0" encoding="UTF-8"?>
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15">
    <Metadata>
        <Creator>pytest</Creator>
        <Created>2026-01-01T00:00:00Z</Created>
        <LastChange>2026-01-01T00:00:00Z</LastChange>
    </Metadata>
    <Page imageFilename="test.jpg" imageWidth="1000" imageHeight="800">
        <TextRegion id="r1" custom="paragraph">
            <Coords points="100,100 200,100 200,200 100,200"/>
            <TextLine id="l1">
                <Coords points="100,100 200,100 200,120 100,120"/>
                <TextEquiv index="0">
                    <Unicode>Hello World</Unicode>
                </TextEquiv>
            </TextLine>
        </TextRegion>
    </Page>
</PcGts>'''


@pytest.fixture
def sample_xml_file(tmp_path, sample_xml_string):
    """
    Creates a temporary XML file with sample content.
    """
    xml_file = tmp_path / 'sample.xml'
    xml_file.write_text(sample_xml_string)
    return xml_file


@pytest.fixture
def invalid_xml_file(tmp_path):
    """
    Creates an invalid XML file for error handling tests.
    """
    xml_file = tmp_path / 'invalid.xml'
    xml_file.write_text('This is not valid XML')
    return xml_file
