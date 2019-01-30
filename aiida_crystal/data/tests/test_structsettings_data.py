"""A module testing data structure with symmetry operations"""
import pytest

# pylint: disable=unused-argument


def test_fail(new_database):
    """A failing test"""
    from aiida.common.exceptions import ValidationError
    from aiida_crystal.data.struct_settings import StructSettingsData

    with pytest.raises(ValidationError):
        StructSettingsData(data={})

    node = StructSettingsData()
    with pytest.raises(ValidationError):
        node.store()


def test_pass(new_database):
    """A passing test"""
    from aiida_crystal.data.struct_settings import StructSettingsData
    data = {
        "space_group": 1,
        "crystal_type": 1,
        "centring_code": 1,
        "operations": [[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]
    }

    node = StructSettingsData(data=data)

    assert node.data == data

    data["space_group"] = 2
    node.set_data(data)

    node.store()

    data["space_group"] = 3
    from aiida.common.exceptions import ModificationNotAllowed
    with pytest.raises(ModificationNotAllowed):
        node.set_data(data)

    assert node.data["space_group"] == 2
