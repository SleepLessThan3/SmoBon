import Type
import Move
import Pokemon
import Ability
import Nature

import pandas as pd

class InstancePokemon():
    def __init__(self, name, species,  level = 100, hp_ev = 0, attack_ev = 0, defense_ev = 0, sp_attack_ev = 0, sp_defense_ev = 0, speed_ev = 0, nature = None, ability = None, move_list = []):
        '''Creates the different instances of Pokemon that can be used to battle.
            
        Parameters
        ----------
            name : string
                The name of the individual Pokemon.
                
            species : string
                The species of Pokemon. Base stats are derived from here.
                
            level : int
                The level of the Pokemon.
                
            hp_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            attack_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            defense_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            sp_attack_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            sp_defense_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            speed_ev : int
                A number between 0 and 255 denoting the number of health effort values that the Pokemon has.
                
            nature : string
                The nature of the Pokemon. Affects calculated stat totals.
                Please consult the included NatureList.txt or https://pokemon3d.net/wiki/index.php/Natures
                to view the list of natures and affected stats.
                
            ability : string
                The Pokemon's ability.
                
            move_list : list of strings
                A set of up to 4 moves that the Pokemon can use in battle. Moves that are not in the
                species' movelist will not be counted, as well as extra moves that cause the number of moves to be greater than four.
                
        Returns
        -------
            None
        '''
        
        self.name = name
        self.species = Pokemon.Pokemon.find_pokemon(species)
        self.level = level
        self.nature = nature
        self.stat_dict = self.calculate_stats(hp_ev, attack_ev, sp_attack_ev, defense_ev, sp_defense_ev, speed_ev)
        self.ability = ability
        # self.move_list = check_move_list(moveList)
        self.move_list = move_list
        
        #self.stat_dict = {}
        
        # Used for combat
        self.instance_stats = {
            'hp' : self.stat_dict['hp'],
            'attack' : 0,
            'defense' : 0,
            'sp_attack' : 0,
            'sp_defense' : 0,
            'speed' : 0,
            'accuracy' : 0,
            'evasion' : 0,
            
            'attack_mod' : 1,
            'defense_mod' : 1,
            'sp_attack_mod' : 1,
            'sp_defense_mod' : 1,
            'speed_mod' : 1,
            'accuracy_mod' : 1,
            'evasion_mod' : 1,
            
            'critical' : 0,
            'status' : [''],
            'toxic' : 0,
            'sleep' : 0,
            'confusion' : 0
        }
        
        
    def calculate_mod(self):
        # Calculates stat modifiers.
        
        for stat_name in ['attack', 'defense', 'sp_attack', 'sp_defense', 'speed']:
            if self.instance_stats[stat_name + '_mod'] >= 0:
                self.instance_stats[stat_name + '_mod'] = (self.instance_stats[stat_name] + 2) / 2
            else:
                self.instance_stats[stat_name + '_mod'] = 2/(-self.instance_stats[stat_name] + 2)
                
        for stat_name in ['accuracy', 'evasion']:
            if self.instance_stats[stat_name + '_mod'] >= 0:
                self.instance_stats[stat_name + '_mod'] = (self.instance_stats[stat_name] + 3) / 3
            else:
                self.instance_stats[stat_name + '_mod'] = 3/(-self.instance_stats[stat_name] + 3)
            
    def calculate_stats(self, hp_ev, attack_ev, sp_attack_ev, defense_ev, sp_defense_ev, speed_ev):
        '''Uses instance variables to calculate a Pokemon's stat values.
        
        Parameters
        ----------
            hp_ev : int
                The Pokmeon's HP EVs
                
            attack_ev : int
                The Pokmeon's attack EVs
                
            defense_ev : int
                The Pokmeon's defense EVs
                
            sp_attack_ev : int
                The Pokmeon's special attack EVs
                
            sp_defense_ev : int
                The Pokmeon's special defense EVs
                
            speed_ev : int
                The Pokmeon's speed EVs
                
        Returns
        -------
            stat_dict : dictionary of ints
                A dictionary containing the Pokemon's stats
        '''
        stat_dict = {}
        stat_dict['hp'] = InstancePokemon.hp_formula(self.species.hp, hp_ev, 31, self.level)
        stat_dict['attack'] = InstancePokemon.stat_formula('attack', self.species.attack, attack_ev, 31, self.level, self.nature)
        stat_dict['defense'] = InstancePokemon.stat_formula('defense', self.species.defense, defense_ev, 31, self.level, self.nature)
        stat_dict['sp_attack'] = InstancePokemon.stat_formula('sp_attack', self.species.sp_attack, sp_attack_ev, 31, self.level, self.nature)
        stat_dict['sp_defense'] = InstancePokemon.stat_formula('sp_defense', self.species.sp_defense, sp_defense_ev, 31, self.level, self.nature)
        stat_dict['speed'] = InstancePokemon.stat_formula('speed', self.species.speed, speed_ev, 31, self.level, self.nature)
        
        return stat_dict
        
    # def update_stats(self, hp_ev, attack_ev, sp_attack_ev, defense_ev, sp_defense_ev, speed_ev):
        # Uses instance variables to calculate a Pokemon's stat values.
        
        
        # stat_dict['attack'] = (InstancePokemon.stat_formula('attack', self.species.attack, attack_ev, 31, self.level, self.nature) * self.instance_stats['attack_mod'])
        # stat_dict['defense'] = (InstancePokemon.stat_formula('defense', self.species.defense, defense_ev, 31, self.level, self.nature) * self.instance_stats['defense_mod'])
        # stat_dict['sp_attack'] = (InstancePokemon.stat_formula('sp_attack', self.species.sp_attack, sp_attack_ev, 31, self.level, self.nature) * self.instance_stats['sp_attack_mod'])
        # stat_dict['sp_defense'] = (InstancePokemon.stat_formula('sp_defense', self.species.sp_defense, sp_defense_ev, 31, self.level, self.nature) * self.instance_stats['sp_defense_mod'])
        # stat_dict['speed'] = (InstancePokemon.stat_formula('speed', self.species.speed, speed_ev, 31, self.level, self.nature) * self.instance_stats['speed_mod'])
        
        # return stat_dict
        
    def hp_formula(base_stat, ev, iv = 31, level = 100):
        ''' Formula for calculating health.
        
        Parameters
        ----------
            base_stat : int
                The value of the base stat.
                
            ev : int
                The EV for the stat.
                
            iv : int
                The IV for the stat.
                
            level : int
                The level of the Pokemon.
                
        Outputs
        -------
            int
                The calculated stat.
        '''
        
        return int((((2 * base_stat) + iv + int(ev / 4)) * level / 100) + level + 10)
        
    def stat_formula(stat_name, base_stat, ev, iv = 31, level = 100, nature = ''):
        '''Formula for calculating stats that are not health before nature modifier.
        
        Parameters
        ----------
            base_stat : int
                The value of the base stat.
                
            ev : int
                The EV for the stat.
                
            iv : int
                The IV for the stat.
                
            level : int
                The level of the Pokemon.
                
            nature : string
                The nature of the Pokemon.
                
        Outputs
        -------
            int
                The calculated stat.
        '''
        
        return int(((((2 * base_stat) + iv + int(ev / 4)) * (level / 100)) + 5) * Nature.Nature.check_mod(nature, stat_name))
        
    def get_summary(self):
        # Prints the summary for the Pokemon
        
        print(self.name + ' / ' + self.species.name + '\nHP\t: ', self.stat_dict['hp'], '\nAtk\t: ', self.stat_dict['attack'], '\nDef\t: ', self.stat_dict['defense'], '\nSp Atk\t: ', self.stat_dict['sp_attack'], '\nSp Def\t: ', self.stat_dict['sp_defense'], '\nSpd\t: ', self.stat_dict['speed'])
        
    def reset_instance(self):
        self.instance_stats = {
            'hp' : self.stat_dict['hp'],
            'attack' : 0,
            'defense' : 0,
            'sp_attack' : 0,
            'sp_defense' : 0,
            'speed' : 0,
            'accuracy' : 0,
            'evasion' : 0,
            
            'attack_mod' : 1,
            'defense_mod' : 1,
            'sp_attack_mod' : 1,
            'sp_defense_mod' : 1,
            'speed_mod' : 1,
            'accuracy_mod' : 1,
            'evasion_mod' : 1,
            
            'critical' : 0,
            'status' : [''],
            'toxic' : 0,
            'sleep' : 0,
            'confusion' : 0
        }
        
    # maybe put the following in class checkLegal?
    def check_move_list(self, move_list):
        '''# Adjusts the movelist to ensure all moves are legal.
        for move in moveList: # Removes moves that are not in the species' movelist.
            if move not in self.species.returnMoveList():
                moveList.remove(move)'''
        '''This method makes sure that a Pokemon's moveset is limited to 4 moves.
        
        Parameters
        ----------
            moveList : list of Moves
                This list represents the current movelist of a given Pokemon
                
        Returns
        -------
            modified_list : list of Moves
                The returned list is shortened if longer than 4, but is
                otherwise the same moveList as the function argument.
        '''
        move_list = modified_list
        while len(modified_list) > 4: # Shortens the set of moves to a length of 4.
            modified_list_list.remove(random.choice(list(move_list)))
        return modified_list