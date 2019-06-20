# Utils
Useful `python` methods that allow me to start a new project or parse datasets 

## Files 

* `CreateNewProject.py`: creates a directory with folders for a new project. It can be personalised. 
* `Utilities.py`
* `COSTARTOntology.py`: parser the COSTART ontology.
* `DrugBankParser.py`: this is a bit old, not sure if covers all the new fields in newer versions of DrugBank.
* `KeggParser.py`
* `MolecularDescriptors.py`
* `ParserIndications.py`
* `Parsers.py`
* `SIDERParser.py`
* `SubstructuralAnalysis.py`
* `Parsers.py`: class EasyParser to parser and save different data formats, including .*csv and .*mat.

```python
class EasyParsers(object):  
    def get_data_directory(self):
    def set_file_directory(self, filename):
    def get_results_directory(self):
    def get_images_directory(self):
    def parse_csv(self, filename, quote = '|'):
    def parse_tsv(self, filename):
    def parse_csv_header(self, filename, column_id = 0):
    def parse_tsv_header(self, filename, column_id = 0):
    def save_pickle(self, directory,variable_name, variable):
    def save_matlab(self, directory,variable_name, variable):
    def read_pickle(self,directory, variable_name):
    def features_dictionary_to_npmatrix(self, my_dict, list_order, list_features, list_fcfp):
```
