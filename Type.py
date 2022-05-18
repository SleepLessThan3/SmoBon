class Type():
    types_dict = {}
    
    def __init__(self, name, list_super_effective = [], list_not_very_effective = [], list_zero_effect = []):
        '''Creates the elemental types that comprise Pokemon and their moves.
        
        Parameters
        ----------
            name : string
                The name of the new type
                
            list_super_effective : list of strings
                Defaults to an empty list. A list of the names of the other types that the new type is super effective against.
                
            list_not_very_effective : list of strings
                Defaults to an empty list. A list of the names of the other types that the new type is not very effective against.
                
            list_zero_effect : list of strings
                Defaults to an empty list. A list of the names of the other types that the new type has no effect against.
            
        Returns
        -------
            None
        '''
        
        self.name = name
        self.list_super_effective = list_super_effective
        self.list_not_very_effective = list_not_very_effective
        self.list_zero_effect = list_zero_effect
        
        Type.types_dict[name] = self
        
    def matchup(self, input_type):
        # Returns a number 0 - 2 depending on the type effectiveness of the current type against the argument type, where 0 = no
        # effectiveness, and 2 = super effective. it is used as move_type.matchup(target_type)
        
        if(input_type.name in self.list_super_effective):
            return 2
        elif(input_type.name in self.list_not_very_effective):
            return 0.5
        elif(input_type.name in self.list_zero_effect):
            return 0
        else:
            return 1
            
    #create isSTAB() function?
        
    def return_types():
        # Returns a dictionary containing all types.
        
        return Type.types_dict
        