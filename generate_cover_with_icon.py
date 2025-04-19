from PIL import Image
import os

lut = {
    "#999999": "#c1ab5a",
    "#6b6b6b": "#957f2d",
    "#585858": "#522e10"
}
color_icon_shadow = "#312104"

template_path = "assets/minecraft/textures/item/enchanted_book/cover/_template.png"
output_dir = "assets/minecraft/textures/item/enchanted_book/cover/"
overlay_dir = "assets/minecraft/textures/font/enchantment/"
template_in_gui_dir = "assets/minecraft/textures/item/enchanted_book/in_gui/_template/"
output_in_gui_dir = "assets/minecraft/textures/item/enchanted_book/in_gui/"

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

os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_in_gui_dir, exist_ok=True)
os.makedirs(os.path.join(output_in_gui_dir, "thick"), exist_ok=True)

template_image = Image.open(template_path).convert("RGBA")
template_in_gui_bases                 = [None]
template_in_gui_base_top              = Image.open(template_in_gui_dir+"base_level_top.png").convert("RGBA")
template_in_gui_base_impossible       = Image.open(template_in_gui_dir+"base_level_impossible.png").convert("RGBA")
template_in_gui_thick_bases           = [None]
template_in_gui_thick_base_top        = Image.open(template_in_gui_dir+"base_thick_level_top.png").convert("RGBA")
template_in_gui_thick_base_impossible = Image.open(template_in_gui_dir+"base_thick_level_impossible.png").convert("RGBA")
for i in range(1,5):
    template_in_gui_bases      .append(Image.open(template_in_gui_dir+f"base_level_{i}.png").convert("RGBA"))
    template_in_gui_thick_bases.append(Image.open(template_in_gui_dir+f"base_thick_level_{i}.png").convert("RGBA"))

for ench, top_level in enchantments_top_level.items():
    
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
    
    tex_3D = template_image.copy()
    tex_3D.paste(overlay_image, (19, 2), overlay_image)
    tex_3D.save(os.path.join(output_dir, f"{ench}.png"))
    
    
    overlay_shadow = Image.open(overlay_path).convert("RGBA")
    
    # Make every non-transparent pixel to the shadow color
    pixels = overlay_shadow.load()
    for y in range(overlay_shadow.size[1]):
        for x in range(overlay_shadow.size[0]):
            rgba = pixels[x, y]
            if rgba[3] != 0:
                new_rgba = tuple(int(color_icon_shadow[i:i+2], 16) for i in (1, 3, 5)) + (rgba[3],)
                pixels[x, y] = new_rgba
                
                
    # Level below the top level
    for lvl in range(1, top_level):
        tex_in_gui = template_in_gui_bases[lvl].copy()
        tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
        tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
        tex_in_gui.save(os.path.join(output_in_gui_dir, f"{ench}_{lvl}.png"))
        
        tex_in_gui = template_in_gui_thick_bases[lvl].copy()
        tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
        tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
        tex_in_gui.save(os.path.join(output_in_gui_dir, f"thick/{ench}_{lvl}.png"))
        
    # Level at the top level
    tex_in_gui = template_in_gui_base_top.copy()
    tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
    tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
    tex_in_gui.save(os.path.join(output_in_gui_dir, f"{ench}_top_{top_level}.png"))
    
    tex_in_gui = template_in_gui_thick_base_top.copy()
    tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
    tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
    tex_in_gui.save(os.path.join(output_in_gui_dir, f"thick/{ench}_top_{top_level}.png"))
    
    # Level exceeding the top level
    tex_in_gui = template_in_gui_base_impossible.copy()
    tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
    tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
    tex_in_gui.save(os.path.join(output_in_gui_dir, f"{ench}_impossible.png"))
    
    tex_in_gui = template_in_gui_thick_base_impossible.copy()
    tex_in_gui.paste(overlay_shadow, (8, 1), overlay_shadow)
    tex_in_gui.paste(overlay_image,  (8, 0), overlay_image)
    tex_in_gui.save(os.path.join(output_in_gui_dir, f"thick/{ench}_impossible.png"))

print("Images created successfully.")
