import pandas as pd

import Util
import Pokemon
import InstancePokemon
import Type
import Move
import Nature
Util.create_type_dict('TypeList.txt')
Util.create_move_dict('MoveList.csv')
Util.create_nature_dict('NatureList.csv')
Util.create_pokemon_dict('PokemonList.csv')

instance_dict = Util.create_instance_dict('InstanceList.csv') # party_self = create_instance_dict('PartyList.csv')

def test_type():
    assert(type(Type.Type.types_dict) == dict)
    assert(Type.Type.types_dict['Fire'].name == 'Fire')
    assert(Type.Type.types_dict['Fire'].list_super_effective == ['Grass', 'Ice', 'Bug', 'Steel'])
    assert(Type.Type.types_dict['Fire'].list_not_very_effective == ['Fire', 'Water', 'Rock', 'Dragon'])
    assert(Type.Type.types_dict['Fire'].list_zero_effect == [])
    assert(Type.Type.matchup(Type.Type.types_dict['Normal'], Type.Type.types_dict['Ghost']) == 0)
    
def test_move():
    assert(Move.Move.check_random() >= 0.85 and Move.Move.check_random() <= 1)
    assert(callable(Move.Move.check_type_effectiveness))
    assert(callable(Move.Move.check_burn))
    
def test_nature():
    assert(type(Nature.Nature.find_nature('modest')) == Nature.Nature)
    assert(Nature.Nature.check_mod('modest', 'sp_attack') == 1.1)
    
def test_pokemon():
    assert(Pokemon.Pokemon.return_move_list(Pokemon.Pokemon.find_pokemon('Ivysaur')) == ['Tackle', 'Growl', 'Energy_Ball', 'Take_Down', 'Toxic', 'Headbutt'])
    assert(type(Pokemon.Pokemon.get_pokemon()) == dict)
    
def test_instance_pokemon():
    assert(instance_dict['An Onion'].stat_dict == {
        'hp' : 155,
        'attack' : 74,
        'defense' : 83,
        'sp_attack' : 145,
        'sp_defense' : 100,
        'speed' : 92
    })
    
