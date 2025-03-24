import json
import copy as c

path = "assets/minecraft/models/item/enchanted_book/"

template_model = {
	"parent": "item/enchanted_book",
	"textures": {
		"book": "item/enchanted_book/cover/",
		"seal": "item/enchanted_book/seal/level_"
	}
}

enchantments_top_level = {
    "aqua_affinity": 1,
    "bane_of_arthropods": 5,
    "curse_of_binding": 1,
    "blast_protection": 4,
    "channeling": 1,
    "cleaving": 3,
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

def save_as(file_name, data):
    with open(path + file_name + ".json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)
        print(f"Generated: {file_name}.json")

for ench, top_level in enchantments_top_level.items():
    
    # Level below the top level
    for lvl in range(1, top_level):
        res = c.deepcopy(template_model)
        res["textures"]["book"] += ench
        res["textures"]["seal"] += str(lvl)
        save_as(f"{ench}_{lvl}", res)
    
    # Level at the top level
    res = c.deepcopy(template_model)
    res["textures"]["book"] += ench
    res["textures"]["seal"] += "top_" + str(top_level)
    save_as(f"{ench}_{top_level}", res)
        
    # Level exceeding the top level
    res = c.deepcopy(template_model)
    res["textures"]["book"] += ench
    res["textures"]["seal"] += "impossible"
    save_as(f"{ench}_impossible", res)