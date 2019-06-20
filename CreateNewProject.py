import os
import errno

__author__ = 'diegogaleano'
__date__ = '20/05/2016'

class Project(object):
    """
    Simple class to create a directories for a new project
    """
    def __init__(self, directory_string):
        self.directory_string = directory_string
        

    def __create_directory(self, folderName):
        """
        Create the specified directory
        """
        try:
            if not os.path.exists(self.directory_string + folderName):
                os.makedirs(self.directory_string + folderName)
        except:
            print('Error creating folders for the project')
    
    def __project_template(self):
        '''
            Create all the folders for the project
        '''
        NewProjectFolders = dict()
        NewProjectFolders['code'] = ['python', 'matlab']
        NewProjectFolders['data'] = ['results', 'databases', 'images']
        NewProjectFolders['papers'] = ['ToLibrary', 'ToRead']
        NewProjectFolders['publications'] = []

        return  NewProjectFolders

    def create_directories(self):
        '''
            Create all the directories for a given template
        '''
        foldersTree = self.__project_template()

        for root, childrens in foldersTree.iteritems():
            self.__create_directory(root)

            for c in childrens:
                self.__create_directory(root + '/' + c)

        print('Done! You can start to work!')

if __name__ == '__main__':
    # Example usage
    path =  ' '
    new_project = Project(url)
    new_project.create_directories()

