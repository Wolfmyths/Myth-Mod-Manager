import pytest

from src.helpers.profile_manager import ProfileManager

@pytest.fixture(scope='module')
def create_profileManager(createTemp_Profiles_ini: str) -> ProfileManager:
    return ProfileManager(createTemp_Profiles_ini)

def test_getMods(create_profileManager: ProfileManager) -> None:
    assert create_profileManager.getMods('Awesome mods') == ['cool_beans', 'among us guards', 'make game easy']

def test_getJSON(create_profileManager: ProfileManager) -> None:
    assert create_profileManager.getJSON() == {'Awesome mods' : ['cool_beans', 'among us guards', 'make game easy']}

def test_addProfile(create_profileManager: ProfileManager) -> None:

    create_profileManager.addProfile('profile1')

    assert 'profile1' in list(create_profileManager.getJSON().keys())

def test_addMod(create_profileManager: ProfileManager) -> None:

    create_profileManager.addMod('profile1', 'pizza_gloves')

    assert create_profileManager.getMods('profile1') == ['pizza_gloves']

def test_changeProfile(create_profileManager: ProfileManager) -> None:

    create_profileManager.changeProfile('profile1', 'profile2')

    list_of_profiles = list(create_profileManager.getJSON().keys())

    assert 'profile1' not in list_of_profiles
    assert 'profile2' in list_of_profiles
    assert create_profileManager.getMods('profile2') == ['pizza_gloves']

def test_removeMod(create_profileManager: ProfileManager) -> None:

    create_profileManager.removeMod('profile2', 'pizza_gloves')

    assert not create_profileManager.getMods('profile2')

def test_removeProfile(create_profileManager: ProfileManager) -> None:

    create_profileManager.removeProfile('profile2')

    assert 'profile2' not in list(create_profileManager.getJSON().keys())
