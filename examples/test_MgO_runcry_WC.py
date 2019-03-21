#!/usr/bin/env python

""" This is a test of base workchain submission for CRYSTAL properties calculation
"""

#  Copyright (c)  Andrey Sobolev, 2019. Distributed under MIT license, see LICENSE file.

import os
import json
from mpds_client.retrieve_MPDS import MPDSDataRetrieval

from aiida.orm import DataFactory, Code
from aiida.work import submit
from aiida_crystal.workflows.runcry import RunCryWorkChain
from aiida_crystal.tests import TEST_DIR

inputs = RunCryWorkChain.get_builder()
inputs.crystal_code = Code.get_from_string('crystal@torquessh')
inputs.properties_code = Code.get_from_string('properties@torquessh')

inputs.crystal_parameters = DataFactory('parameter')(dict={
    "title": "MgO",
    "scf": {
        "k_points": (8, 8),
    }
})
inputs.properties_parameters = DataFactory('parameter')(dict={
    "band": {
        "shrink": 12,
        "k_points": 30,
        "first": 7,
        "last": 14,
#        "bands": [["G", "W"]]
    },
})
inputs.basis_family = DataFactory('str')('sto-3g')
with open(os.path.join(TEST_DIR, "input_files", "MgO.json")) as f:
    data = json.load(f)

datarow = [
    data["cell_abc"],
    data["sg_n"],
    data.get("setting", None),
    data["basis_noneq"],
    data["els_noneq"]
]

atoms = MPDSDataRetrieval.compile_crystal(datarow, flavor='ase')
inputs.structure = DataFactory('structure')(ase=atoms)

inputs.options = DataFactory('parameter')(dict={
    'resources': {
        'num_machines': 1,
        'num_mpiprocs_per_machine': 1
    }
})

calc = submit(RunCryWorkChain, **inputs)
print("submitted WorkChain; calc=WorkCalculation(PK={})".format(
    calc.dbnode.pk))
