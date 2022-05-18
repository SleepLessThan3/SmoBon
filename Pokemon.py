import Type
#import Data #what is this

class Pokemon():
    pokemon_dict = {}
    
    def __init__(self, name, element_type, hp = 1, attack = 1, defense = 1, sp_attack = 1, sp_defense = 1, speed = 1, ability_list = [], move_list = []):
        '''Creates the different species of Pokemon
            
        Parameters
        ----------
            name : string
                The name of the new Pokemon.
                
            element_type : list of strings
                The list of types of the Pokemon.
                
            hp : int
                Defaults to 1. The base health of the Pokemon.
                
            attack : int
                Defaults to 1. The base attack of the Pokemon.
                
            defense : int
                Defaults to 1. The base defense of the Pokemon.
                
            sp_attack : int
                Defaults to 1. The base special attack of the Pokemon.
                
            sp_defense : int
                Defaults to 1. The base special defense of the Pokemon.
                
            speed : int
                Defaults to 1. The base speed of the Pokemon.
                
            ability_list : list of Abilities
                Defaults to an empty list. Denotes all the possible abilites that the Pokemon can have.
                
            move_list : list of Moves
                Defaults to an empty list. The list of all moves that a Pokemon can learn.
                
        Returns
        -------
            None
        '''
        
        self.name = name
        self.element_type = element_type
        
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        
        self.ability_list = ability_list
        self.move_list = move_list
        
        Pokemon.pokemon_dict[name] = self
    
    def return_move_list(self):
        # Returns a dictionary of all moves that the species of Pokemon can learn.
        
        return self.move_list
        
    def return_nature_list(self):
        # Returns a list of all possible abilities for the species of Pokemon.
        
        return self.ability_list()
        
    def find_pokemon(species):
        # Takes in a string of a Pokemon species and returns the Pokemon.
        return Pokemon.pokemon_dict[species]
    def get_pokemon():
        # Returns a dictionary containing all Pokemon.
        
        return Pokemon.pokemon_dict