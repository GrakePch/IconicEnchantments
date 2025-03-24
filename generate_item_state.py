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
    "value": [{"enchantments": None, "levels": None}],
    "on_true": {"type": "model", "model": None},
    "on_false": {},
}

ref = res_json["model"]

for ench, top_level in enchantments_top_level.items():
    ench_id = ench_name_to_id.get(ench, ench)
    for lvl in range(1, top_level + 1):
        new_cond = c.deepcopy(template_case)
        new_cond["value"][0]["enchantments"] = ench_id
        new_cond["value"][0]["levels"] = lvl
        new_cond["on_true"]["model"] = path_model + ench + "_" + str(lvl)
        ref.update(new_cond)
        ref = ref["on_false"]
    new_cond = c.deepcopy(template_case)
    new_cond["value"][0]["enchantments"] = ench_id
    new_cond["value"][0]["levels"] = {"min": top_level + 1}
    new_cond["on_true"]["model"] = path_model + ench + "_impossible"
    ref.update(new_cond)
    ref = ref["on_false"]

ref.update({"type": "model", "model": file_fallback})

with open(save_to, "w") as f:
    json.dump(res_json, f, indent=0, ensure_ascii=True)
    print(f"Generated: {save_to}")
