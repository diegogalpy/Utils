import operator
import numpy as np
import requests
import pandas as pd
from collections import defaultdict

import Parsers as parsers
__author__ = 'diegogaleano'
__email__  = 'Diego.Galeano.2014@rhul.live.ac.uk'
__date__  = '19-10-2016'

class DrugBankExtractor(object):
    """
    Container for Drug Bank Extraction
    """
    start = '<span class="glyphicon glyphicon-info-sign"> </span></a></th><td><ul><li>'
    end = '<th>Pharmacodynamics'
    base_url = 'https://www.drugbank.ca/drugs/'

    def __init__(self):
        pass

    def extract_structured_indications(self, drug_id):
        html = requests.get(self.base_url+drug_id).text
        start_pt = html.find(self.start)
        end_pt = html.find(self.end)
        subset = html[start_pt:end_pt].split('</a>')
        structured_indications = []
        for val in subset:
            if "/indications" in val:
                structured_indication = val.split('">')[1]
                structured_indications.append(structured_indication)
        return drug_id, structured_indications
		
class ParserIndications(object):
	"""
	   Parser indications
	"""

	def __init__(self):

		# Get the default directories
		self.easyparser = parsers.EasyParsers()
		self.data_directory = self.easyparser.get_data_directory()
		self.result_directory = self.easyparser.get_results_directory()
		self.image_directory = self.easyparser.get_images_directory()
		
	def getKeggIndications(self, mykeggdict):
		'''
			get the kegg indications
		'''
		kegg_activity = defaultdict(set)
		for drugID, fiels in mykeggdict.iteritems():
			if 'ACTIVITY' in fiels:
				for acts in fiels['ACTIVITY']:
					for act in acts.split(','):
						kegg_activity[drugID].add(act.lower().strip())

		return kegg_activity
		
	def getKeggPathways(self, mykeggdict):
		'''
			get the kegg pathways
		'''
		kegg_pathways = defaultdict(set)
		for drugID, fiels in mykeggdict.iteritems():
			if 'PATHWAY' in fiels:
				for pathway in fiels['PATHWAY']:
					pathway = pathway.split(')')
					kegg_pathways[drugID].add(pathway[-1].strip())
					
		return kegg_pathways
		
	def getGottliebIndications(self):
		'''
			PREDICT: a method for inferring novel drug indications with application to personalized medicine
			Assaf Gottlieb, Gideon Y Stein, Eytan Ruppin, Roded Sharan
		'''
		
		
		rawdata = self.easyparser.parse_csv(self.data_directory + 'drugIndicationGoldStandard.csv', '"')
		drugInd = defaultdict(set)
		for line in rawdata:
			drugName = line[0].lower().strip()
			#indication = line[1].strip().lower().split(',')
			#firstindi  = indication[0].split(';')
			#drugInd[drugName].add(firstindi[0])
			drugInd[drugName].add(line[1])
			
		return drugInd
		
		
	def getBarabasiIndications(self):
		'''
			Network-based in silico drug efficacy screening 
			Emre Guney, Barabasu
		'''
		rawdata = self.easyparser.parse_csv_header(self.data_directory + 'drugDiseaseBarabasi.csv', 2)
		return rawdata
		
	def getBarabasiSymptoms(self):
		'''
			Network-based in silico drug efficacy screening 
			Emre Guney, Barabasu
		'''
		rawdata = self.easyparser.parse_tsv(self.data_directory + 'diseaseSymptomsBarabasi.txt')
		
		my_symptoms = defaultdict(list)
		
		for idx,row in enumerate(rawdata):
			# ignore headings
			if idx > 0:
				disease = row[1].lower().strip()
				symptom = row[0].lower().strip()
				
				my_symptoms[disease].append(symptom)
				
		
				
		
		return my_symptoms