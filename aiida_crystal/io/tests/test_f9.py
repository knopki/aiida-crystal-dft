#  Copyright (c)  Andrey Sobolev, 2019. Distributed under MIT license, see LICENSE file.
"""
Tests for fort.9 reader
"""
import os
import shutil
import pytest
from aiida_crystal.tests import TEST_DIR
from aiida_crystal.io.f9 import Fort9

file_name = os.path.join(TEST_DIR,
                         "output_files",
                         "mgo_sto3g",
                         "fort.9")


def test_fail():
    with pytest.raises(ValueError):
        Fort9("invalid_file_name.9")


def test_pass():
    parser = Fort9(file_name)
    cell, positions, numbers = parser.get_cell()
    assert cell.shape == (3, 3)
    assert positions.shape == (2, 3)
    assert sorted(numbers.tolist()) == [8, 12]
    assert parser.get_ao_number() == 18
