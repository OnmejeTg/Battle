import random


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ['Attack', 'Magic', 'Items']
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp = self.hp - dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print('\n' + BColors.BOLD + '    ' + self.name + BColors.ENDC)
        print(BColors.OKBLUE + BColors.BOLD + '    ACTIONS' + BColors.ENDC)
        for item in self.actions:
            print('    ' + '    ' + str(i) + '.', item)
            i += 1

    def choose_magic(self):
        i = 1
        print('\n' + BColors.OKBLUE + BColors.BOLD + '    MAGIC' + BColors.ENDC)
        for spell in self.magic:
            print('    ' + '    ' + str(i) + '.', spell.name, '( cost: ', str(spell.cost) + ')')
            i += 1

    def choose_item(self):
        i = 1
        print('\n' + BColors.OKGREEN + BColors.BOLD + '    ITEM' + BColors.ENDC)
        for item in self.items:
            print('    ' + '    ' + str(i) + '.', item['item'].name, ':', item['item'].description, '(x' + str(item['quantity']) + ')')
            i += 1

    def choose_target(self, enemies):
        i = 1
        print('\n' + BColors.FAIL + BColors.BOLD + '    TARGET:' + BColors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 1:
                print('        ' + str(i) + '.', enemy.name)
            i += 1
        choice = int(input('    Choose target:')) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ''
        bar_ticks = (self.hp/self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += '???'
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += ' '

        hp_string = str(self.hp) + '/' + str(self.maxhp)
        current_hp = ''

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print('                      __________________________________________________')
        print(BColors.BOLD + self.name + ':    ' +
              current_hp + '|' + BColors.FAIL + hp_bar + BColors.ENDC + '|       ')

    def get_stats(self):

        hp_bar = ''
        bar_ticks = (self.hp/self.maxhp) * 100 / 4

        mp_bar = ''
        mp_ticks = (self.mp / self.maxmp) * 100 / 10

        while bar_ticks > 0:
            hp_bar += '???'
            bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += ' '

        while mp_ticks > 0:
            mp_bar += '???'
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += ' '

        hp_string = str(self.hp) + '/' + str(self.maxhp)
        current_hp = ''

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + '/' + str(self.maxmp)
        current_mp = ''
        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)

            while decreased > 0:
                current_mp += ' '
                decreased -= 1

            current_mp += mp_string

        else:
            current_mp = mp_string

        print('                    _________________________                 __________')
        print(BColors.BOLD + self.name + ':   ' +
              current_hp + '|' + BColors.OKGREEN + hp_bar + BColors.ENDC + '|       ' +
              BColors.BOLD + current_mp + ' |' + BColors.OKBLUE + mp_bar + BColors.ENDC + '|')

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.typed == 'white' and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg

