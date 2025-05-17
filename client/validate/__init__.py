'''
validate

module to validate strings
'''

def validate(string:str,*rules):
    '''
    validate the given string by the given rules
    
    rules: tuple of functions with one argument of type str and output true if the string is valid
    '''
    for rule in rules:
        if not rule(string):
            return False
        pass
    return True
