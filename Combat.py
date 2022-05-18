import Move
import InstancePokemon
import Status
import Util

import random

'''This script handles battles.'''

turn = 0
user_move = None
opponent_move = None
move_damage = []
weather = 'clear'

statuses = {
    'paralysis' : ' was paralyzed! It may be unable to move!',
    'burn' : ' was burned!',
    'poison' : ' was poisoned!',
    'toxic' : ' was badly poisoned!',
    'sleep' : ' fell asleep!',
    'freeze' : ' was frozen!',
    'confusion' : ' was confused!'
}

statuses2 = {
}

def combat(user, opponent):
    '''
    Parameters
    ----------
        user : InstancePokemon
            The user's Pokemon
            
        opponent : InstancePokemon
            The opponent's (cpu's) Pokemon
            
    Returns
    -------
        None
    '''
    turn = 0
    user_move = None
    opponent_move = None
    move_damage = []
    weather = 'clear'
    
    intro(user, opponent)
    
    while(user.instance_stats['hp'] > 0 and opponent.instance_stats['hp'] > 0):
        print(get_hp(opponent))
        print(get_hp(user))
        print(user.instance_stats['hp'], '/' ,user.stat_dict['hp'])
        user_move = query_move(user)
        opponent_move = pick_random(user)
        if user.stat_dict['speed'] > opponent.stat_dict['speed'] or (user.stat_dict['speed'] == opponent.stat_dict['speed'] and random.randrange(0,2) == 1):
            attack(user, opponent, user_move, weather)
            turn += 1
            if(user.instance_stats['hp'] <= 0 or opponent.instance_stats['hp'] <= 0):
                break
            attack(opponent, user, pick_random(opponent), weather)
            turn += 1
        else:
            attack(opponent, user, pick_random(opponent), weather)
            turn += 1
            if(user.instance_stats['hp'] <= 0 or opponent.instance_stats['hp'] <= 0):
                break
            attack(user, opponent, user_move, weather)
            turn += 1
        opponent.instance_stats['hp'] -= status_check_post(opponent, opponent_move)
        if(opponent.instance_stats['hp'] <= 0):
            break
        user.instance_stats['hp'] -= status_check_post(user, user_move)
        
    if user.instance_stats['hp'] <= 0:
        finish(opponent, user)
    elif opponent.instance_stats['hp'] <= 0:
        finish(user, opponent)
    
def get_hp(pokemon):
    '''Prints an HP bar for a Pokmeon
    Parameters
    ----------
        pokemon : InstancePokemon
            The Pokemon whose HP bar is being printed.
            
    Returns
    -------
        None
    '''
    
    out = ''
    num_bars = int(pokemon.instance_stats['hp'] / pokemon.stat_dict['hp'] * 50)
    
    for i in range(0, 50 - num_bars):
        out = out + '-'
    
    for i in range(50 - num_bars, 50):
        out = out + '|'
        
    out = Util.adjust(pokemon.name + ':') + ('[' + out + ']')
    
    return out
    
def reset():
    # Resets class attributes
    turn = 0
    user_move = None
    opponent_move = None
    move_damage = 0
    weather = 'clear'
    
def query_move(pokemon):
    '''
    Parameters
    ----------
        pokemon : InstancePokemon
            The Pokemon that is being queried
            
    Returns
    -------
        move : Move
            The selected move
    '''
    print()
    print('What will ' + pokemon.name + ' do?')
    print('~~~~~~~~~~~~~~~~~~~~')
    for move in pokemon.move_list:
        print('-' + move)
    print('~~~~~~~~~~~~~~~~~~~~')
    move_selection = input()
    
    while(move_selection not in pokemon.move_list):
        print(pokemon.move_list)
        print(move_selection)
        print('\nInvalid entry. Please try again!')
        move_selection = input()
    return Move.Move.moves_dict[move_selection]
    
def pick_random(pokemon):
    '''Simple RNG for opponent Pokemon.
    Parameters
    ----------
        pokemon : InstancePokemon
            The attacking Pokemon.
            
    Returns
    -------
        Move
            The selected move.
    '''
    
    selected_move = random.choice(pokemon.move_list)
    return Move.Move.moves_dict[selected_move]
    
def attack(user, target, move, weather):
    '''
    Parameters
    ----------
        user : InstancePokemon
            The attacking Pokemon.
            
        target : InstancePokemon
            The target Pokemon.
            
        move : Move
            The used move.
            
    Returns
    -------
        None
    '''
    can_move = status_check_pre(user)
    if(can_move == 1):
        print(user.name + ' used ' + Util.clean(move) + '!')
        if(check_accuracy(user, target, move)):
            if(move.category == 'Physical' or move.category == 'Special'):
                move_damage = Move.Move.calc_damage(move, user, target, weather)
                if move_damage[0] == 0:
                    print('The move had no effect!')
                else:
                    if move_damage[1]:
                        print('A critical hit!')
                    elif move_damage[2] == 3 :
                        print('It was super effective!')
                    elif move_damage[2] == 1:
                        print('It was not very effective.')
                    target.instance_stats['hp'] -= move_damage[0]
                    if target.instance_stats['hp'] < 0:
                        target.instance_stats['hp'] = 0
                    apply_effect(move, user, target)
            elif(move.category == 'Status'):
                apply_effect(move, user, target)
        else:
            print('The attack missed!')
            
def check_accuracy(user, target, move): 
    '''Accuracy check for a Pokemon's move
    Parameters
    ----------
        user : InstancePokemon
            The attacking Pokemon.
            
        target : InstancePokemon
            The target Pokemon.
            
        move : Move
            The used move.
            
    Returns
    -------
        bool
            True : attack can hit
            False : attack misses
    '''
    
    if move.base_accuracy < 0:
        return True
    threshold = move.base_accuracy * user.instance_stats['accuracy_mod'] / target.instance_stats['evasion_mod']
    if random.randrange(0,100) < threshold:
        return True
    else:
        return False
    
def intro(user, opponent):
    # Prints battle start messages.
    print('Trainer PC would like to battle!\nTrainer PC sent out ' + opponent.name + '. Go ' + user.name + '!')
    
def finish(winning_pokemon, losing_pokemon):
    # Prints battle end messages.
    print(losing_pokemon.name + ' fainted!')
    print(winning_pokemon.name + ' was victorious!')
    
def apply_effect(move, user, target):
    '''Applies an effect on a user/target, depending on the move and effect
    Parameters
        ----------
            move : Move
                The move that is being used.
                
            user : InstancePokemon
                The Pokemon that is using the move.
                
            target : InstancePokemon
                The target of the move.
                
        Returns
        -------
            bool
                True if the move had an effect, and false if the effect failed.
    '''
    
    if move.effect_chance > random.randrange(0,100):
        if move.effect[0] == 'status':
            if move.effect[1] == 'user':
                if move.effect[2] in statuses:
                    user.instance_stats['status'][0] = move.effect[2]
                    return True
                else:
                    user.instance_stats['status'].append(move.effect[2])
                    return True
            elif move.effect[1] == 'target':
                if (move.effect[2] in statuses and move.effect[0] not in target.instance_stats['status']):
                    target.instance_stats['status'][0] = move.effect[2]
                    return True
                
        elif move.effect[0] == 'stat':
            if(move.effect[1] == 'user' and abs(user.instance_stats[move.effect[2]]) < 6):
                user.instance_stats[move.effect[2]] += int(move.effect[3])
                if int(move.effect[3]) > 0:
                    print(user.name + "'s " + move.effect[2] + ' increased!')
                elif int(move.effect[3]) < 0:
                    print(user.name + "'s " + move.effect[2] + ' decreased!')
                if user.instance_stats[move.effect[2]] > 6:
                    user.instance_stats[move.effect[2]] = 6
                elif user.instance_stats[move.effect[2]] < -6:
                    user.instance_stats[move.effect[2]] = -6
                print(user.instance_stats['defense'], user.instance_stats['defense_mod'])
                user.calculate_mod()
                print(user.instance_stats['defense'], user.instance_stats['defense_mod'])
                return True
            elif(move.effect[1] == 'target' and abs(target.instance_stats[move.effect[2]]) < 6):
                target.instance_stats[move.effect[2]] += int(move.effect[3])
                if int(move.effect[3]) > 0:
                    print(target.name + "'s " + move.effect[2] + ' increased!')
                elif int(move.effect[3]) < 0:
                    print(target.name + "'s " + move.effect[2] + ' decreased!')
                if target.instance_stats[move.effect[2]] > 6:
                    target.instance_stats[move.effect[2]] = 6
                    return True
                elif target.instance_stats[move.effect[2]] < -6:
                    target.instance_stats[move.effect[2]] = -6
                    return True
            else:
                if(move.effect[1] == 'target' and target.instance_stats[move.effect[2]] == 6) or (move.effect[1] == 'user' and user.instance_stats[move.effect[2]] == 6):
                    print("The stat can't get any higher!")
                if(move.effect[1] == 'target' and target.instance_stats[move.effect[2]] == -6) or (move.effect[1] == 'user' and user.instance_stats[move.effect[2]] == -6):
                    print("The stat can't get any lower!")
            
        elif move.effect[0] == 'damage':
            if move.effect[1] == 'user':
                user.instance_stats['hp'] -= int(move.effect[2])
                if user.instance_stats['hp'] <= 0:
                    user.instance_stats['hp'] = 0
                return True
            elif move.effect[1] == 'target':
                target.instance_stats['hp'] -= int(move.effect[2])
                if target.instance_stats['hp'] <= 0:
                    target.instance_stats['hp'] = 0
                return True
    return False

def status_check_pre(pokemon):
    '''Checks for the effects of status conditions before a turn.

    Parameters
    ----------
        pokemon : InstancePokemon
        
    Returns
    -------
        int
            0 : The Pokemon is unable to use a move.
            1 : The Pokemon is able to use a move.
    '''
    # print(pokemon.instance_stats['status'])
    if 'flinch' in pokemon.instance_stats['status']:
        pokemon.instance_stats['status'].remove('flinch')
        print(pokemon.name + ' flinched!')
        return 0
    for status in pokemon.instance_stats['status']:
        if status == 'paralysis':
            if random.randrange(0,100) < 25:
                True
            else:
                print(pokemon.name + " is paralyzed! It can't move!")
                return 0
        elif status == 'freeze':
            if random.randrange(0,100) < 20:
                pokemon.instance_stats['status'][0]  = ''
                print(pokemon.name + ' thawed out!')
            else:
                print(pokemon.name + ' is frozen solid!')
                return 0
        elif status == 'sleep':
            if pokemon.instance_stats['sleep'] == 0:
                pokemon.instance_stats['status'][0]  = ''
                print(pokemon.name + ' woke up!')
            elif pokemon.instance_stats['sleep'] > 0:
                pokemon.instance_stats['sleep'] -= 1
                print(pokemon.name + ' is fast asleep.')
                return 0
        elif status == 'confusion':
            if pokemon.instance_stats['confusion'] > 0:
                if random.randrange(0,100) < 33:
                    print(pokemon.name + ' hurt itself in confusion!')
                    pokemon.instance_stats['hp'] -= Move.Move.confusion_damage(pokemon)
                    pokemon.instance_stats['confusion'] -= 0
                    return 0
                else:
                    pokemon.instance_stats['hp'] -= Move.Move.confusion_damage(pokemon)
                    pokemon.instance_stats['confusion'] -= 0
                    return 1
            if pokemon.instance_stats['confusion'] <= 0:
                pokemon.instance_stats['status'].remove('confusion')
                print(pokemon.name + ' snapped out of confusion!')
                return 1
    return 1

def status_check_post(pokemon, move):
    '''Checks for the effects of status conditions after a turn.

    Parameters
    ----------
        pokemon : InstancePokemon
            The Pokemon.
            
        previous_move : Move
            The move just used by this Pokemon.
    Returns
    -------
        int
            The amount of damage that the Pokemon takes.
    '''
    
    for status in pokemon.instance_stats['status']:
        if status == 'burn':
            print(pokemon.name + ' is hurt by its burn!')
            return int(pokemon.stat_dict['hp'] / 16)
        elif status == 'poison':
            print(pokemon.name + ' is hurt by poison!')
            return int(pokemon.stat_dict['hp'] / 8)
        elif status == 'toxic':
            print(pokemon.name + ' is hurt by poison!')
            pokemon.instance_stats['toxic'] += 1
            return int(pokemon.stat_dict['hp'] * pokemon.instance_stats['toxic'] / 16)
        elif status == 'recoil':
            print(pokemon.name + ' is hit with recoil damage!')
            return int(move_damage[0] * (move.effect[3] / 100))
        else:
            return 0
            
    # status_list = ['paralysis', 'burn', 'poison', 'toxic', 'sleep', 'freeze', 'confusion', 'pause', 'hide', 'flinch', 'recoil', 'damage'] 
