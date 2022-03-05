import random

from Classes.game import Person, BColors
from Classes.magic import Spell
from Classes.inventory import Item


# create black magic
fire = Spell('Fire', 25, 600, 'black')
thunder = Spell('Thunder', 25, 600, 'black')
blizzard = Spell('Blizzard', 25, 600, 'black')
meteor = Spell('Meteor', 40, 1200, 'black')
quake = Spell('Quake', 14, 140, 'black')

# create white magic
cure = Spell('Cure', 25, 620, 'white')
cura = Spell('Cura', 32, 1500, 'white')
curaga = Spell('Curaga', 50, 6000, 'white')

# Create Items
potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
hipotion = Item('Hi-Potion', 'potion', 'Heals 100 HP', 100)
superpotion = Item('Super-Potion', 'potion', 'Heals 1000 HP', 1000)
elixir = Item('Elixir', 'elixir', 'Fully restores HP/MP of one of the party members', 9999)
hielixer = Item('MegaElixer', 'elixir', "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", 'attack', 'Deal 500 damage', 500)

# instantiate people
player_spell = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spell = [fire, meteor, cure, curaga]

player_items = [{'item': potion, 'quantity': 15},
                {'item': hipotion, 'quantity': 5},
                {'item': superpotion, 'quantity': 5},
                {'item': elixir, 'quantity': 5},
                {'item': hielixer, 'quantity': 2},
                {'item': grenade, 'quantity': 1}]

player1 = Person('Valos ', 4600, 132, 300, 34, player_spell, player_items)
player2 = Person('Nick  ', 5600, 188, 311, 34, player_spell, player_items)
player3 = Person('Robot ', 6600, 174, 288, 34, player_spell, player_items)

enemy1 = Person('Imp  ', 1250, 130, 560, 325, enemy_spell, [])
enemy2 = Person('Magus', 11200, 701, 525, 25, enemy_spell, [])
enemy3 = Person('Imp  ', 1250, 130, 560, 325, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(BColors.FAIL + BColors.BOLD + 'An enemy attacks' + BColors.ENDC)

while running:
    print('===================')
    print('\n')
    print('Name                HP                                        MP')
    for player in players:
        player.get_stats()

    print('\n')

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input('    Choose an action:')
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print('You attacked ' + enemies[enemy].name + 'for', dmg, 'points of damage')

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + ' has died')
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('    Choose magic: ')) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(BColors.FAIL + '\nNot enough MP\n' + BColors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            if spell.typed == 'white':
                player.heal(magic_dmg)
                print(BColors.OKBLUE + '\n' + spell.name + 'Heals for', str(magic_dmg), 'HP.' + BColors.ENDC)
            elif spell.typed == 'black':
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(BColors.OKBLUE + '\n' + spell.name + ' deals', str(magic_dmg), 'points of damage to '+ enemies[enemy].name + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + ' has died')
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input('    Choose item: ')) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']

            if player.items[item_choice]['quantity'] == 0:
                print(BColors.FAIL + '\n' + 'None left...' + BColors.ENDC)
                continue

            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(BColors.OKGREEN + '\n' + item.name + ' heals for', item.prop, 'HP' + BColors.ENDC)
            elif item.type == 'elixir':

                if item.name == 'MegaElixer':
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp

                print(BColors.OKGREEN + '\n' + item.name + ' Fully restores HP/MP' + BColors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(BColors.FAIL + '\n' + item.name + ' deals', str(item.prop), 'points of damage to ' + enemies[enemy].name + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + ' has died')
                    del enemies[enemy]

    # check if battle is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # check if player won
    if defeated_enemies == 2:
        print(BColors.OKGREEN + 'You win!' + BColors.ENDC)
        running = False

    # check if enemy won
    elif defeated_players == 2:
        print(BColors.FAIL + 'You lose!' + BColors.ENDC)
        running = False

    print('\n')
    # enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name + ' attacks ', players[target].name, 'for ', enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.typed == 'white':
                enemy.heal(magic_dmg)
                print(BColors.OKBLUE + spell.name + ' Heals ' + enemy.name + ' for', str(magic_dmg), 'HP.' + BColors.ENDC)
            elif spell.typed == 'black':
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)
                print(BColors.OKBLUE + '\n' + enemy.name.replace(' ', '') + "'s " + spell.name + ' deals', str(magic_dmg), 'points of damage to ' + str(players[target].name) + BColors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + ' has died')
                    del players[player]

            # print('Enemy chose', spell, 'damage is', magic_dmg)

