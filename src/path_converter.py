import os


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (ROOT_PATH )


def convert_to_relative(absolute_path):
    '''
    converts an absolute path to a relative path

    Parameters
    ----------
    absolute_path : String
        absolute path
        
    Returns
    -------
    string
        
    '''
    relative_path=os.path.relpath(absolute_path, start=ROOT_PATH)
    
    generic_path= relative_path.replace(os.path.sep, "/")

    return generic_path


def convert_to_absolute(relative_path):
    '''
    converts an relative path to a absolute path

    Parameters
    ----------
    relative_path : String
        relative path
        
    Returns
    -------
    string
        
    '''
    system_path =relative_path.replace("/", os.path.sep)
    
    absolute_path = os.path.abspath(os.path.join(ROOT_PATH, system_path))
 
    return absolute_path 



