import json
import copy as c

save_to = "assets/minecraft/items/enchanted_book.json"

path_model = "item/enchanted_book/"
file_fallback = "item/enchanted_book"

# Some enchantments have different id from name.
ench_name_to_id = {
    "curse_of_binding": "binding_curse",
    "curse_of_vanishing": "vanishing_curse",
}

enchantments_top_level = {
    "aqua_affinity": 1,
    "bane_of_arthropods": 5,
    "curse_of_binding": 1,
    "blast_protection": 4,
    "channeling": 1,
    # "cleaving": 3,
    "depth_strider": 3,
    "efficiency": 5,
    "feather_falling": 4,
    "fire_aspect": 2,
    "fire_protection": 4,
    "flame": 1,
    "fortune": 3,
    "frost_walker": 2,
    "impaling": 5,
    "infinity": 1,
    "knockback": 2,
    "looting": 3,
    "loyalty": 3,
    "luck_of_the_sea": 3,
    "lure": 3,
    "mending": 1,
    "multishot": 1,
    "piercing": 4,
    "power": 5,
    "projectile_protection": 4,
    "protection": 4,
    "punch": 2,
    "quick_charge": 3,
    "respiration": 3,
    "riptide": 3,
    "sharpness": 5,
    "silk_touch": 1,
    "smite": 5,
    "soul_speed": 3,
    "sweeping_edge": 3,
    "swift_sneak": 3,
    "thorns": 3,
    "unbreaking": 3,
    "curse_of_vanishing": 1,
    "density": 5,
    "breach": 4,
    "wind_burst": 3,
}

res_json = {"model": {}}

template_case = {
    "type": "condition",
    "property": "component",
    "predicate": "stored_enchantments",
    "value": [{"enchantments": None}],
    "on_true": {},
    "on_false": {},
}

# Enchantments have higher priority
important_ench = [
    "curse_of_binding",
    "curse_of_vanishing",
]

max_top_level = max(enchantments_top_level.values())

order_ench = []  # (enchantment, top_level, is_impossible)[]

# Push important enchantments first
for ench in important_ench:
    top_level = enchantments_top_level[ench]
    order_ench.append((ench, top_level+1, True))
    for lvl in range(top_level, 0, -1):
        order_ench.append((ench, lvl, False))

order_ench_not_im = []
for ench, top_level in enchantments_top_level.items():
    if ench in important_ench: continue
    order_ench_not_im.append((ench, top_level+1, True))
    for lvl in range(top_level, 0, -1):
        order_ench_not_im.append((ench, lvl, False))

# For non-important enchantments, sort by: impossible first, then by level descending
order_ench_not_im.sort(key=lambda x: (x[2], x[1]), reverse=True)

order_ench = order_ench + order_ench_not_im

ref = res_json["model"]

for ench, lvl, is_impossible in order_ench:
    ench_id = ench_name_to_id.get(ench, ench)
    new_cond = c.deepcopy(template_case)
    new_cond["value"][0]["enchantments"] = ench_id
    base_name = ""
    if is_impossible:
        base_name = ench + "_impossible"
        new_cond["value"][0]["levels"] = {"min": lvl}
    else:
        base_name = ench + "_" + str(lvl)
        new_cond["value"][0]["levels"] = lvl
    
    ref_inner = new_cond["on_true"]
    for ench2 in enchantments_top_level.keys():
        if ench2 == ench: continue
        inner_cond = c.deepcopy(template_case)
        inner_cond["value"][0]["enchantments"] = ench_name_to_id.get(ench2, ench2)
        inner_cond["on_true"].update({"type": "model", "model": path_model + "_multiple_" + base_name})
        ref_inner.update(inner_cond)
        ref_inner = ref_inner["on_false"]
    ref_inner.update({"type": "model", "model": path_model + base_name})
        
    ref.update(new_cond)
    print("Model added: " + base_name)
    ref = ref["on_false"]

ref.update({"type": "model", "model": file_fallback})

with open(save_to, "w") as f:
    json.dump(res_json, f, indent=0, ensure_ascii=True)
    print(f"Generated: {save_to}")
