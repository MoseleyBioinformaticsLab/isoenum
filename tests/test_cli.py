#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import pytest


def setup_module(module):
    if not os.path.exists("tests/example_data/tmp/"):
        os.mkdir("tests/example_data/tmp")


@pytest.mark.parametrize(
    "path, parameters, expected_output",
    [
        (
            "tests/example_data/valine.mol",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "tests/example_data/valine.mol",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "tests/example_data/valine.mol",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
        (
            "tests/example_data/valine.sdf",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "tests/example_data/valine.sdf",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "tests/example_data/valine.sdf",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
        (
            "tests/example_data/valine.inchi",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "tests/example_data/valine.inchi",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "tests/example_data/valine.inchi",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
        (
            "tests/example_data/valine.mol",
            "-a 13:C -s 13:C:2 -e 15:N",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1,6+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
            },
        ),
        (
            "tests/example_data/valine.sdf",
            "-a 13:C -s 13:C:2 -e 15:N",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1,6+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
            },
        ),
        (
            "tests/example_data/valine.inchi",
            "-a 13:C -s 13:C:2 -e 15:N",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1,6+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.mol",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.mol",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.mol",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.sdf",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.sdf",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.sdf",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.inchi",
            "-a 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1"
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.inchi",
            "-e 13:C",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,5+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,3+1,4+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i3+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,4+1,5+1",
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1,2+1,3+1,4+1",
            },
        ),
        (
            "https://raw.githubusercontent.com/MoseleyBioinformaticsLab/isoenum/master/tests/example_data/valine.inchi",
            "-s 13:C:2",
            {
                b"InChI=1S/C5H11NO2/c1-3(2)4(6)5(7)8/h3-4H,6H2,1-2H3,(H,7,8)/t4-/m0/s1/i1+1/t3?,4-"
            },
        ),
    ],
)
def test_name_command(path, parameters, expected_output):
    command = "python -m isoenum name {} {}".format(path, parameters)
    output = subprocess.check_output(command.split())
    assert set(output.split()) == expected_output


def teardown_module(module):
    if os.path.exists("tests/example_data/tmp/"):
        shutil.rmtree("tests/example_data/tmp")
