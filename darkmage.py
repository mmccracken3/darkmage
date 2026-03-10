import math


def relic_cost(final_level, initial_level=None):
    if initial_level is None:
        return round(final_level ** 1.3, 0)
    total_cost = 0
    for cost in range(initial_level, final_level):
        total_cost += round(cost ** 1.3, 0)
    return total_cost


class RelicStats:
    def __init__(self, relic_levels):
        self.atk = relic_levels['atk'] * 2 + relic_levels['dm'] * 2
        self.mp = relic_levels['mp'] * 3 + relic_levels['dm'] * 2
        self.mboost = relic_levels['mboost'] * 0.03


class Equipment:
    def __init__(self, atk=0, mp=0, mboost=0.0):
        self.atk = atk
        self.mp = mp
        self.mboost = mboost


class DarkMage:
    def __init__(self, armor=None, weapon=None, accessory1=None, accessory2=None, relic_levels=None):
        relics = RelicStats(relic_levels)
        self.mp = 30 + armor.mp + weapon.mp + accessory1.mp + accessory2.mp + relics.mp
        self.atk = 8 + armor.atk + weapon.atk + accessory1.atk + accessory2.atk + relics.atk
        self.mboost = 0.8 + armor.mboost + weapon.mboost + accessory1.mboost + accessory2.mboost + relics.mboost

    @property
    def noxin(self):
        return self.atk * 0.6 * (1 + self.mboost)

    @property
    def necroblast(self):
        return (self.mp * 1.5 + self.atk * 0.9) * (1 + self.mboost)


class CostComparison:
    def __init__(self, equipment, relic_levels, dm_num, increment):
        self.equipment = equipment
        self.relic_levels = relic_levels
        self.increment = increment
        self.dm_num = dm_num

        atk_relic = dict(self.relic_levels)
        mp_relic = dict(self.relic_levels)
        dm_relic = dict(self.relic_levels)
        mboost_relic = dict(self.relic_levels)
        atk_relic['atk'] += self.increment
        mp_relic['mp'] += self.increment
        dm_relic['dm'] += self.increment
        mboost_relic['mboost'] += self.increment

        self.cost = {'atk': relic_cost(self.relic_levels['atk'] + self.increment,
                                       initial_level=self.relic_levels['atk']),
                     'mp': relic_cost(self.relic_levels['mp'] + self.increment,
                                      initial_level=self.relic_levels['mp']),
                     'dm': relic_cost(self.relic_levels['dm'] + self.increment,
                                      initial_level=self.relic_levels['dm']),
                     'mboost': relic_cost(self.relic_levels['mboost'] + self.increment,
                                          initial_level=self.relic_levels['mboost'])
                     }

        self.base_dm = DarkMage(armor=self.equipment['armor'], weapon=self.equipment['weapon'],
                                accessory1=self.equipment['accessory1'], accessory2=self.equipment['accessory2'],
                                relic_levels=self.relic_levels)
        self.atk_dm = DarkMage(armor=self.equipment['armor'], weapon=self.equipment['weapon'],
                               accessory1=self.equipment['accessory1'], accessory2=self.equipment['accessory2'],
                               relic_levels=atk_relic)
        self.mp_dm = DarkMage(armor=self.equipment['armor'], weapon=self.equipment['weapon'],
                              accessory1=self.equipment['accessory1'], accessory2=self.equipment['accessory2'],
                              relic_levels=mp_relic)
        self.dm_dm = DarkMage(armor=self.equipment['armor'], weapon=self.equipment['weapon'],
                              accessory1=self.equipment['accessory1'], accessory2=self.equipment['accessory2'],
                              relic_levels=dm_relic)
        self.mboost_dm = DarkMage(armor=self.equipment['armor'], weapon=self.equipment['weapon'],
                                  accessory1=self.equipment['accessory1'], accessory2=self.equipment['accessory2'],
                                  relic_levels=mboost_relic)

    def what_to_upgrade(self):
        if self.upgrade_necro():
            return self.compare_necroblast()
        else:
            return self.compare_noxin()

    def upgrade_cost(self):
        return self.cost[self.what_to_upgrade()]

    def wall80(self):
        return math.floor((self.base_dm.noxin * (self.dm_num - 1) - 575) / 4 / 100) * 100 + 180

    def wall1000(self):
        if math.floor((self.base_dm.necroblast * self.dm_num - 18430) / 20 / 1000) * 1000 + 1000 < 1000:
            return 1000
        return math.floor((self.base_dm.necroblast * self.dm_num - 18430) / 20 / 1000) * 1000 + 1000

    def wall(self):
        return max(self.wall80(), self.wall1000())

    def upgrade_necro(self):
        if self.wall80() > self.wall1000():
            return True
        return False

    def compare_necroblast(self):
        efficiencies = {'mp': (self.mp_dm.necroblast - self.base_dm.necroblast) / self.cost['mp'],
                        'dm': (self.dm_dm.necroblast - self.base_dm.necroblast) / self.cost['dm'],
                        'atk': (self.atk_dm.necroblast - self.base_dm.necroblast) / self.cost['atk'],
                        'mboost': (self.mboost_dm.necroblast - self.base_dm.necroblast) / self.cost['mboost']
                        }
        return max(efficiencies, key=efficiencies.get)

    def compare_noxin(self):
        efficiencies = {'dm': (self.dm_dm.noxin - self.base_dm.noxin) / self.cost['dm'],
                        'atk': (self.atk_dm.noxin - self.base_dm.noxin) / self.cost['atk'],
                        'mboost': (self.mboost_dm.noxin - self.base_dm.noxin) / self.cost['mboost']
                        }
        return max(efficiencies, key=efficiencies.get)


def main():
    relic_levels = {'atk':    600,
                    'mp':     160,
                    'mboost': 800,
                    'dm':     600}
    armor = Equipment(mp=65)
    weapon = Equipment(atk=145, mp=145)
    accessory1 = Equipment()
    accessory2 = Equipment()

    increment = 100
    dm_num = 2

    equipment = {
        'armor':  armor,
        'weapon': weapon,
        'accessory1': accessory1,
        'accessory2': accessory2
    }

    compare = CostComparison(equipment, relic_levels, dm_num, increment)

    print()
    space = 12
    print(''.ljust(space) + '|' + 'Noxin'.center(space) + '|' + 'Necro'.center(space))
    print('-' * space * 3)
    print('Limit'.ljust(space) + '|' + f'{compare.wall80():.0f}'.center(space) + '|' +
          f'{compare.wall1000():.0f}'.center(space))
    print('HP'.ljust(space) + '|' + f'{400 * int(compare.wall80() / 100) + 575:.0f}'.center(space) + '|' +
          f'{20000 * compare.wall1000() / 1000 + 18430:.0f}'.center(space))
    print('Tot. Damage'.ljust(space) + '|' + f'{compare.base_dm.noxin * (dm_num - 1):.0f}'.center(space) + '|' +
          f'{compare.base_dm.necroblast * dm_num:.0f}'.center(space))
    print('Ind. Damage'.ljust(space) + '|' + f'{compare.base_dm.noxin:.0f}'.center(space) + '|' +
          f'{compare.base_dm.necroblast:.0f}'.center(space))
    print()
    print(f'Upgrade {compare.what_to_upgrade()} to level {relic_levels[compare.what_to_upgrade()] + increment} at a'
          f' cost of {compare.upgrade_cost():.0f} essence')


if __name__ == '__main__':
    main()
