import json


def read_json(json_path):
    '''
    tries to open the json file and returns its information  

    Parameters
    ----------
    json_path : String
        json path
        
    Returns
    -------
    List
        
    '''
    json_data = []
    with open(json_path, encoding= "utf-8", mode= "r") as file:
        json_data = json.load(file)
    
    return json_data


def write_json(json_path, data):
    '''
    tries to write the received dictionary to the json file 
    Parameters
    ----------
    json_path : String
        json path
    data: Dictionary
        information to save in the json
        
    Returns
    -------
    List
        
    '''

    with open(json_path, encoding= "utf-8", mode= "w") as file:
        json.dump(data, file, indent= 4)