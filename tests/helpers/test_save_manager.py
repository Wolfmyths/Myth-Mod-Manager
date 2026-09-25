import pytest

from src.constant_vars import ModKeys, ModType

from src.helpers.save_manager import Save

EXPECTED_MODS = ('super fun mod', 'best mod ever', 'make game easy mod')

@pytest.mark.parametrize('modName', EXPECTED_MODS)
def test_testSave(createTemp_Mod_ini: str, modName: str) -> None:
    save = Save(createTemp_Mod_ini)

    assert save.hasMod(modName)
    assert save.hasModOption(modName, ModKeys.type.value)
    assert save.hasModOption(modName, ModKeys.modworkshopid.value) is not False

def test_saveMethods(createTemp_Mod_ini: str) -> None:

    save = Save(createTemp_Mod_ini)

    modName = 'super fun mod'
    
    # Testing setters and getters (get/setType() is tested through the use of addMods())
    save.setEnabled(modName, False)
    assert save.hasModOption(modName, ModKeys.enabled.value)
    assert not save.getEnabled(modName)

    save.setIgnored(modName, True)
    assert save.hasModOption(modName, ModKeys.ignored.value)
    assert save.getIgnored(modName)

    save.setModWorkshopAssetID(modName, '12345')
    assert save.hasModOption(modName, ModKeys.modworkshopid.value)
    assert save.getModworkshopAssetID(modName) == '12345'

    # Testing Sequence argument for addMods
    modsList: list[str] = ['I hate my teammates mod', 'cats mod']

    save.addMods((modsList, ModType.mods_override))

    for mod in modsList:
        assert save.hasMod(mod)
        assert save.hasModOption(mod, ModKeys.type.value)
        assert save.getType(mod) == ModType.mods_override

    save.removeMods(*modsList)
    
    for mod in modsList:
        assert not save.hasMod(mod)
    
    save.clearModData()

    assert len(save.mods()) == 0
