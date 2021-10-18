import pathlib
import json


my_dex_path = pathlib.Path(r'myParty.json')
rival_dex_path = pathlib.Path(r'rivalParty.json')



class Pokemon():
    def __init__(self, name, start_hp, energy_type, weakness, resistance, moves):
        # The following is a summary of the inputs to this class:
        # - (str) name: the name of the pokemon
        # - (int) start_hp: the starting (or base) hp of the pokemon
        # - (str) energy_type: the energy type of the pokemon (electric, water,
        #   fire, etc,.)
        # - (str) weakness: the energy type the pokemon is weak against
        # - (str) resistence: the energy type the pokemon is resistant against
        # - (tuple) moves: a tuple of ((str), (int)) pairs that represent the
        #   move name and damage amount
        self.name = name
        self.start_hp = start_hp
        self.hp = start_hp 
        self.energy_type = energy_type
        self.weakness = weakness # a tuple that represents the energy type and stregth of the weakness (if any)
        self.resistance = resistance # a tuple that represents the energy type and damage offset of the resiliance (if any)
        self.moves = moves
        self.is_fainted = False # a boolean that represents if the pokemon is at 0 HP 

    def take_damage(self, damage_amount):
        self.hp -= damage_amount

        if self.hp < 0:
            self.hp = 0

        if self.hp == 0:
            self.is_fainted = True

class PokeCardDex():
    def __init__(self, json_file_path=None):
        # NOTE: It is important to handle the case where no path is passed in
        # meaning that json_file_path has a value of None.
        self.json_file_path = json_file_path

        if json_file_path is None: 
            self.party = [] # List of Pokemon that represents the current party. 

        else:

            self.party = [] # List of Pokemon that represents the current party. 

            with open(self.json_file_path) as reader:
                pokedex = json.load(reader)

            for monster in pokedex:

                energy_type = '' 
                for item in monster['types']:
                    energy_type += item

                if monster.get('weaknesses') != None:
                    for item in monster.get('weaknesses'):
                        weakness = (item['type'], int(item['value'].replace('x','')))
                else:
                    weakness = None

                if monster.get('resistances') != None:
                    for item in monster.get('resistances'):
                        resistance = (item['type'], int(item['value'])) 
                else:
                    resistance = None

                moves_list = []

                for item in monster['attacks']:
                    if item['damage'] == '':
                        moves_list.append((item['name'], int(item['damage'].replace('','5'))))
                    else:
                        moves_list.append((item['name'], int(item['damage'].replace('+','').replace('x',''))))

                moves = tuple(moves_list)

                self.party.append(Pokemon(monster['name'], int(monster['hp']), energy_type, weakness, resistance, moves)) 

    def set_order(self, order):
        # Sets the order of the pokemon based on a list of strings for the pokemon that is passed in
        ordered_party = []
        for item in order:
            for i in range(len(self.party)):
                if item in self.party[i].name:
                    ordered_party.append(Pokemon(self.party[i].name, self.party[i].hp, self.party[i].energy_type, self.party[i].weakness, self.party[i].resistance, self.party[i].moves))

        self.party = ordered_party

    def battle(self, challenger_party): 
        # Simulates a battle based on the passed in opposing PokeCardDex class's party
        k = 0
        m = 0

        i = 0
        j = 0

        while self.party[m].hp > 0 and challenger_party.party[k].hp > 0: 

            base_damage_to_self = challenger_party.party[k].moves[i][1]
            base_damage_to_challenger = self.party[m].moves[j][1]

            self_weakness_to_challenger = 1
            challenger_weakness_to_self = 1

            if self.party[m].weakness != None:
                if self.party[m].weakness[0] == challenger_party.party[k].energy_type:
                   self_weakness_to_challenger = self.party[m].weakness[1]

            if challenger_party.party[k].weakness != None:
                if challenger_party.party[k].weakness[0] == self.party[m].energy_type:
                    challenger_weakness_to_self = challenger_party.party[k].weakness[1]

            self_resistance_to_challenger = 0
            challenger_resistance_to_self = 0

            if self.party[m].resistance != None:
                if self.party[m].resistance[0] == challenger_party.party[k].energy_type:
                    self_resistance_to_challenger = self.party[m].resistance[1]

            if challenger_party.party[k].resistance != None:
                if challenger_party.party[k].resistance[0] == self.party[m].energy_type:
                    challenger_resistance_to_self = challenger_party.party[k].resistance[1]


            self.party[m].take_damage(base_damage_to_self * self_weakness_to_challenger + self_resistance_to_challenger)

            if self.party[m].hp > 0 and challenger_party.party[k].hp > 0:
                 challenger_party.party[k].take_damage(base_damage_to_challenger * challenger_weakness_to_self + challenger_resistance_to_self)

            print(f'{self.party[m].name}: {self.party[m].hp}, {challenger_party.party[k].name}: {challenger_party.party[k].hp}')

            if i < len(challenger_party.party[k].moves) - 1:
                i += 1
            else:
                i = 0
            if j < len(self.party[m].moves) - 1:
                j += 1
            else:
                j = 0

            if self.party[m].hp <= 0:
                print(f'{challenger_party.party[k].name} wins with {challenger_party.party[k].hp} HP remaining; {self.party[m].name} has fainted: {self.party[m].hp} HP remaining')
                if m < len(self.party) - 1:
                    m += 1
                    j = 0
                else:
                    print('Party 1 (self) defeated')

            if challenger_party.party[k].hp <= 0:
                print(f'{self.party[m].name} wins with {self.party[m].hp} HP remaining; {challenger_party.party[k].name} has fainted: {challenger_party.party[k].hp} HP remaining')
                if k < len(challenger_party.party) - 1:
                    k += 1
                    i = 0
                else:
                    print('Party 2 (challenger) defeated')

    def heal_party(self):
        # heals the party pokemon to their original starting hp
        for i in range(len(self.party)):
            self.party[i].hp = self.party[i].start_hp

    def add_to_party(self, pokemon):
        self.party.append(pokemon) # adds a Pokemon to the party. It will be added to the end of the party order


# Below is an example usage for using the classes
if __name__ == "__main__":
    my_dex = PokeCardDex(my_dex_path) 
    rival_dex = PokeCardDex()
    pikachu = Pokemon('Pikachu', 100, 'electric', None, None, (('electric charge', 30),))
    rival_dex.add_to_party(pikachu)

print('pokemon in "my_dex" - testing PokeCardDex __init__')
for i in range(len(my_dex.party)): 
    print(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves, my_dex.party[i].is_fainted)
    #print(type(my_dex.party[i].name), type(my_dex.party[i].hp), type(my_dex.party[i].energy_type), type(my_dex.party[i].weakness), type(my_dex.party[i].resistance), type(my_dex.party[i].moves), type(my_dex.party[i].is_fainted))

print()
print('pokemon in "rival_dex" - testing "add_to_party"')
for i in range(len(rival_dex.party)):
    print(rival_dex.party[i].name, rival_dex.party[i].hp, rival_dex.party[i].energy_type, rival_dex.party[i].weakness, rival_dex.party[i].resistance, rival_dex.party[i].moves, rival_dex.party[i].is_fainted)

print()
print('changing the order of my_dex.party based on a list of names - testing "set_order"')
#ordered_party = []
name_order = ['Weezing', 'Doduo', 'Skarmory', 'Chansey', 'Machoke', 'Persian', 'Clefable', 'Chikorita', 'Mareep']
#for item in name_order:
#    for i in range(len(my_dex.party)):
#        if item in my_dex.party[i].name:
#            ordered_party.append(Pokemon(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves))

#my_dex.party = ordered_party

my_dex.set_order(name_order)        
for i in range(len(my_dex.party)): 
    print(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves, my_dex.party[i].is_fainted)
    #print(type(my_dex.party[i].name), type(my_dex.party[i].hp), type(my_dex.party[i].energy_type), type(my_dex.party[i].weakness), type(my_dex.party[i].resistance), type(my_dex.party[i].moves), type(my_dex.party[i].is_fainted))


print()
print('setting all pokemon in "my_dex" to hp = 0')
for i in range(len(my_dex.party)):
    my_dex.party[i].hp = 0

for i in range(len(my_dex.party)): 
    print(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves, my_dex.party[i].is_fainted)
  
print()
print('resetting all pokemon in "my_dex" to orig hp - testing "heal_party"')
#for i in range(len(my_dex.party)):
#    my_dex.party[i].hp = my_dex.party[i].start_hp

my_dex.heal_party()

for i in range(len(my_dex.party)): 
    print(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves, my_dex.party[i].is_fainted)

print()
print('printing rival_dex_2:')
rival_dex_2 = PokeCardDex(rival_dex_path)

for i in range(len(rival_dex_2.party)): 
    print(rival_dex_2.party[i].name, rival_dex_2.party[i].hp, rival_dex_2.party[i].energy_type, rival_dex_2.party[i].weakness, rival_dex_2.party[i].resistance, rival_dex_2.party[i].moves, rival_dex_2.party[i].is_fainted)

print()
print('changing the order of rival_dex_2.party based on a list of names - testing "set_order"')
name_order_2 = ['Abra', 'Meganium', 'Hitmonchan', 'Porygon', 'Ekans', 'Butterfree', 'Venomoth', 'Dewgong', 'Feraligatr', 'Zapdos']
rival_dex_2.set_order(name_order_2)     

for i in range(len(rival_dex_2.party)): 
    print(rival_dex_2.party[i].name, rival_dex_2.party[i].hp, rival_dex_2.party[i].energy_type, rival_dex_2.party[i].weakness, rival_dex_2.party[i].resistance, rival_dex_2.party[i].moves, rival_dex_2.party[i].is_fainted)


print()
print('testing "battle"')

my_dex.battle(rival_dex_2)
print()
print('printing my_dex party')
for i in range(len(my_dex.party)): 
    print(my_dex.party[i].name, my_dex.party[i].hp, my_dex.party[i].energy_type, my_dex.party[i].weakness, my_dex.party[i].resistance, my_dex.party[i].moves, my_dex.party[i].is_fainted)

print()
print('printing rival_dex_2 party')
for i in range(len(rival_dex_2.party)): 
    print(rival_dex_2.party[i].name, rival_dex_2.party[i].hp, rival_dex_2.party[i].energy_type, rival_dex_2.party[i].weakness, rival_dex_2.party[i].resistance, rival_dex_2.party[i].moves, rival_dex_2.party[i].is_fainted)


