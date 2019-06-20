import csv

__author__ = 'diegogaleano'
__email__  = 'Diego.Galeano.2014@rhul.live.ac.uk'
__date__  = '19-10-2016'
import string
import Parsers as parsers
from collections import defaultdict
class COSTARTOntology(object):
	"""
		COSTART (Coding Symbols for a Thesaurus of Adverse Reaction Terms) Ontology to map side-effects 
		
	"""
	
	def __init__(self, directory_file=''):

		self.directory_file = directory_file
		self.path = defaultdict(list)
		# This mapping was taken from Gobbliet et at. PREDICT: check supplementary materials.
		self.ATC_Costart = {
			'A': ['digestive system', 'gastrointestinal disorders', 'metabolic disorders', 'metabolic and nutritional disorders'],
			'B': ['hematologic disorders', 'hemic and lymphatic system'],
			'C': ['cardiovascular disorders','cardiovascular system'],
			'D': ['skin and appendages', 'skin disorders'],
			'G': ['urogenital system', 'genitourinary disorders', 'gynecologic disorders','renal disorders'],
			'H': ['endocrine disorders', 'endocrine system'],
			'J': [ ],
			'L': [ ],
			'M': ['musculo-skeletal system'],
			'N': ['nervous system', 'nervous disorders', 'autonomic nervous disorders'],
			'P': [ ],
			'R': ['pulmonary disorders','respiratory system'],
			'S': ['ophthalmic disorders','special senses']    
		}

		self.ATC_code = {
			'A':    'ALIMENTARY TRACT AND METABOLISM',
			'B':    'BLOOD AND BLOOD FORMING ORGANS',
			'C':    'CARDIOVASCULAR SYSTEM',
			'D':    'DERMATOLOGICALS',
			'G':    'GENITO URINARY SYSTEM AND SEX HORMONES',
			'H':    'SYSTEMIC HORMONAL PREPARATIONS, EXCL. SEX HORMONES AND INSULINS',
			'J':    'ANTIINFECTIVES FOR SYSTEMIC USE',
			'L':    'ANTINEOPLASTIC AND IMMUNOMODULATING AGENTS',
			'M':    'MUSCULO-SKELETAL SYSTEM',
			'N':    'NERVOUS SYSTEM',
			'P':    'ANTIPARASITIC PRODUCTS, INSECTICIDES AND REPELLENTS',
			'R':    'RESPIRATORY SYSTEM',
			'S':    'SENSORY ORGANS',
			'V':    'VARIOUS'
			
		}

		
	def getData(self):
	
		parser = parsers.EasyParsers()		
		data_directory = parser.get_data_directory()
		
		with open(data_directory + 'COSTART.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			
			costartGraph = dict()
			for row in spamreader:       
				costartGraph[row[0]] = dict()
				costartGraph[row[0]]["Preferred Label"] = row[1]
				costartGraph[row[0]]["Synonyms"]        = row[2].split("|")
				costartGraph[row[0]]["Definitions"]     = row[3]
				costartGraph[row[0]]["Obsolete"]        = row[4]
				costartGraph[row[0]]["CUI"]             = row[5].split("|")
				costartGraph[row[0]]["Semantic Types"]  = row[6].split("|")
				costartGraph[row[0]]["Parents"]         = row[7].split("|")       
				costartGraph[row[0]]["Semantic type UMLS property"] = row[8].split("|")
			
		return costartGraph
		
	def amount_of_se_in_costart(self,costartGraph, unique_side_effects):    
		se_in_costart = defaultdict(list)   
		
		for k,v in costartGraph.iteritems():       
			for val in v["Synonyms"]:
				se_in_costart[v["Preferred Label"].lower()].append(val.lower())
		
		#print se_in_costart
		print "Number of unique se PT in COSTART", len(se_in_costart)    
		print "Number of input side effects", len(unique_side_effects)
		
		cont  = 0
		PT_se_found = set()
		se_not_costart = list()    
		for v in unique_side_effects:
			if v.lower() in se_in_costart.keys():
				cont = cont + 1
				PT_se_found.add(v.lower())
			else: #look on the synonyms
				for k,synSE in se_in_costart.iteritems():
					if v.lower() in synSE:
						cont = cont + 1
						PT_se_found.add(v.lower())
						break
						
		print "Number of input side effects in COSTART as PT or as Syn", cont
		
		return PT_se_found
		
	def find_parents(self,costartGraph, set_side_effects):
		se_parents = defaultdict(set)
		rootID = 'http://www.w3.org/2002/07/owl#Thing' 
		cont = 1
	
		for se in set_side_effects:        
			for k, node in costartGraph.iteritems():      
				if k == rootID:
					continue
				#print k,node
				if se in node["Preferred Label"].lower() or se in [v.lower() for v in node["Synonyms"]]:
					self.__recursive_search(costartGraph, se, rootID, k,node["Parents"],se_parents, 0)
		
		return se_parents, self.path
	
	def path_root(self, allpath, cat_set_costart):
		mydict = defaultdict()
		
		for se, tupla in allpath.iteritems():
			if se not in mydict:
				mydict[se] = defaultdict(set)
				
			for root in cat_set_costart[se]:
				for row in tupla:
					if root == row[2].lower():
						mydict[se][root].add(row[1])
				
		return mydict
				
	def codify_terms(self,  path_root):
		
		
		terms_L0 = list(set([r for se, roots in path_root.iteritems() for r in roots]))
		code_L0 = {v:'T'+ str(idx).zfill(2) for idx,v in enumerate(terms_L0)}
		terms_tupla = set([(r,t) for se, roots in path_root.iteritems() for r,childs in roots.iteritems() for t in childs])
		terms_L1 = list(set([t for se, roots in path_root.iteritems() for r,childs in roots.iteritems() for t in childs]))
		abc = list(string.ascii_uppercase)
			
		code_L1 = defaultdict(list)
		L1 = defaultdict(set)
		
		for root, child in terms_tupla:
			L1[root].add(child.lower())
			
		for root, childs in L1.iteritems():
			for idx,c in enumerate(childs):				
				code_L1[c].append(code_L0[root] + abc[idx])
	
		return code_L0, code_L1, L1
	
	def enumerate_terms(self, code_L0, code_L1):
	
		terms0 = [k + ' (' + v + ')' for k, v in code_L0.iteritems()]
		
		mydict0 = {v:idx for idx,v in enumerate(code_L0)}
		
		terms1 = [c for k,cds in code_L1.iteritems() for c in cds]
		terms1. sort()
		
		mydict1 = {v:idx for idx,v in enumerate(terms1)}
		
		return terms0, mydict0, terms1, mydict1
		
	def __recursive_search(self,costartGraph, se, rootID, child, ParentID, se_parents, nivel):    
		for pID in ParentID: 
			if pID not in costartGraph:
				continue
			
			newstr = costartGraph[pID]['Preferred Label']		
						
			
			
			
			#print '++',pID, costartGraph[pID]
			if rootID in costartGraph[pID]["Parents"]:
				se_parents[se].add(costartGraph[pID]["Preferred Label"].lower())
				self.path[se].append((nivel,costartGraph[child]["Preferred Label"], newstr.lower()))
				return
			else:
				self.path[se].append((nivel,child, pID))
				#print costartGraph[pID]["Parents"], pID
				
				self.__recursive_search(costartGraph, se, rootID, pID, costartGraph[pID]["Parents"],se_parents, nivel + 1)  
				
	def MappingtoCOSTARTroot(self, se_parents):
		
		TopCostartToATC = dict()
		SEtoATC = defaultdict(set)
		
		for k,v in self.ATC_Costart.iteritems():
			for val in v:
				TopCostartToATC[val] = k;
		
		
		for k,v in se_parents.iteritems():
			for val in v:
				if val in TopCostartToATC.keys():
					SEtoATC[k].add(TopCostartToATC[val])
			
		return SEtoATC, TopCostartToATC