#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest


@pytest.mark.parametrize('path, parameters', [
    ('tests/example_data/bmse000040.mol', '-a 13:C'),
    ('tests/example_data/bmse000040.mol', '-e 13:C'),
    ('tests/example_data/bmse000040.mol', '-s 13:C:2'),
    ('tests/example_data/bmse000040.sdf', '-a 13:C'),
    ('tests/example_data/bmse000040.sdf', '-e 13:C'),
    ('tests/example_data/bmse000040.sdf', '-s 13:C:2'),
    ('tests/example_data/bmse000040.inchi', '-a 13:C'),
    ('tests/example_data/bmse000040.inchi', '-e 13:C'),
    ('tests/example_data/bmse000040.inchi', '-s 13:C:2'),
    ('tests/example_data/bmse000040.mol', '-a 13:C -s 13:C:2 -e 15:N'),
    ('tests/example_data/bmse000040.sdf', '-a 13:C -s 13:C:2 -e 15:N'),
    ('tests/example_data/bmse000040.inchi', '-a 13:C -s 13:C:2 -e 15:N'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.mol', '-a 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.mol', '-e 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.mol', '-s 13:C:2'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.sdf', '-a 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.sdf', '-e 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.sdf', '-s 13:C:2'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.inchi', '-a 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.inchi', '-e 13:C'),
    ('https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/bmse000040.inchi', '-s 13:C:2')
])
def test_name_command(path, parameters):
    command = "python -m isoenum name {} {}".format(path, parameters)
    assert os.system(command) == 0
