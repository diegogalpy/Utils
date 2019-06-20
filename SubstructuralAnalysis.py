import operator

__author__ = 'diegogaleano'
__email__  = 'Diego.Galeano.2014@rhul.live.ac.uk'
__date__  = '19-10-2016'

class SubstructuralAnalysis(object):
    """
    Implementation of sub-structural analysis algorithms.
    """

    def __init__(self, directory_file=''):

        self.directory_file = directory_file


    def RankMoleculesSSA(self, molecules):
        '''
           Ranking of the molecules according to the activity. This code is specific to the format of the file.
        :param molecules:
        :return:
        '''
        print('\n Scoring your molecules with SSA...\n')
        weight_substructures = dict()
        score_molecules = dict()
        substructures = set()

        # Create a set of all the substructures.
        for k, v in molecules.iteritems():
            for sub in v['fcfp']:
                substructures.add(sub)

        # Score the fragments
        for sub in substructures:
            weight_substructures[sub] = self.__weightFragment(sub, molecules)

        # Score the molecules.
        for k,v in molecules.iteritems():
            score = 0

            for sub in molecules[k]['fcfp']:
                score += weight_substructures[sub]

            score_molecules[k] = score

        return  score_molecules



    def __weightFragment(self, fragment, molecules):
        '''
           The weight of a fragment i is defined as:
                   Wfragi = acti / (acti+inacti)
           where:
               acti = number of active molecules that contain the ith fragment.
               inacti = number of inactive molecule that contact the ith fragment.
        '''
        act = 0
        inact = 0
        for k, v in molecules.iteritems():
            if molecules[k]['LABEL'] == '1':
                if fragment in molecules[k]['fcfp']:
                    act += 1
            else:
                if fragment in molecules[k]['fcfp']:
                    inact += 1

        weight = act / float(act + inact)

        return weight

