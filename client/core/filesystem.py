'''
filesystem

manage the filesystem's operations 
'''
import os
import pathlib

def validate_path(path:str):
    '''
    validate if the path exists in filesystem
    '''
    return os.path.exists(path)

def writefile(filepath:str,content:str,create=True):
    '''
    write the given content inside the given

    raise Exception if any error in the path 
    '''
    if not validate_path(pathlib.Path(filepath).parent):
        raise Exception(f'The given root {filepath} doesn\'t exists')
    if not create and not validate_path(pathlib.Path(filepath)):
        raise Exception(f'The specified {filepath} doesn\'t exists')
    with open(filepath,'w') as writer:
        writer.write(content)
        pass
    pass

def readfile(filepath:str):
    '''
    read the content inside the given filepath

    raise Exception if any error in the path 
    '''
    if not validate_path(pathlib.Path(filepath).parent):
        raise Exception(f'The given root {filepath} doesn\'t exists')
    if not validate_path(filepath):
        raise Exception(f'The specified {filepath} doesn\'t exists')
    if not os.path.isfile(filepath):
        raise Exception(f'The specified {filepath} is not a file')
    reader = open(filepath,'r')
    content = reader.read()
    reader.close()
    return content

def removefile(filepath:str):
    '''
    remove the file

    raise exception if filepath doesn't exists
    '''
    if not validate_path(pathlib.Path(filepath).parent):
        raise Exception(f'The given root {filepath} doesn\'t exists')
    if not validate_path(filepath):
        raise Exception(f'The specified {filepath} doesn\'t exists')
    if not os.path.isfile(filepath):
        raise Exception(f'The specified {filepath} is not a file')
    os.remove(filepath)