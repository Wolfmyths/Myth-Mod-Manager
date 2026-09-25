from collections.abc import Generator
import tempfile
import os

import pytest

from src.objects.worker import Worker

MOCK_FOLDER_NAME = "regular_folder"
MOCK_FOLDER_NAME1 = "permission_folder"
MOCK_FOLDER_NAME2 = "non-existant_folder"
MOCK_FOLDER_NAME3 = "sub_permission_folder"

@pytest.fixture(scope="module")
def create_worker() -> Generator[Worker]:
    worker = Worker()

    yield worker

    worker.deleteLater()

@pytest.fixture(scope="module")
def create_tmp_src() -> Generator[str]:
    with tempfile.TemporaryDirectory() as tmp_src:
        os.mkdir(os.path.join(tmp_src, MOCK_FOLDER_NAME))
        os.mkdir(os.path.join(tmp_src, MOCK_FOLDER_NAME1))
        os.mkdir(os.path.join(tmp_src, MOCK_FOLDER_NAME1, MOCK_FOLDER_NAME3))

        yield tmp_src

@pytest.fixture(scope="module")
def create_tmp_dest() -> Generator[str]:
    with tempfile.TemporaryDirectory() as tmp_dest:
        yield tmp_dest

# TODO: Find out why I cannot raise the appropriate exceptions in create_worker.move()
def test_move(create_worker: Worker, create_tmp_src: str, create_tmp_dest: str) -> None:

    regular_folder_src = os.path.join(create_tmp_src, MOCK_FOLDER_NAME)
    #permission_folder_src = os.path.join(create_tmp_src, MOCK_FOLDER_NAME1)
    #sub_permission_folder_src = os.path.join(permission_folder_src, MOCK_FOLDER_NAME3)
    nonexistant_folder_src = os.path.join(create_tmp_src, MOCK_FOLDER_NAME2)
    regular_folder_dest = os.path.join(create_tmp_dest, MOCK_FOLDER_NAME)
    #permission_folder_dest = os.path.join(create_tmp_dest, MOCK_FOLDER_NAME1)
    nonexistant_folder_dest = os.path.join(create_tmp_dest, MOCK_FOLDER_NAME2)

    # Test regular move
    create_worker.move(regular_folder_src, regular_folder_dest)

    assert os.path.exists(regular_folder_dest) is True

    # Test move with a sub folder giving permission error
    #create_worker.move(permission_folder_src, permission_folder_dest)

    #assert os.path.exists(permission_folder_src) is True
    #assert os.path.exists(permission_folder_dest) is False
    #assert os.path.exists(sub_permission_folder_src) is True
    #assert os.path.exists(os.path.join(create_tmp_dest, MOCK_FOLDER_NAME3)) is False

    # Test non existant folder
    create_worker.move(nonexistant_folder_src, nonexistant_folder_dest)
