import pandas as pd

import Type
import Move
import Pokemon
import InstancePokemon
import Nature

'''This file houses the utility methods that are used to make things easier on me.
'''

def create_type_dict(txt_file):
    '''Opens a txt file and uses it to create a dictionary of all types.
    
    Parameters
    ----------
        txt_file : string
            The name of the text file that is being read.
            
    Returns
    -------
        type_dict : dictionary of Types
            A dictionary of all possible types.
    '''
    type_dict = {}
    
    file = open(txt_file, 'r')
    for line in file:
        name = line.strip('\n')
        super_effective = list(file.readline().split())
        not_very_effective = list(file.readline().split())
        no_effect = list(file.readline().split())
        type_dict[name] = Type.Type(name, super_effective, not_very_effective, no_effect)
    file.close()
    
    return type_dict

def create_move_dict(csv_file):
    '''Opens a csv file and uses it to create a dictionary of all moves.
    
    Parameters
    ----------
        csv_file : string
            The name of the csv file that is being read.
            
    Returns
    -------
        move_dict : dictionary of Moves
            A dictionary of all possible moves.
    '''
    move_dict = {}
    file = pd.read_csv(csv_file)
    for item in range(0,len(file)):
        name = file.loc[item, 'name']
        element_type = file.loc[item, 'element_type']
        category = file.loc[item, 'category']
        base_power = file.loc[item, 'base_power']
        base_accuracy = file.loc[item, 'base_accuracy']
        pp = file.loc[item, 'pp']
        effect = list(str(file.loc[item, 'effect']).split())
        effect_chance = file.loc[item, 'effect_chance']
        move_dict[name] = Move.Move(name, element_type, category, base_power, base_accuracy, pp, effect, effect_chance)
    
    return move_dict

def create_nature_dict(csv_file):
    '''Opens a csv file and uses it to create a dictionary of all natures.
    
    Parameters
    ----------
        csv_file : string
            The name of the csv file that is being read.
            
    Returns
    -------
        effect_dict : dictionary of Natures
            A dictionary of natures.
    '''
    nature_dict = {}
    file = pd.read_csv(csv_file)
    for item in range(0,len(file)):
        id_ = item
        name = file.loc[item, 'name']
        increased = file.loc[item, 'increased']
        decreased = file.loc[item, 'decreased']
        nature_dict[name] = Nature.Nature(id_, name, increased, decreased)
    
    return nature_dict

def create_pokemon_dict(csv_file):
    '''Opens a csv file and uses it to create a dictionary of all Pokemon.
    
    Parameters
    ----------
        csv_file : string
            The name of the csv file that is being read.
            
    Outputs
    -------
        pokemon_dict : dictionary of Pokemon
            A dictionary of Pokemon
    '''
    pokemon_dict = {}
    file = pd.read_csv(csv_file)
    for item in range(0,len(file)):
        name = file.loc[item, 'name']
        element_type = list(file.loc[item, 'element_type'].split('/'))
        hp = file.loc[item, 'hp']
        attack = file.loc[item, 'attack']
        defense = file.loc[item, 'defense']
        sp_attack = file.loc[item, 'sp_attack']
        sp_defense = file.loc[item, 'sp_defense']
        speed = file.loc[item, 'speed']
        ability_list = list(file.loc[item, 'ability_list'].split('/'))
        move_list = list(file.loc[item, 'move_list'].split('/'))
        pokemon_dict[name] = Pokemon.Pokemon(name, element_type, hp, attack, defense, sp_attack, sp_defense, speed, ability_list, move_list)
    
    return pokemon_dict
    
def create_instance_dict(csv_file):
    '''Opens a csv file and uses it to create a dictionary of all instances of Pokemon.
    
    Parameters
    ----------
        csv_file : string
            The name of the csv file that is being read.
            
    Outputs
    -------
        instance_dict : dictionary of instances of Pokemon
            A dictionary of InstancePokemon
    '''
    instance_dict = {}
    file = pd.read_csv(csv_file)
    for item in range(0,len(file)):
        name = file.loc[item, 'name']
        species = file.loc[item, 'species']
        level = file.loc[item, 'level']
        hp_ev = file.loc[item, 'hp_ev']
        attack_ev = file.loc[item, 'attack_ev']
        defense_ev = file.loc[item, 'defense_ev']
        sp_attack_ev = file.loc[item, 'sp_attack_ev']
        sp_defense_ev = file.loc[item, 'sp_defense_ev']
        speed_ev = file.loc[item, 'speed_ev']
        nature = file.loc[item, 'nature']
        ability = file.loc[item, 'ability']
        move_list = list(file.loc[item, 'move_list'].split('/'))
        
        instance_dict[name] = InstancePokemon.InstancePokemon(name, species, level, hp_ev, attack_ev, defense_ev, sp_attack_ev, sp_defense_ev, speed_ev, nature, ability, move_list)
    
    return instance_dict
    
def read(txt_file):
    '''Reads a txt file. For the changelog.
    
    Parameters
    ----------
        txt_file : string
            The Name of the txt file that is being read.
            
    Outputs
    -------
        None
    '''
    file = open(txt_file, 'r')
    print('test')
    print(file.read())
    file.close()
    
def clean(move):
    '''Makes the move name pretty.

    Parameters
    ----------
        move : Move
            The move that is being made pretty
            
    Returns
    -------
        string
            Pretty name
    '''
    
    return move.name.replace('_', ' ').title()
    
def adjust(line_in):
    for i in range(0,3 - int(len(line_in) / 8)):
        line_in = line_in + '\t'
    return line_in