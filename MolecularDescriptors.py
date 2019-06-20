from __future__ import print_function
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import DataStructs, Chem

__author__ = 'diegogaleano'
__email__  = 'Diego.Galeano.2014@rhul.live.ac.uk'
__date__  = '19-10-2016'

class MolecularDescriptors(object):
    """
        Chemical features
    """
    def __init__(self, my_smiles = ''):
        self.my_smiles = my_smiles
        self.mol = None
        MolecularDescriptors.__parse_molecule(self)

    def __parse_molecule(self):
        '''
        Parse SMILES string into molecule object
        :return:
        '''
        self.mol = Chem.MolFromSmiles(self.my_smiles)

    def calculate_crippen_logp(self):
        '''
        Calcules the Crippen LogP
        :return: ClogP
        '''

        clogp = rdMolDescriptors.CalcCrippenDescriptors(self.mol)
        return clogp[0]

    def generate_fcfp(self, radius=3):
        '''
        Calculates Functional Class fingerprints
        :param radius:
        :return:
        '''
        ffp = AllChem.GetMorganFingerprint(self.mol, radius, useFeatures = True)
        return ffp.GetNonzeroElements()

    def calculate_number_rings(self):
        '''
        Number of rings in the molecule
        :return:
        '''
        return rdMolDescriptors.CalcNumRings(self.mol)

    def calculate_number_aromatic_rings(self):
        '''
        Calculates the number of aromatic rings
        :return:
        '''
        return rdMolDescriptors.CalcNumAromaticRings(self.mol)


class ChemicalSimilarity(object):
    """
        Chemical similarity
    """
    def __init__(self, my_smiles1, my_smiles2):
        self.smiles1 = my_smiles1
        self.smiles2 = my_smiles2
        self.mol = None

    def tanimoto_similarity(self):
        ms = [Chem.MolFromSmiles(self.smiles1), Chem.MolFromSmiles(self.smiles2)]
        fps = [FingerprintMols.FingerprintMol(x) for x in ms]
        return DataStructs.FingerprintSimilarity(fps[0],fps[1])