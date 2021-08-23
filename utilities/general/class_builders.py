class self_setup_class : 
    '''helper class to setup class which can create attributes from 
    the passed key value pairs during initalization of instance'''
    def __init__(self,**kwargs):
        self.set_inputs(**kwargs)
    def set_inputs(self,**inputs):
        for key in inputs:
            setattr(self,key,inputs.get(key))
    def __getitem__(self,tag):
        if not isinstance(tag,str):
            raise ValueError (f"{tag} is not string , provide key in string format" )
        return getattr(self,tag,None)
    def __setitem__(self,tag,value):
        if not isinstance(tag,str):
            raise ValueError (f"{tag} is not string , provide key in string format" )
        setattr(self,tag,value)
        return value
    def keys(self):
        return list(vars(self).keys())
    def items(self):
        return list(vars(self).items())
    def get(self,key,default=None):
        if self.__getitem__(key) is None :
            return default
        return self.__getitem__(key)