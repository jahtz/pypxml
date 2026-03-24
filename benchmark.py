from datetime import datetime, timedelta
from pathlib import Path
from pypxml import PageXML, PageType, PageElement


LINE_PATHS: list[Path] = list(Path('...').glob('*.xml'))
WORD_PATHS: list[Path] = list(Path('...').glob('*.xml'))
GLYPH_PATHS: list[Path] = list(Path('...').glob('*.xml'))


def run_test_open(xmls: list[Path]) -> float:
    timings: list[float] = []
    for xml in xmls:
        start: datetime = datetime.now()
        page: PageXML = PageXML.open(xml)
        end: datetime = datetime.now()
        
        delta: timedelta = end - start
        timings.append(delta.total_seconds())
    return sum(timings) / len(timings)

 
def run_test_search(xmls: list[Path], pagetype: PageType) -> float:
    timings: list[float] = []
    for xml in xmls:
        page: PageXML = PageXML.open(xml)
        start: datetime = datetime.now()
        findings: list[PageElement] = list(page.find_all(pagetype, -1))
        end: datetime = datetime.now()
    
        delta: timedelta = end - start
        timings.append(delta.total_seconds())
    return sum(timings) / len(timings)


def run_test_write(xmls: list[Path]) -> float:
    timings: list[float] = []
    for xml in xmls:
        page: PageXML = PageXML.open(xml)
        start: datetime = datetime.now()
        page.save(xml)
        end: datetime = datetime.now()
        
        delta: timedelta = end - start
        timings.append(delta.total_seconds())
    return sum(timings) / len(timings)


print('Open')
print(f'LINE: {run_test_open(LINE_PATHS)}')
print(f'WORD: {run_test_open(WORD_PATHS)}')
print(f'GLYPH: {run_test_open(GLYPH_PATHS)}')

print('Search')
print(f'LINE: {run_test_search(LINE_PATHS, PageType.TextLine)}')
print(f'WORD: {run_test_search(WORD_PATHS, PageType.Word)}')
print(f'GLYPH: {run_test_search(GLYPH_PATHS, PageType.Glyph)}')

print('Open')
print(f'LINE: {run_test_write(LINE_PATHS)}')
print(f'WORD: {run_test_write(WORD_PATHS)}')
print(f'GLYPH: {run_test_write(GLYPH_PATHS)}')
