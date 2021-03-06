from RePoE.util import write_json, call_with_default_args


def write_default_monster_stats(data_path, relational_reader, **kwargs):
    root = {}
    for row in relational_reader['DefaultMonsterStats.dat']:
        root[row['DisplayLevel']] = {
            'physical_damage': row['Damage'],
            'evasion': row['Evasion'],
            'accuracy': row['Accuracy'],
            'life': row['Life'],
            'ally_life': row['AllyLife']
        }
    write_json(root, data_path, 'default_monster_stats')


if __name__ == '__main__':
    call_with_default_args(write_default_monster_stats)
