import operator
import numpy as np
from bioservices.kegg import KEGG
from collections import defaultdict

import Parsers as parsers
__author__ = 'diegogaleano'
__email__  = 'Diego.Galeano.2014@rhul.live.ac.uk'
__date__  = '19-10-2016'

class KeggParser(object):
	"""
	Kegg Parser
	"""

	def __init__(self, directory_file=''):

		self.directory_file = directory_file
	
	def getData(self):
		'''
		  Gets all the data for the drugs
		  Obs. IT TAKES TIME.
		'''
		mykegg = KEGG()
		
		print 'There are',len(mykegg.drugIds), 'drugs in Kegg'
		data = dict()
		# Get data from Kegg database.
		for num,ID in enumerate(k.drugIds):
			data[ID] = k.get(ID)

		print 'Finish!'
		
		return data
		
	def loadRawData(self):
		'''
			We load the raw data we got from kegg
		'''
		parser = parsers.EasyParsers()		
		result_directory = parser.get_results_directory()
		
		data =  parser.read_pickle(result_directory, 'RawKeggDrugs.pkl')
		return data
		
	def ParserRawData(self, KeggDrugs):
		'''
			We parser the raw data
		'''
		drugsKegg = dict()
		old_id = ""
		for ID, v in KeggDrugs.iteritems():
			drugsKegg[ID] = defaultdict(list)
			for l in v.split('\n'):
				if l=='' or l[:3]=='///':
					continue
       
				line = l.split()
				cur_id = line[0]        
				
				
				if l[:3] == "   ":
					cur_id = old_id
					value = " ".join(line[0:]).strip()
				else:
					old_id = cur_id
					value = " ".join(line[1:]).strip()
    
       
        
				drugsKegg[ID][cur_id].append(value)  
		return drugsKegg
		
	