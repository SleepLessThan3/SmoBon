import Type
import Status
import InstancePokemon
import random

class Move():
    '''This class houses the methods and functions associated with moves and their associated logic.
    '''
    moves_dict = {}
    
    def __init__(self, name, element_type, category, base_power = 0, base_accuracy = 100, pp = 1, effect = [], effect_chance = 0):
        '''Creates the moves that Pokemon can use.
        
        Parameters
        ----------
            name : string
                The name of the move
                
            element_type : string
                The type of the move.
                
            category : string
                The category of the move. Can be 'Physical' (ex. Tackle), 'Special'
                (ex. Water Gun), or 'Status' (ex. Growl)
                
            base_power : int
                Defaults to 0. The base power of an attacking move. Does not affect status moves.
                
            base_accuracy : int
                Defaults to 100. The base accuracy (out of 100) of the move. Moves that never
                miss(auch as Aerial Ace) have an accuracy value of -1.
                
            pp : int
                Defaults to 1. The number of times that a move can be used in battle.
                
            effect : list
                Defaults to an empty list. A string denoting the secondary effect that a move
                has (such as a flinch, poison, burn, stat change)and an int (1-100)
                denoting the percentage chance that the status takes effect.
                
        Returns
        -------
            None
        '''
        
        self.name = name
        self.element_type = element_type
        self.category = category
        self.base_power = base_power
        self.base_accuracy = base_accuracy
        self.pp = pp
        self.effect = effect
        self.effect_chance = effect_chance
        
        Move.moves_dict[name] = self
        
    def return_moves():
        # This function returns a dictionary containing all moves.
        
        return Move.moves_dict
        
    # The following functions are related to calculating the damage of a move.
    def calc_damage(move, user, target, weather):
        ''' This method calculates the damage dealt by an attack against a target. If the move deals an absolute value for damage, that value will be returned.
        Parameters
        ----------
            move : Move
                The used move.
            user : InstancePokemon
                The user of the move.
            target : InstancePokemon
                The target of the attack.
            weather : string
                The current weather.
                
        Returns
        -------
            [int, bool, int]
                The damage dealt, whether it was a critical hit, and the type effectiveness of the move.
        '''
        
        crit = Move.check_crit(move, user)
        if crit > 1:
            is_crit = True
        else:
            is_crit = False
        
        effective = Move.check_type_effectiveness(move, target)
        if effective > 1:
            type_effect = 3
        elif effective == 1:
            type_effect = 2
        elif effective == 0:
            type_effect = 0 
        else:
            type_effect = 1
            
        if(effective < 1 and effective > 0 and is_crit):
            effective = 1
            
        mod = Move.check_weather(move, weather) * crit * Move.check_random() * Move.check_stab(move, user) * effective * Move.check_burn(move, user)
        damage = (((((user.level * 0.4) + 2) * move.base_power * (Move.check_stats(move, user, target, is_crit)))/50)+2) * mod
        
        return [int(damage), is_crit, type_effect]
        
    def confusion_damage(target):
        ''' This method calculates the damage dealt by a confused Pokemon against themselves.
        Parameters
        ----------
            target : InstancePokemon
                The Pokemon taking damage.
                
        Returns
        -------
            int
                The damage dealt.
        '''
        damage = (((((target.level * 0.4) + 2) * 40 * (Move.check_stats(Move.moves_dict['Tackle'], target, target, False)))/50)+2) * Move.check_burn(Move.moves_dict['Tackle'], target)
        return int(damage)
        
    def check_weather(move, weather):
        '''Normally, this function would return a value between 0.5 and 1.5 depending on the
        type of move used and the current weather, but weather has not been implemented,
        so it will just be returning 1.
        
        Parameters
        ----------
            move : Move
                The move that is being used.
            weather : Weather
                The current weather.
                
        Returns
        -------
            weather_modifier : float
                0.5, 1, or 0.5 depending on move type and weather.
        '''
        
        return 1

    def check_crit(move, user):
        '''Calculates a critical hit.
        Parameters
        ----------
            move : Move
                The move that is being used.
                
            user : InstancePokemon
                The Pokemon that is using the move.
                
        Returns
        -------
            int
                The modifier for a critical hit.
        '''
        if(user.instance_stats['critical'] == 0):
            if(random.randrange(24) == 23):
                return 1.5
            else:
                return 1
                
        elif(user.instance_stats['critical'] == 1):
            if(random.randrange(8) == 7):
                return 1.5
            else:
                return 1
                
        elif(user.instance_stats['critical'] == 2):
            if(random.randrange(2) == 1):
                return 1.5
            else:
                return 1
                
    def check_random():
        '''Returns a random float within 0.85 and 1.
        Parameters
        ----------
            None
            
        Returns
        -------
            float
                A random float within 0.85 and 1. 
        '''
        
        return (random.randint(85, 101) / 100)
                
    def check_stab(move, user):
        '''Calculates same type attack bonus (stab) of a move.
        Parameters
        ----------
            move : Move
                The move that is being used.
                
            user : InstancePokemon
                The Pokemon that is using the move.
                
        Returns
        -------
            int
                The modifier for same type attack bonus.
        '''
        
        if(move.element_type in user.species.element_type):
            return 1.5
        else:
            return 1
            
    def check_type_effectiveness(move, target):
        '''Calculates type effectiveness of a move against a target.
        
        Parameters
        ----------
            move : Move
                The move that is being used.
                
            target : InstancePokemon
                The target of the move.
                
        Returns
        -------
            multiplier : int
                The type effectiveness multiplier.
        '''
        
        multiplier = 1
        for element in target.species.element_type:
            attack_type = Type.Type.types_dict[move.element_type]
            pokemon_type = Type.Type.types_dict[element]
            multiplier = multiplier * attack_type.matchup(pokemon_type)
        return multiplier
        
    def check_burn(move, user):
        '''Calculates the effect of a burn.
        
        Parameters
        ----------
            user : InstancePokemon
                The Pokemon that is being checked.
                
        Returns
        -------
            int
                The damage modifier for a burn.
        '''
        
        if 'burn' in user.instance_stats['status']:
            if move.category == 'physical':
                if user.ability == 'guts':
                    return 1.5
                return 0.5
        return 1
        
    def check_stats(move, user, target, is_crit):
        ''' Returns the ratio of the user's offensive stat and the target's defensive stat.
        
        Parameters
        ----------
            move : Move
                The move that is being calculated for.
                
            user : InstancePokemon
                The user of the move.
                
            target : InstancePokemon
                The target of the move.
                
            is_crit : bool
                Whether the attack was a critical hit or not.
                
        Returns
        -------
            int
                A modifier for the calculated damage.
        '''
        mod = 0
        mod2 = 0
        if(move.category == 'Physical'):
            mod = user.stat_dict['attack'] / target.stat_dict['defense']
        elif(move.category == 'Special'):
            mod = user.stat_dict['sp_attack'] / target.stat_dict['sp_defense']
        elif(move.category == 'Physical_X'):
            mod = user.stat_dict['attack'] / target.stat_dict['sp_defense']
        elif(move.category == 'Special_X'):
            mod = user.stat_dict['sp_attack'] / target.stat_dict['defense']
            
        if is_crit:
            temp1 = 1
            temp2 = 1
            if(move.category == 'Physical'):
                if user.instance_stats['attack_mod'] > 1:
                    temp1 = user.instance_stats['attack_mod']
                if target.instance_stats['defense_mod'] < 1:
                    temp2 = target.instance_stats['defense_mod']
                    
            elif(move.category == 'Special'):
                if user.instance_stats['sp_attack_mod'] > 1:
                    temp1 = user.instance_stats['sp_attack_mod']
                if target.instance_stats['sp_defense_mod'] < 1:
                    temp2 = target.instance_stats['sp_defense_mod']
                    
            elif(move.category == 'Physical_X'):
                if user.instance_stats['attack_mod'] > 1:
                    temp1 = user.instance_stats['attack_mod']
                if target.instance_stats['sp_defense_mod'] < 1:
                    temp2 = target.instance_stats['sp_defense_mod']
                    
            elif(move.category == 'Special_X'):
                if user.instance_stats['sp_attack_mod'] > 1:
                    temp1 = user.instance_stats['sp_attack_mod']
                if target.instance_stats['defense_mod'] < 1:
                    temp2 = target.instance_stats['defense_mod']
            mod2 = temp1 * temp2
        else:
            if(move.category == 'Physical'):
                mod2 = user.instance_stats['attack_mod'] / target.instance_stats['defense_mod']
            elif(move.category == 'Special'):
                mod2 = user.instance_stats['sp_attack_mod'] / target.instance_stats['sp_defense_mod']
            elif(move.category == 'Physical_X'):
                mod2 = user.instance_stats['attack_mod'] / target.instance_stats['sp_defense_mod']
            elif(move.category == 'Special_X'):
                mod2 = user.instance_stats['sp_attack_mod'] / target.instance_stats['defense_mod']
                
        return mod * mod2
            
    def check_effect_chance(move, user):
        '''Checks for whether an effect is afflicted or not
        Parameters
        ----------
            move : Move
                The move that is being used.
                
            user : InstancePokemon
                The Pokemon that is using the move.
                
        Returns
        -------
            bool
                A boolean for whether an effect is afflicted or not.
        '''
        return move.effect_chance >= random.randrange(0,100)