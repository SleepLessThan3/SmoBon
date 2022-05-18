import pandas as pd

import Util
import Pokemon
import InstancePokemon
import Combat
import Type
import Move
import Nature

#Pep8 function/method/variable naming convention sucks and camel case is superior :^)

Util.create_type_dict('TypeList.txt')
Util.create_move_dict('MoveList.csv')
Util.create_nature_dict('NatureList.csv')
Util.create_pokemon_dict('PokemonList.csv')

instance_dict = Util.create_instance_dict('InstanceList.csv') # party_self = create_instance_dict('PartyList.csv')

def menu():
    print('  _____   __  __    ____    ____     ____    _   _ ')
    print(' / ____| |  \/  |  / __ \  |  _ \   / __ \  | \ | |')
    print('| (___   | \  / | | |  | | | |_) | | |  | | |  \| |')
    print(' \___ \  | |\/| | | |  | | |  _ <  | |  | | | . ` |')
    print(' ____) | | |  | | | |__| | | |_) | | |__| | | |\  |')
    print('|_____/  |_|  |_|  \____/  |____/   \____/  |_| \_|')
    print()
    print("Welcome to Smobon, the definitely not ripoff of Smogon. What would you like to do?")
    print('~~~~~~~~~~~~~~~~~~~~')
    print('-Battle')
    # print('-Create New Pokemon')
    print('-Changelog')
    print('-Quit')
    print('~~~~~~~~~~~~~~~~~~~~')
    
    line_in = input().lower()
    while(line_in != 'battle' and line_in != 'changelog' and line_in != 'quit'):
    # while(line_in != 'battle' and line_in != 'create new pokemon' and line_in != 'changelog' and line_in != 'quit'):
        print('\nInvalid entry. Please try again!')
        line_in = input().lower()
    return line_in
    
def choose_self_pokemon():
    print()
    print("Here is a list of all currently available Pokemon. Enter a Pokemon's name to select it, or enter 'Back' to return to the previous menu.")
    print('~~~~~~~~~~~~~~~~~~~~')
    for item in instance_dict:
        print(item)
    print('~~~~~~~~~~~~~~~~~~~~')
    
    line_in = input()
    while(line_in not in instance_dict and line_in.lower() != 'back'):
        print('\nInvalid entry. Please try again!')
        line_in = input()
    return line_in
    
def choose_opponent_pokemon():
    print()
    print("Choose a Pokemon to battle against. Enter a Pokemon's name to select it, or enter 'Back' to return to the previous menu.")
    print('~~~~~~~~~~~~~~~~~~~~')
    for item in instance_dict:
        print(item)
    print('~~~~~~~~~~~~~~~~~~~~')
    
    line_in = input()
    while(line_in not in instance_dict and line_in.lower() != 'back'):
        print('\nInvalid entry. Please try again!')
        line_in = input()
    return line_in
    
def confirm_pokemon(line_in):
    print()
    instance_dict[line_in].get_summary()
    # print(instance_dict[line_in].get_summary())
    print()
    print('Would you like to select this Pokemon?')
    print('~~~~~~~~~~~~~~~~~~~~')
    print('-Yes')
    print('-No')
    print('~~~~~~~~~~~~~~~~~~~~')
    
    line_in = input().lower()
    while(line_in != 'yes' and line_in != 'no'):
        print('\nInvalid entry. Please try again!')
        line_in = input().lower()
    return line_in
    
line_in = None
self_pokemon = None
opponent_pokemon = None
status = 'menu'

while status == 'menu':
    line_in = menu()
    
    while line_in == 'battle':
        line_in = choose_self_pokemon()
        self_pokemon = line_in
        
        
        while line_in in instance_dict:
            line_in = confirm_pokemon(self_pokemon)
            
            while line_in == 'yes':
                line_in = choose_opponent_pokemon()
                opponent_pokemon = line_in
                
                while line_in in instance_dict:
                    line_in = confirm_pokemon(opponent_pokemon)
                    
                    while line_in == 'yes':
                        status = 'battle'
                        line_in = None
                        print(line_in)
                    if line_in == 'no':
                        line_in = 'yes'
                        break
                if line_in == 'back':
                    line_in = 'battle'
                    break
            if line_in == 'no':
                line_in = 'battle'
                break
        if line_in == 'back':
            line_in = None
            break
    while line_in == 'changelog':
        print()
        print('working?')
        Util.read('FinalProject\\Changelog.txt')
        print("Enter any key to return to the menu.")
        input()
        break
    if line_in == 'quit':
        break
    
if status == 'battle':    
    print(instance_dict[self_pokemon].name + ' is battling against ' + instance_dict[opponent_pokemon].name)
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    Combat.combat(instance_dict[self_pokemon], instance_dict[opponent_pokemon])
print('Goodbye.')