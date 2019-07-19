#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.nmr
~~~~~~~~~~~

This module provides descriptions of coupling combinations that
could be observed within NMR experiments.
"""

import itertools

import more_itertools

from . import utils


class ResonanceAtom(object):
    """Resonance atom - part of the coupling path."""

    def __init__(self, atom, isotope):
        """Resonance atom initializer.

        :param atom: Atom.
        :type atom: :class:`ctfile.Atom.`
        :param str isotope: Absolute mass of the atom.
        """
        self.atom = atom
        self.isotope = isotope
        self.atom_number = atom.atom_number
        self.atom_symbol = atom.atom_symbol

    def __str__(self):
        """String representation of resonance atom.
        
        :return: String representation of resonance atom.
        :rtype: :py:class:`str`
        """
        return '{}{}{}'.format(self.isotope, self.atom_symbol, self.atom_number)

    def __repr__(self):
        """String representation of resonance atom.

        :return: String representation of resonance atom.
        :rtype: :py:class:`str`
        """
        return str(self)


class Coupling(object):
    """Coupling provides information on the connectivity of molecules."""

    def __init__(self, coupling_path=None, nmr_active_atoms=None, subset_atoms=None):
        """Coupling initializer.
        
        :param list coupling_path: List of atoms that are responsible for observed coupling type.
        :param dict nmr_active_atoms: Atom-isotope pairs that describe labeling.
        :param dict subset_atoms: Atom-isotope pairs used for subset generation.
        """
        if coupling_path:
            self.coupling_path = [sorted(atom_group, key=lambda atom: int(atom.atom_number))
                                  for atom_group in coupling_path]
        else:
            self.coupling_path = coupling_path

        self.nmr_active_atoms = nmr_active_atoms
        self.subset_atoms = subset_atoms

    @property
    def coupling_type(self):
        """Coupling type.
        
        :return: Coupling type.
        :rtype: :py:class:`str`
        """
        return self.__class__.__qualname__

    @property
    def subset(self):
        """Generate coupling path subsets.
        
        :return: Coupling path subsets.
        :rtype: :py:class:`list`
        """
        subset_coupling_path = []

        for atoms_group in self.coupling_path:
            new_atoms_group = []
            for rsize in range(1, len(atoms_group)+1):
                subset = [self._atom_substitution(original_atoms=atoms_group, new_atoms=list(combination))
                          for combination in itertools.combinations(atoms_group, rsize)]
                new_atoms_group.extend(subset)
            subset_coupling_path.append(new_atoms_group)

        subset_couplings = [self.__class__(coupling_path=list(coupling_path),
                                           nmr_active_atoms=self.nmr_active_atoms,
                                           subset_atoms=self.subset_atoms)
                            for coupling_path in itertools.product(*subset_coupling_path)]
        return subset_couplings

    def _atom_substitution(self, original_atoms, new_atoms):
        """Helper function to add missing atom(s) to group of atoms during subset generation.
        
        :param list original_atoms: Group of atoms as part of coupling path before subset.
        :param list new_atoms: Group of atoms as part of coupling path after subset.
        :return: Group of atoms as part of coupling path after subset
        :rtype: :py:class:`list`
        """
        if len(new_atoms) == len(original_atoms):
            return original_atoms
        else:
            atoms_difference = set(new_atoms).symmetric_difference(original_atoms)
            for atom in atoms_difference:
                new_atoms.append(ResonanceAtom(atom=atom, isotope=self.subset_atoms.get(atom.atom_symbol, '')))
            return new_atoms

    def is_resonance_compatible(self, resonance):
        """Test if coupling is compatible with resonance.

        :param resonance: Subclass of :class:`~isoenum.nmr.Coupling`.
        :type resonance: :class:`~isoenum.nmr.Coupling`
        :return: True if compatible, False otherwise.
        :rtype: :py:obj:`True` or `False`
        """
        if set(resonance.hydrogen_coupling_path_repr[0]) == set(more_itertools.flatten(self.hydrogen_coupling_path_repr)):
            return True
        else:
            return False

    @classmethod
    def couplings(cls, atom):
        """Generate list of possible couplings for a given atom type.
        
        :param atom: Atom type.
        :type atom: :class:`ctfile.Atom`
        :return: List of couplings.
        :rtype: :py:class:`list`
        """
        return NotImplementedError('Subclass must implement method.')

    @property
    def name(self):
        """Specific coupling name that indicates interacting atoms.

        :return: Specific coupling name.
        :rtype: :py:class:`str`
        """
        return '[{}:{}]{}'.format(
            ','.join(['{}{}{}'.format(atom.isotope, atom.atom_symbol, atom.atom_number) for atom in self.coupling_path[0]]),
            ','.join(['{}{}{}'.format(atom.isotope, atom.atom_symbol, atom.atom_number) for atom in self.coupling_path[-1]]),
            self.coupling_type)

    @property
    def hydrogen_coupling_path(self, atom_symbol='H'):
        """Coupling path that consists of hydrogen atoms.

        :return: Coupling path.
        :rtype: :py:class:`list`
        """
        return list(filter(lambda lst: bool(lst),
                           [[atom for atom in atom_group if atom.atom_symbol == atom_symbol] for atom_group in
                            self.coupling_path]))

    @property
    def hydrogen_coupling_path_repr(self):
        """Hydrogen coupling path representation.

        :return: List of hydrogen groups representing hydrogen coupling path.
        :rtype: :py:class:`list`
        """
        return [['{}{}{}'.format(atom.isotope, atom.atom_symbol, atom.atom_number) for atom in atom_group]
                for atom_group in self.hydrogen_coupling_path]

    def __eq__(self, other):
        """Comparison of couplings based on atom and isotope specific coupling name."""
        return self.name == other.name

    def __ne__(self, other):
        """Comparison of couplings based on atom and isotope specific coupling name."""
        return self.name != other.name

    def __str__(self):
        """String representation of coupling.
        
        :return: String representation of coupling.
        :rtype: :py:class:`str`.
        """
        return '{}(coupling_path={})'.format(self.__class__.__qualname__, self.coupling_path)

    def __repr__(self):
        """String representation of coupling.
        
        :return: String representation of coupling.
        :rtype: :py:class:`str`.
        """
        return str(self)


class J1CH(Coupling):
    """J1CH coupling type: C-H."""

    def __init__(self, coupling_path=None, nmr_active_atoms=None, subset_atoms=None):
        super(J1CH, self).__init__(coupling_path=coupling_path,
                                   nmr_active_atoms=nmr_active_atoms,
                                   subset_atoms=subset_atoms)

    def couplings(self, carbon_atom):
        """Generate list of possible J1CH couplings.

        :param carbon_atom: Carbon atom.
        :type atom: :class:`ctfile.Atom`
        :return: List of couplings.
        :rtype: :py:class:`list`
        """
        couplings = []
        if len(carbon_atom.neighbor_hydrogen_atoms) > 0:
            coupling_path = [
                [ResonanceAtom(atom=atom, isotope=self.nmr_active_atoms.get(atom.atom_symbol, '')) for atom in carbon_atom.neighbor_hydrogen_atoms],
                [ResonanceAtom(atom=carbon_atom, isotope=self.nmr_active_atoms.get(carbon_atom.atom_symbol, ''))]
            ]
            couplings.append(self.__class__(coupling_path=coupling_path,
                                            nmr_active_atoms=self.nmr_active_atoms,
                                            subset_atoms=self.subset_atoms))
        return couplings


class J2HH(Coupling):
    """J2HH coupling type: H-C-H."""

    def __init__(self, coupling_path=None, nmr_active_atoms=None, subset_atoms=None):
        super(J2HH, self).__init__(coupling_path=coupling_path,
                                   nmr_active_atoms=nmr_active_atoms,
                                   subset_atoms=subset_atoms)

    def couplings(self, carbon_atom):
        """Generate list of possible J2HH couplings.

        :param carbon_atom: Carbon atom.
        :type atom: :class:`ctfile.Atom`
        :return: List of couplings.
        :rtype: :py:class:`list`
        """
        couplings = []
        if len(carbon_atom.neighbor_hydrogen_atoms) == 2:
            coupling_path = [
                [ResonanceAtom(atom=carbon_atom.neighbor_hydrogen_atoms[0], isotope=self.nmr_active_atoms.get(carbon_atom.neighbor_hydrogen_atoms[0].atom_symbol, ''))],
                [ResonanceAtom(atom=carbon_atom, isotope=self.nmr_active_atoms.get(carbon_atom.atom_symbol, ''))],
                [ResonanceAtom(atom=carbon_atom.neighbor_hydrogen_atoms[1], isotope=self.nmr_active_atoms.get(carbon_atom.neighbor_hydrogen_atoms[1].atom_symbol, ''))]
            ]
            couplings.append(self.__class__(coupling_path=coupling_path,
                                            nmr_active_atoms=self.nmr_active_atoms,
                                            subset_atoms=self.subset_atoms))
        return couplings


class J3HH(Coupling):
    """J3HH coupling type: H-C-C-H."""

    def __init__(self, coupling_path=None, nmr_active_atoms=None, subset_atoms=None):
        super(J3HH, self).__init__(coupling_path=coupling_path,
                                   nmr_active_atoms=nmr_active_atoms,
                                   subset_atoms=subset_atoms)

    def couplings(self, carbon_atom):
        """Generate list of possible J3HH couplings.

        :param carbon_atom: Carbon atom.
        :type atom: :class:`ctfile.Atom`
        :return: List of couplings.
        :rtype: :py:class:`list`
        """
        couplings = []
        for neighbor_carbon_atom in carbon_atom.neighbor_carbon_atoms:
            if len(neighbor_carbon_atom.neighbor_hydrogen_atoms) > 0:
                coupling_path = [
                    [ResonanceAtom(atom=atom, isotope=self.nmr_active_atoms.get(atom.atom_symbol, '')) for atom in carbon_atom.neighbor_hydrogen_atoms],
                    [ResonanceAtom(atom=carbon_atom, isotope=self.nmr_active_atoms.get(carbon_atom.atom_symbol, ''))],
                    [ResonanceAtom(atom=neighbor_carbon_atom, isotope=self.nmr_active_atoms.get(neighbor_carbon_atom.atom_symbol, ''))],
                    [ResonanceAtom(atom=atom, isotope=self.nmr_active_atoms.get(atom.atom_symbol, '')) for atom in neighbor_carbon_atom.neighbor_hydrogen_atoms]
                ]
                couplings.append(self.__class__(coupling_path=coupling_path,
                                                nmr_active_atoms=self.nmr_active_atoms,
                                                subset_atoms=self.subset_atoms))
        return couplings

    def is_resonance_compatible(self, resonance):
        """Test if ``J3HH`` coupling is compatible with resonance.

        :param resonance: Subclass of :class:`~isoenum.nmr.Coupling`.
        :type resonance: :class:`~isoenum.nmr.Coupling`
        :return: True if compatible, False otherwise.
        :rtype: :py:obj:`True` or `False`
        """
        if set(resonance.hydrogen_coupling_path_repr[0]) == set(self.hydrogen_coupling_path_repr[0]):
            return True
        else:
            return False


class HResonance(Coupling):
    """Hydrogen resonance."""

    def __init__(self, coupling_path=None, nmr_active_atoms=None, subset_atoms=None):
        super(HResonance, self).__init__(coupling_path=coupling_path,
                                         nmr_active_atoms=nmr_active_atoms,
                                         subset_atoms=subset_atoms)

    def couplings(self, carbon_atom):
        """Generate resonance.

        :param carbon_atom: Carbon atom.
        :type atom: :class:`ctfile.Atom`
        :return: List of couplings.
        :rtype: :py:class:`list`
        """
        couplings = []
        if len(carbon_atom.neighbor_hydrogen_atoms) > 0:
            coupling_path = [
                [ResonanceAtom(atom=atom, isotope=self.nmr_active_atoms.get(atom.atom_symbol, '')) for atom in carbon_atom.neighbor_hydrogen_atoms],
                [ResonanceAtom(atom=carbon_atom, isotope=self.nmr_active_atoms.get(carbon_atom.atom_symbol, ''))]
            ]
            couplings.append(self.__class__(coupling_path=coupling_path,
                                            nmr_active_atoms=self.nmr_active_atoms,
                                            subset_atoms=self.subset_atoms))
        return couplings


class NMRExperiment(object):
    """NMR experiment."""

    def __init__(self, name, couplings, decoupled, default_coupling_definitions):
        """NMR experiment initializer.

        :param str name: NMR experiment name (type).
        :param list couplings: List of allowed coupling types.
        :param list decoupled: List of decoupled elements.
        :param list default_coupling_definitions: List of default coupling definitions.
        """
        self.name = name
        self.couplings = couplings
        self.decoupled = decoupled
        self.default_coupling_definitions = default_coupling_definitions

        if not couplings:
            self.coupling_definitions = [coupling for coupling
                                         in self.default_coupling_definitions]
        else:
            self.coupling_definitions = [self.default_coupling_definitions[coupling.upper()] for coupling
                                         in couplings if coupling in self.default_coupling_definitions]

        if decoupled:
            self.coupling_definitions = [coupling for coupling in self.coupling_definitions
                                         if not set(coupling.nmr_active_atoms).intersection([element.upper()
                                                                                             for element in decoupled])]

    def generate_coupling_combinations(self, molfile, subset=False):
        """Generate possible J couplings for a ``Molfile``."""
        raise NotImplementedError('Subclass must implement method.')


class NMR1D1H(NMRExperiment):
    """1D 1H NMR experiment."""

    def __init__(self, name, couplings=None, decoupled=None,
                 default_coupling_definitions=(HResonance(nmr_active_atoms={'H': '1'}, subset_atoms={'H': '2'}),
                                               J1CH(nmr_active_atoms={'C': '13', 'H': '1'}, subset_atoms={'H': '2'}),
                                               J2HH(nmr_active_atoms={'H': '1'}, subset_atoms={'H': '2'}),
                                               J3HH(nmr_active_atoms={'H': '1'}, subset_atoms={'H': '2'}))):
        """NMR experiment initializer.
        
        :param str name: NMR experiment name (type).
        :param list couplings: List of allowed coupling types.
        :param list decoupled: List of decoupled elements.
        """
        super(NMR1D1H, self).__init__(name=name, couplings=couplings, decoupled=decoupled,
                                      default_coupling_definitions=default_coupling_definitions)

        self.possible_coupling_type_combinations = [combination for combination in utils.all_combinations(self.coupling_definitions)
                                                    if any(isinstance(coupling, HResonance)
                                                    for coupling in combination)]

    def generate_coupling_combinations(self, molfile, subset=False):
        """Generate 1D 1H NMR experiment J couplings for a ``Molfile``.
        
        :param molfile: ``Molfile`` object.
        :type molfile: :class:`ctfile.Molfile`
        :param subset: Generate couplings subsets?
        :type subset: :py:obj:`True` or :py:obj:`False`
        :return: List of possible couplings for a given ``Molfile``.
        :rtype: :py:class:`list`
        """
        valid_coupling_combinations = []
        valid_subset_coupling_combinations = []

        for carbon_atom in molfile.carbon_atoms:
            if len(carbon_atom.neighbor_hydrogen_atoms) > 0:
                for coupling_type_combination in self.possible_coupling_type_combinations:
                    coupling_combination_lists = []
                    for coupling_type in coupling_type_combination:
                        couplings = coupling_type.couplings(carbon_atom)

                        if couplings:
                            coupling_combination_lists.append(utils.all_combinations(couplings))

                        for product in itertools.product(*coupling_combination_lists):
                            coupling_combination = list(more_itertools.flatten(product))

                            if coupling_combination not in valid_coupling_combinations:
                                valid_coupling_combinations.append(coupling_combination)

        if subset:
            for coupling_combination in valid_coupling_combinations:
                subsets = [coupling.subset for coupling in coupling_combination]

                for product in itertools.product(*subsets):
                    subset_product = list(product)
                    subset_product = [coupling for coupling in subset_product
                                      if coupling.is_resonance_compatible(subset_product[0])]

                    if subset_product not in valid_subset_coupling_combinations:
                        valid_subset_coupling_combinations.append(subset_product)

            valid_coupling_combinations = valid_subset_coupling_combinations
        return valid_coupling_combinations


class NMR1DCHSQC(NMR1D1H):
    """1D 13C HSQC NMR experiment."""

    def __init__(
        self,
        name,
        couplings=None,
        decoupled=None,
        default_coupling_definitions=(
            HResonance(nmr_active_atoms={'C': '13', 'H': '1'}, subset_atoms={'H': '2'}),
            J1CH(nmr_active_atoms={'C': '13', 'H': '1'}, subset_atoms={'H': '2'}),
            J2HH(nmr_active_atoms={'C': '13', 'H': '1'}, subset_atoms={'H': '2'}),
            J3HH(nmr_active_atoms={'H': '1'}, subset_atoms={'H': '2'}))):
        """

        :param name:
        :param couplings:
        :param decoupled:
        :param default_coupling_definitions:
        """
        super(NMR1DCHSQC, self).__init__(name=name, couplings=couplings, decoupled=decoupled,
                                         default_coupling_definitions=default_coupling_definitions)


def create_nmr_experiment(name, couplings=None, decoupled=None):
    """Create NMR experiment upon provided experiment type.
    
    :param str name: NMR experiment type.
    :param list couplings: List of coupling types.
    :param list decoupled: List of elements.
    :return: NMR experiment.
    :rtype: :class:`~isoenum.nmr.NMRExperiment`.
    """
    nmr_experiment_types = {
        '1D1H': NMR1D1H,
        '1DCHSQC': NMR1DCHSQC
    }

    try:
        return nmr_experiment_types[name.upper()](name=name, couplings=couplings, decoupled=decoupled)
    except KeyError:
        raise ValueError('Unknown nmr experiment type: "{}"'.format(name))
