import json


def read_json(json_path) -> list:
    '''
    Tries to open a ".json" file and read its information.

    Parameters
    ----------
    json_path : str
        ".json" file path.
        
    Returns
    -------
    list
        The content of a ".json" file.
    '''
    json_data = []
    with open(json_path, encoding= "utf-8", mode= "r") as file:
        json_data = json.load(file)
    
    return json_data


def write_json(json_path, data):
    '''
    Tries to open a ".json" file and write in it.
    
    Parameters
    ----------
    json_path : String
        ".json" file path.
    
    data: dict
        Information to be written in the ".json" file.
    '''

    with open(json_path, encoding= "utf-8", mode= "w") as file:
        json.dump(data, file, indent= 4)