class Configurable:
    '''
    base implementation of a configurable element
    '''

    _attributes = {}

    def __init__(self,**kwargs):
        for key in kwargs.keys():
            self._attributes[key] = kwargs[key]
            pass
        pass

    def __setattr__(self,item,value):
        self._attributes[item] = value
        pass

    def __getattr__(self,item):
        return self._attributes[item] if item in self._attributes.keys() else None