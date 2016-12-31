from PyPoE.poe.file.translations import TranslationFileCache, get_custom_translation_file
from RePoE.util import write_json,call_with_default_args


def _convert_tags(n_ids, tags, tags_types):
    f = ["ignore" for _ in range(n_ids)]
    for tag, tag_type in zip(tags, tags_types):
        if tag_type == "%":
            f[tag] = "#"
        elif tag_type == "$+d":
            f[tag] = "+#"
        elif tag_type == "$d%":
            f[tag] = "#%"
        elif tag_type == "d%":
            f[tag] = "#%"
        else:
            print("Unknown tag type:", tag_type)
    return f


def _convert_range(translation_range):
    rs = []
    for r in translation_range:
        if r.min is None and r.max is None:
            rs.append({})
        elif r.min is None:
            rs.append({
                'max': r.max
            })
        elif r.max is None:
            rs.append({
                'min': r.min
            })
        else:
            rs.append({
                'min': r.min,
                'max': r.max
            })
    return rs


def _convert_handlers(n_ids, index_handlers):
    hs = [[] for _ in range(n_ids)]
    for handler_name, ids in index_handlers.items():
        for i in ids:
            # Indices in the handler dict are 1-based
            hs[i - 1].append(handler_name)
    return hs


def _convert(tr):
    ids = tr.ids
    n_ids = len(ids)
    english = []
    for s in tr.get_language('English').strings:
        # todo: '%1$d' is not converted to format correctly
        # see e.g. "split_arrow_number_of_additional_arrows"
        english.append({
            'condition': _convert_range(s.range),
            'string': s.as_format_string,
            'format': _convert_tags(n_ids, s.tags, s.tags_types),
            'index_handlers': _convert_handlers(n_ids, s.quantifier.index_handlers)
        })
    return {
        'ids': ids,
        'English': english
    }


def write_stat_translations(ggpk, data_path, **kwargs):
    tc = TranslationFileCache(path_or_ggpk=ggpk, files=STAT_FILES)
    previous = set()
    root = []
    for f in STAT_FILES:
        previous_f = set()
        for tr in tc[f].translations:
            id_str = " ".join(tr.ids)
            if id_str in previous:
                if id_str in previous_f:
                    print("Duplicate id", tr.ids, "in file", f)
                continue
            previous.add(id_str)
            previous_f.add(id_str)
            root.append(_convert(tr))
    for tr in get_custom_translation_file().translations:
        id_str = " ".join(tr.ids)
        if id_str in previous:
            print("Duplicate custom id", tr.ids)
            continue
        previous.add(id_str)
        result = _convert(tr)
        result['hidden'] = True
        root.append(result)
    write_json(root, data_path, 'stat_translations')


# 'stat_descriptions.txt' tree
# - chest
# - gem
#   - active_skill_gem
#     - skill
#       - aura_skill
#       - beam_skill
#       - curse_skill
#       - debuff_skill
#       - minion_skill
#         - minion_attack_skill
#         - minion_spell_skill
#       - offering_skill
# - map
#   - atlas
# - passive_skill
#   - passive_aura_skill
# 'monster_stat_descriptions.txt' tree
STAT_FILES = [
    'stat_descriptions.txt',
    'gem_stat_descriptions.txt',
    'active_skill_gem_stat_descriptions.txt',
]


if __name__ == '__main__':
    call_with_default_args(write_stat_translations)
