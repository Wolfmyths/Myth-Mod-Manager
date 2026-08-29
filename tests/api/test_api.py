import xml.etree.ElementTree as et
import tempfile
import os
from collections.abc import Generator

import pytest
from PySide6.QtCore import QVersionNumber

from src.api import api

MOCK_DATA_ASSET_IDS = (
    ('<table><AssetUpdates id="1234" version="1.2.3" provider="modworkshop"/></table>', '1234'),
    ('<table></table>', ''),
    ('<table><elementThatIsNotRelevant/></table>', ''),
    ('', '')
)

MOCK_DATA_VERSIONS = (
     (MOCK_DATA_ASSET_IDS[0][0], QVersionNumber(1, 2, 3)),
     (MOCK_DATA_ASSET_IDS[1][0], None),
     (MOCK_DATA_ASSET_IDS[2][0], None),
     (MOCK_DATA_ASSET_IDS[3][0], None),
     ('<table><AssetUpdates id="1234" version="V1.4.0" provider="modworkshop"/></table>', QVersionNumber(1, 4, 0)),
     ('<table><AssetUpdates id="1234" version="v1.1.0" provider="modworkshop"/></table>', QVersionNumber(1, 1, 0))
)

@pytest.fixture(scope='function')
def create_testXML() -> Generator[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:

        with open(os.path.join(tmp_dir, 'main.xml'), 'w') as _tmp:
            pass

        yield tmp_dir
     

@pytest.mark.parametrize(('data', 'expected_outcome'), MOCK_DATA_ASSET_IDS)
def test_findModworkshopAssetID(create_testXML: str, data: str, expected_outcome: str) -> None:
        
    if data != '':
        et.ElementTree(et.fromstring(data)).write(os.path.join(create_testXML, 'main.xml'))

    assert api.findModworkshopAssetID(create_testXML) == expected_outcome

@pytest.mark.parametrize(('data', 'expected_outcome'), MOCK_DATA_VERSIONS)
def test_findModVersion(create_testXML: str, data: str, expected_outcome: str) -> None:

    if data != '':
        et.ElementTree(et.fromstring(data)).write(os.path.join(create_testXML, 'main.xml'))

    assert api.findModVersion(create_testXML) == expected_outcome