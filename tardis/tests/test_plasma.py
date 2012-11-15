__author__ = 'wkerzend'

#Testing plasma


from ..import atomic, plasma
from numpy import testing
import pytest
import numpy as np
from astropy import units, table
import os

atom_model = atomic.AtomData.from_hdf5()

fe_mass = atom_model._atom[25]['mass']


def read_nist_data(fname):
    #raise Exception(os.getcwd())
    data = np.genfromtxt(fname, skip_header=3, delimiter='|', usecols=(2, 3),
        converters={3: lambda s: float(s.strip().strip('?[]'))}, names=('j', 'energy'))
    table.Table(data)

tests_data_dir = os.path.join('tardis', 'tests', 'data')
nist_si1 = read_nist_data(os.path.join(tests_data_dir, 'nist_si1.dat'))
#nist_si2 = read_nist_data('tardis/tests/data/nist_si2.dat')
#nist_si3 = read_nist_data('tardis/tests/data/nist_si3.dat')


@pytest.mark.parametrize(("abundances", "abundance_fraction_fe"), [
    (dict(Fe=0.5, Ni=0.5), 0.5),
    (dict(Fe=1., Ni=0.5), 1. / 1.5)
])
def test_abundance_table(abundances, abundance_fraction_fe):
    temperature = 10000
    density = 1
    plasma_model = plasma.Plasma(abundances, temperature, density, atom_model)
    fe_filter = plasma_model.abundances['atomic_number'] == 26
    testing.assert_almost_equal(plasma_model.abundances[fe_filter]['abundance_fraction'], abundance_fraction_fe,
        decimal=10)


@pytest.mark.parametrize(("abundances", "density", "number_abundances_fe"), [
    (dict(Fe=0.5, Ni=0.5), 1, 0.5 / fe_mass ),
    (dict(Fe=0.5, Ni=1), 1e-13, (0.5 / 1.5) * 1e-13 / fe_mass)
])
def test_number_abundances(abundances, density, number_abundances_fe):
    temperature = 10000
    plasma_model = plasma.Plasma(abundances, temperature, density, atom_model)
    fe_filter = plasma_model.abundances['atomic_number'] == 26
    fe_test = (plasma_model.abundances[fe_filter]['number_density'][0] - number_abundances_fe)
    fe_test /= (plasma_model.abundances[fe_filter]['number_density'][0] + number_abundances_fe)
    assert abs(fe_test) < 1e-7




