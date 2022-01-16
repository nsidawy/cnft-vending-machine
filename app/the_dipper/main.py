import math
import os
import random

import cv2
import ffmpeg
from PIL import Image, ImageChops
from glitch_this import ImageGlitcher

effects = {
    'Fancy Ketchup':
        {
            'type': 'sandwich'
        },
    'Honey Mustard':
        {
            'type': 'single',
            'order': 1
        },
    'Kewl Ranch':
        {
            'type': 'single',
            'order': 2
        },
    'Blazing Buffalo':
        {
            'type': 'single',
            'order': 2
        },
    'Spooky Sauce':
        {
            'type': 'single',
            'order': 2
        },
    'Unsig Sauce':
        {
        },
    'Glitch Sauce':
        {
        },
    'Degen Dip':
        {
        }
}

# Only Degen Dip Eligible Sauces Go Here
# No Limited
SAUCES_BY_RARITY = {
    'Common' : [
        'Fancy Ketchup'
    ],
    'Uncommon' : [
        'Honey Mustard'
    ],
        'Rare' : [
        'Kewl Ranch'
    ],
        'Epic' : [
        'Blazing Buffalo'
    ],
        'Legendary' : [
        'Glitch Sauce'
    ],
        'Mythic' : [
        'Unsig Sauce'
    ]
}

SAUCE_RARITIES = [
    'Common',
    'Uncommon',
    'Rare',
    'Epic',
    'Legendary',
    'Mythic'
]

# Used for Degen Roll
# Common Dip Effect is weighted lower than normal to reward degens
WEIGHTS = (
  10, # Common
  30, # Uncommon
  25, # Rare
  20, # Epic
  10,  # Legendary
  5   # Mythic
)


glitcher = ImageGlitcher()

def degen_dip_roll():
    sauce_rarity = random.choices(SAUCE_RARITIES, weights=WEIGHTS, k=1)[0]
    sauce = random.choice(SAUCES_BY_RARITY[sauce_rarity])
    return sauce



def interpolate(start, end, size):
    delta = float(end - start) / (size - 1)
    return [start + int(i * delta) for i in range(size)]


def interpolate_color(start, end, size):
    red = interpolate(start[0], end[0], size)
    green = interpolate(start[1], end[1], size)
    blue = interpolate(start[2], end[2], size)
    alpha = interpolate(start[3], end[3], size)
    return zip(red, green, blue, alpha)


def dip_nugget(nugget_base_path, nugget_id, sauce):
    nugget_file = f'{nugget_base_path}/Nugget_{nugget_id}/{nugget_id}-nug.png'

    dipped_nugget = []
    if sauce is None:
        for f in range(250):
            nug = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
            dipped_nugget.append(nug)
    elif sauce == 'Glitch Sauce':
        for f in range(250):
            amount = random.randint(25, 80) / 10.0
            nug = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
            if 100 < f < 200:
                glitched_nugget = glitcher.glitch_image(nug, amount, scan_lines=True,
                                                        seed=f, color_offset=True)
                dipped_nugget.append(glitched_nugget)
            else:
                dipped_nugget.append(nug)
    elif sauce == 'Unsig Sauce':
        original_nugget = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
        unsig = cv2.imread(f'{nugget_base_path}/dips/unsig/unsig.png')
        nug = cv2.imread(nugget_file)
        diff = nug.copy()
        cv2.absdiff(nug, unsig, diff)
        for f in range(125):
            dilated = cv2.dilate(diff.copy(), None, iterations=math.floor(f/5))
            unsigned_nug = original_nugget.copy()
            unsigned_nug.paste(Image.fromarray(dilated).resize((500, 500)), (0,0), original_nugget)
            dipped_nugget.append(unsigned_nug)
        for f in range(125):
            dipped_nugget.append(dipped_nugget[125-f-1])
        print(len(dipped_nugget))
    else:
        effect_type = effects[sauce]['type']
        if effect_type == 'single':
            order = effects[sauce]['order']
            for f in range(250):
                nug = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
                sauce_frame = Image.open(f'{nugget_base_path}/dips/{sauce}_2/{str(f).zfill(4)}.png').convert("RGBA").resize((500, 500),
                                                                                                         resample=0)
                if order == 1:
                    sauce_frame.paste(nug, (0, 0), nug)
                    dipped_nugget.append(sauce_frame)
                if order == 2:
                    nug.paste(sauce_frame, (0, 0), sauce_frame)
                    dipped_nugget.append(nug)
        elif effect_type == 'sandwich':
            for f in range(250):
                sauce_frame_a = Image.open(f'{nugget_base_path}/dips/{sauce}_2/A{str(f).zfill(4)}.png').convert("RGBA").resize(
                    (500, 500), resample=0)
                nug = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
                sauce_frame_b = Image.open(f'{nugget_base_path}/dips/{sauce}_2/B{str(f).zfill(4)}.png').convert("RGBA").resize(
                    (500, 500), resample=0)
                sauce_frame_b.paste(nug, (0, 0), nug)
                sauce_frame_b.paste(sauce_frame_a, (0, 0), sauce_frame_a)
                dipped_nugget.append(sauce_frame_b)
    return dipped_nugget


def blend_background(nugget_base_path, nugget_id, sauce):
    background_file = f'{nugget_base_path}/Nugget_{nugget_id}/{nugget_id}-background.png'
    background_frames = []

    if sauce == None:
        print("WARNING: FIRST SAUCE IS NONE, SOMETHING IS FUCKY")
        background_frame = Image.open(background_file).convert("RGBA").resize((500, 500), resample=0)
        for f in range(250):
            background_frames.append(background_frame)
    elif sauce == 'Glitch Sauce':

        additive = Image.open(f'{nugget_base_path}/dips/glitch/glitch_additive.png').convert("RGBA").resize((500, 500), resample=0)
        test_card = Image.open(f'{nugget_base_path}/dips/glitch/glitch_additive_alt2.png').convert("RGBA").resize((500, 500), resample=0)
        for f in range(250):
            background_frame = Image.open(background_file).convert("RGBA").resize((500, 500), resample=0)
            glitch_pre = ImageChops.add_modulo(background_frame, test_card)
            roll = random.randint(1, 5)
            if 50 < f < 150 or 200 < f:
                glitch_pre = ImageChops.subtract(glitch_pre, additive, 0.5, roll)
                background_frames.append(glitcher.glitch_image(glitch_pre, roll * 2,
                                                               seed=int(nugget_id) * f, color_offset=True,
                                                               scan_lines=True))
            else:
                background_frames.append(glitcher.glitch_image(background_frame, roll,
                                                               seed=int(nugget_id) * f, color_offset=False,
                                                               scan_lines=True))

    elif sauce == 'Unsig Sauce':
        for i in range(0, 250):
            unsig = cv2.imread(f'{nugget_base_path}/dips/unsig/unsig2.png')
            M = cv2.getRotationMatrix2D((540,540), 1.44*i, 1)
            rotated = cv2.warpAffine(unsig, M, (1080, 1080))
            rotated = rotated[int(290):int(790), int(290):int(790)]
            bg = Image.open(background_file).convert('RGBA')
            f = bg.resize((500, 500))
            fu =Image.fromarray(rotated).convert('RGBA')
            fum = ImageChops.blend(f, fu, math.sin(i/250))
            background_frames.append(fum)
    else:
        for f in range(250):
            background_frame = Image.open(background_file).convert("RGBA").resize((500, 500), resample=0)
            sauce_frame = Image.open(f'{nugget_base_path}/dips/{sauce}_1/{str(f).zfill(4)}.png').convert("RGBA").resize((500, 500),
                                                                                                     resample=0)
            background_frame.paste(sauce_frame, (0, 0), sauce_frame)
            background_frames.append(background_frame)
    return background_frames


def dip(nugget_base_path, nugget_id, used_sauce1, used_sauce2, output_dir):
    nid = str(nugget_id).zfill(5)
    if used_sauce1 == 'Degen Dip':
        sauce1 = degen_dip_roll()
    else:
        sauce1 = None if used_sauce1 is None else used_sauce1.replace('*', '')
    if used_sauce2 == 'Degen Dip':
        sauce2 = degen_dip_roll()
    else:
        sauce2 = None if used_sauce2 is None else used_sauce2.replace('*', '')
    background_frames = blend_background(nugget_base_path, nid, sauce1)

    nugget_frames = dip_nugget(nugget_base_path, nid, sauce2)
    nugget_file = f'{nugget_base_path}/Nugget_{nid}/{nid}-nug.png'
    nug = Image.open(nugget_file, 'r').convert('RGBA').resize((500, 500), resample=0)
    dipped = []
    if sauce1 == None:
        background_file = f'{nugget_base_path}/Nugget_{nid}/{nid}-background.png'
        for f in range(250):
            frame = Image.open(background_file).convert("RGBA").resize((500, 500), resample=0)
            if sauce2 == 'Glitch Sauce' or sauce2 == 'Unsig Sauce':
                frame.paste(nugget_frames[f], (0,0), nug)
            else:
                frame.paste(nugget_frames[f], (0,0), nugget_frames[f])
            dipped.append(frame)
    else:
        for i in range(250):
            background_frame = background_frames[i]
            nug_frame = nugget_frames[i]
            if sauce2 == 'Glitch Sauce' or sauce2 == 'Unsig Sauce':
                background_frame.paste(nug_frame, (0, 0), nug)
            else:
                background_frame.paste(nug_frame, (0, 0), nug_frame)
            dipped.append(background_frame)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    gif_file = f'{output_dir}/{nid}-1.gif' if sauce2 is None else f'{output_dir}/{nid}-2.gif'
    dipped[0].save(gif_file, format='GIF', append_images=dipped[1:], save_all=True, duration=20, loop=0,
                   minimize_size=True)
    png_file = f'{output_dir}/{nid}-dipped-1.png' if sauce2 is None else f'{output_dir}/{nid}-dipped-2.png'
    dipped[124].save(png_file, format='PNG')

    ffmpeg_global_arguments = ['-y', '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf',
                               '"scale=trunc(iw/2)*2:trunc(ih/2)*2"']
    stream = ffmpeg.input(gif_file)
    mp4_file = f'{output_dir}/{nid}-dip-1.mp4' if sauce2 is None else f'{output_dir}/{nid}-dip-2.mp4'
    stream = ffmpeg.output(stream, mp4_file, pix_fmt='yuv420p', movflags='+faststart')
    stream = stream.global_args(*ffmpeg_global_arguments)
    stream.run()
    os.remove(gif_file)

    if used_sauce1 == 'Degen Dip':
        sauce1 += '*'
    if used_sauce2 == 'Degen Dip':
        sauce2 += '*'
    return (png_file, mp4_file, sauce1, sauce2)


# root dir holding the nugget folders
#print(dip('/Users/ben/Desktop/', 0, 'Degen Dip', 'Degen Dip', 'dipped_nuggets'))
#dip('/Users/ben/Desktop/', 0, None, 'honey_mustard', 'dipped_nuggets')
