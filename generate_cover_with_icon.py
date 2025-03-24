from PIL import Image
import os

lut = {
    # "#999999": "#312104",
    "#999999": "#c1ab5a",
    "#585858": "#522e10"
}

template_path = "assets/minecraft/textures/item/enchanted_book/cover/_template.png"
output_dir = "assets/minecraft/textures/item/enchanted_book/cover/"
overlay_dir = "assets/minecraft/textures/font/enchantment/"

list_ench = [
    "aqua_affinity",
    "bane_of_arthropods",
    "curse_of_binding",
    "blast_protection",
    "channeling",
    "cleaving",
    "depth_strider",
    "efficiency",
    "feather_falling",
    "fire_aspect",
    "fire_protection",
    "flame",
    "fortune",
    "frost_walker",
    "impaling",
    "infinity",
    "knockback",
    "looting",
    "loyalty",
    "luck_of_the_sea",
    "lure",
    "mending",
    "multishot",
    "piercing",
    "power",
    "projectile_protection",
    "protection",
    "punch",
    "quick_charge",
    "respiration",
    "riptide",
    "sharpness",
    "silk_touch",
    "smite",
    "soul_speed",
    "sweeping_edge",
    "swift_sneak",
    "thorns",
    "unbreaking",
    "curse_of_vanishing",
    "density",
    "breach",
    "wind_burst",
]

os.makedirs(output_dir, exist_ok=True)

template_image = Image.open(template_path).convert("RGBA")

for ench in list_ench:
    new_image = template_image.copy()
    
    overlay_path = os.path.join(overlay_dir, f"{ench}.png")
    overlay_image = Image.open(overlay_path).convert("RGBA")
    
    # Recolor pixels based on lut
    pixels = overlay_image.load()
    for y in range(overlay_image.size[1]):
        for x in range(overlay_image.size[0]):
            rgba = pixels[x, y]
            hex_color = "#{:02x}{:02x}{:02x}".format(rgba[0], rgba[1], rgba[2])
            if hex_color in lut:
                new_color = lut[hex_color]
                new_rgba = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)) + (rgba[3],)
                pixels[x, y] = new_rgba
    
    new_image.paste(overlay_image, (19, 2), overlay_image)
    
    new_image.save(os.path.join(output_dir, f"{ench}.png"))

print("Images created successfully.")
