from RePoE.util import write_json, call_with_default_args


def _convert_alias_stats(alias_stats_key_1, alias_stats_key_2):
    r = {}
    if alias_stats_key_1 is not None:
        r['when_in_main_hand'] = alias_stats_key_1['Id']
    if alias_stats_key_2 is not None:
        r['when_in_off_hand'] = alias_stats_key_2['Id']
    return r


def write_stats(data_path, relational_reader, **kwargs):
    root = {}
    previous = set()
    for stat in relational_reader['Stats.dat']:
        if stat['Id'] in previous:
            print("Duplicate stat id %s" % stat['Id'])
            continue
        root[stat['Id']] = {
            'is_local': stat['IsLocal'],
            'is_aliased': stat['IsWeaponLocal'],
            'alias': _convert_alias_stats(stat['MainHandAlias_StatsKey'], stat['OffHandAlias_StatsKey']),
            # 'is_on_character_panel': stat['Flag6'],  # not sure
            # 'is_on_tooltip': stat['Flag7'],  # not sure
        }

    write_json(root, data_path, 'stats')


if __name__ == '__main__':
    call_with_default_args(write_stats)
