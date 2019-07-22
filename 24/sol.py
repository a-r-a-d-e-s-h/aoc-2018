import re
import time
from collections import defaultdict

start_time = time.time()

class UnitGroup:
    def __init__(self, line, army_name):
        self.raw_line = line
        self.parse_line()
        self.remaining_units = self.units
        self.army_name = army_name
        self.boost = 0

    def parse_line(self):
        line = self.raw_line
        units, line = line.split(' units each with ')
        self.units = int(units)
        hp, line = line.split(' hit points ')
        self.hp = int(hp)

        regex = "^\((.*)\)"
        result = re.match(regex, line)
        self.weak_to = []
        self.immune_to = []
        if result:
            specials = result.groups()[0]
            secs = specials.split('; ')
            for sec in secs:
                if sec.startswith('immune'):
                    sec = sec.split('immune to ')[1]
                    add_to = self.immune_to
                elif sec.startswith('weak'):
                    sec = sec.split('weak to ')[1]
                    add_to = self.weak_to
                add_to.extend(sec.split(', '))
        line = line.split('with an attack that does ')[1]
        words = line.split(' ')
        self.attack_damage = int(words[0])
        self.attack_type = words[1]
        self.initiative = int(words[-1])

    def effective_power(self):
        return self.remaining_units * (self.attack_damage + self.boost)

    def compute_damage(self, group):
        if self.attack_type in group.immune_to:
            return 0
        if self.attack_type in group.weak_to:
            return 2 * self.effective_power()
        return self.effective_power()

    def take_hit(self, hps):
        self.remaining_units -= hps//self.hp
        self.remaining_units = max(0, self.remaining_units)

    def __repr__(self):
        return "{}: i={} ep={}".format(self.army_name, self.initiative, self.effective_power())

def do_fight(army_data):
    all_unit_groups = []
    for unit_groups in army_data.values():
        all_unit_groups.extend(unit_groups)
    all_unit_groups.sort(key=lambda x: -x.initiative)

    battle_in_progress = True
    while battle_in_progress:
        target_choice_order = list(all_unit_groups)
        target_choice_order.sort(key=lambda x: (-x.effective_power(), -x.initiative))
        target_choices = []
        for ug in target_choice_order:
            targets = sorted(all_unit_groups, key=lambda x: (-ug.compute_damage(x), -x.effective_power(), -x.initiative))
            for t in targets:
                if t.remaining_units == 0:
                    continue
                if t.army_name == ug.army_name:
                    continue
                if t in target_choices:
                    continue
                if ug.compute_damage(t) == 0:
                    continue
                target_choices.append(t)
                break
            else:
                target_choices.append(None)
        for ug, target in zip(target_choice_order, target_choices):
            ug.next_target = target

        for ug in all_unit_groups:
            if ug.next_target is None:
                continue
            else:
                ug.next_target.take_hit(ug.compute_damage(ug.next_target))
        if all(ug.next_target is None for ug in unit_groups):
            battle_in_progress = False

        surviving_units = defaultdict(int)
        for ug in all_unit_groups:
            surviving_units[ug.army_name] += ug.remaining_units
        if 0 in surviving_units.values():
            battle_in_progress = False


def calculate_margin(filename, boost=0):
    with open(filename) as f:
        text = f.read().strip()

    sections = text.split('\n\n')
    assert len(sections) == 2
    army_data = {}
    for sec in sections:
        lines = sec.splitlines()
        if lines[0].lower().startswith('immune'):
            army_name = 'immune'
        elif lines[0].lower().startswith('infection'):
            army_name = 'infection'
        army_data[army_name] = [UnitGroup(l, army_name) for l in lines[1:]]

    for ug in army_data['immune']:
        ug.boost = boost

    do_fight(army_data)
    infection_units = sum(ug.remaining_units for ug in army_data['infection'])
    immune_units = sum(ug.remaining_units for ug in army_data['immune'])
    if infection_units > 0: # default for infection winning in case of tie
        return ("infection", infection_units)
    else:
        return ("reindeer", immune_units)

def part_1(filename):
    return calculate_margin(filename)[1]

def part_2(filename):
    boost = 0
    while 1:
        result = calculate_margin(filename, boost)
        if result[0] == 'infection':
            boost += 1
        else:
            return {'boost': boost, 'margin': result[1]}

assert part_1("test1.txt") == 5216
print("Part 1")
print(part_1("input.txt"))

test_result = part_2('test1.txt')
assert test_result['margin'] == 51
assert test_result['boost'] == 1570
result = part_2('input.txt')
print("Part 2 (with boost {})".format(result['boost']))
print(result['margin'])

print("Time elapsed: {:.2f}s".format(time.time() - start_time))
