import pandas as pd

class Nature():
    natures_dict = {}
    
    def __init__(self, id_, name, increase = '', decrease = ''):
        '''This class creates the possible natures for the Pokemon.
        
        Parameters
        ----------
            name : string
                The name of the nature.
                
            incerease : string
                Defaults to an empty string. The stat that is increased.
                
            decrease : string
                Defaults to an empty string. The stat that is decreased.
                
        Returns
        -------
            None
        '''
        #self.id_ = id_
        self.name = name
        self.increase = increase
        self.decrease = decrease
        
        Nature.natures_dict[name] = self
        
    def get_name(self):
        return self.name
        
    def find_nature(nature_name):
        return Nature.natures_dict[nature_name]
        
    def check_nature(name):
        '''Checks if the argument string is the name of an existing Nature, and if so, returns that Nature.
        
        Parameters
        ----------
            name : string
                The name of the nature.
                
        Returns
        -------
            match : Nature
                A matching nature
        '''
        if name in natures_dict:
            return natures_dict[name]
        else:
            print('Error: Nature [' + name + '] does not exist')
        
    def check_mod(nature_name, stat_name):
        '''Returns a float/integer between 0.9 and 1.1 depending on how a nature
        affects a given stat.
        
        Parameters
        ----------
            nature_name : string
                The name of the nature that is being checked
                
            stat_name : string
                The name of the stat that is being checked
                
        Returns
        -------
            int
                Float/integer between 0.9 and 1.1
        '''
        
        if(Nature.find_nature(nature_name).increase == stat_name):
            return 1.1
        elif(Nature.find_nature(nature_name).decrease == stat_name):
            return 0.9
        else:
            return 1