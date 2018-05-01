#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest


@pytest.mark.parametrize('path, parameters', [
    ('-a C-13', 'tests/example_data/bmse000040.mol'),
    ('-e C-13', 'tests/example_data/bmse000040.mol'),
    ('-s C-13-2', 'tests/example_data/bmse000040.mol'),
    ('-a C-13', 'tests/example_data/bmse000040.sdf'),
    ('-e C-13', 'tests/example_data/bmse000040.sdf'),
    ('-a C-13', 'tests/example_data/bmse000040.inchi'),
    ('-e C-13', 'tests/example_data/bmse000040.inchi')
])
def test_name_command(path, parameters):
    command = "python -m isoenum name {} {}".format(path, parameters)
    assert os.system(command) == 0
