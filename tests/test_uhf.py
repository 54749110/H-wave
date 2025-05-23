#!/usr/bin/env python3

import os
import unittest

import numpy as np
import tomli
from requests.structures import CaseInsensitiveDict

import hwave.qlms

tolerance = 1.0e-8

def readfile(filename):
    tbl = CaseInsensitiveDict()
    try:
        with open(filename, "r") as fh:
            lines = fh.read().splitlines()
    except Exception as e:
        print("ERROR:", e)
        return tbl
    for line in lines:
        k,v = line.split('=')
        tbl[k.strip()] = float(v)
    return tbl

def runtest(test, type):
    cur=os.getcwd()
    os.chdir(type)
    with open("input.toml", "rb") as f:
        params = tomli.load(f)

    hwave.qlms.run(input_dict=params)

    result = readfile("output/energy.dat")
    expect = readfile("output_ref/energy.dat")

    os.chdir(cur)

    test.assertTrue(np.isclose(result['energy_total'], expect['energy_total'], rtol=0.0, atol=tolerance))


class TestUHFr(unittest.TestCase):
    def test_CoulombIntra(self):
        return runtest(self, "tests/uhfr/coulombintra")

    def test_CoulombInter(self):
        return runtest(self, "tests/uhfr/coulombinter")

    def test_Exchange(self):
        return runtest(self, "tests/uhfr/exchange")

    def test_Hund(self):
        return runtest(self, "tests/uhfr/hund")

    def test_Ising(self):
        return runtest(self, "tests/uhfr/ising")

    def test_PairLift(self):
        return runtest(self, "tests/uhfr/pairlift")

    def test_PairHop(self):
        return runtest(self, "tests/uhfr/pairhop")

    def test_2sz0(self):
        return runtest(self, "tests/uhfr/2sz0")

    def test_2sz1(self):
        return runtest(self, "tests/uhfr/2sz1")


class TestUHFk(unittest.TestCase):
    def test_CoulombIntra(self):
        return runtest(self, "tests/uhfk/CoulombIntra")

    def test_CoulombInter(self):
        return runtest(self, "tests/uhfk/CoulombInter")

    def test_Exchange(self):
        return runtest(self, "tests/uhfk/Exchange")

    # def test_Hund(self):
    #     return runtest(self, "tests/uhfk/Hund")

    def test_Ising(self):
        return runtest(self, "tests/uhfk/Ising")

    def test_PairLift(self):
        return runtest(self, "tests/uhfk/PairLift")

    def test_PairHop(self):
        return runtest(self, "tests/uhfk/PairHop")

    def test_2sz0(self):
        return runtest(self, "tests/uhfk/2sz0")

    def test_2sz1(self):
        return runtest(self, "tests/uhfk/2sz1")

    

if __name__ == "__main__":
    unittest.main()
