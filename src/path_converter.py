import os


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (ROOT_PATH)


def convert_to_relative(absolute_path):
    '''
    Converts an absolute path to a relative path.

    Parameters
    ----------
    absolute_path : str
        An abosolute path to be converted.
        
    Returns
    -------
    str
        The relative path version of the received absolute path.
    '''
    relative_path=os.path.relpath(absolute_path, start= ROOT_PATH)
    
    generic_path= relative_path.replace(os.path.sep, "/")

    return generic_path


def convert_to_absolute(relative_path):
    '''
    Converts a relative path to an absolute path.

    Parameters
    ----------
    relative_path : str
        A relative path to be converted.
        
    Returns
    -------
    str
        The absolute path version of the received relative path.
    '''
    system_path =relative_path.replace("/", os.path.sep)
    
    absolute_path = os.path.abspath(os.path.join(ROOT_PATH, system_path))
 
    return absolute_path 



