import pytest

from src.toolsData import ToolJSON

MOCK_URL = 'C:\\mock\\url'

EXPECTED_SHORTCUTS = ['C:\\path\\program.exe', 'D:\\path\\payday.exe', 'C:\\path\\map_builder.exe']

@pytest.fixture(scope='module')
def create_ToolJSON(createTemp_externalShortcuts_ini: str) -> ToolJSON:
    return ToolJSON(createTemp_externalShortcuts_ini)

def test_getShortcuts(create_ToolJSON: ToolJSON) -> None:
    assert create_ToolJSON.getShortcuts() == EXPECTED_SHORTCUTS

def test_newTool(create_ToolJSON: ToolJSON) -> None:
    create_ToolJSON.newTool(MOCK_URL)
    assert create_ToolJSON.getShortcuts()[-1] == MOCK_URL
    create_ToolJSON.newTool(MOCK_URL)
    assert create_ToolJSON.getShortcuts().count(MOCK_URL) == 1  # Testing dupe prevention

def test_removeTool(create_ToolJSON: ToolJSON) -> None:
    create_ToolJSON.removeTool(MOCK_URL)
    assert MOCK_URL not in create_ToolJSON.getShortcuts()

def test_changeTool(create_ToolJSON: ToolJSON) -> None:
    create_ToolJSON.changeTool(EXPECTED_SHORTCUTS[1], MOCK_URL)
    assert create_ToolJSON.getShortcuts()[1] == MOCK_URL