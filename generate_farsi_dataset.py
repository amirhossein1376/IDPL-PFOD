import argparse
import csv
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


def load_fonts(font_dir, sizes):
    fonts = []
    for font_path in Path(font_dir).glob('**/*.ttf'):
        for size in sizes:
            try:
                fonts.append((font_path, size, ImageFont.truetype(str(font_path), size)))
            except OSError:
                # Skip fonts that PIL cannot load
                continue
    return fonts


def load_text_lines(text_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def create_plain_background(width, height):
    return Image.new('RGB', (width, height), 'white')


def create_noisy_background(width, height):
    image = create_plain_background(width, height)
    noise = np.random.randint(0, 50, (height, width, 3), dtype='uint8')
    noisy = Image.fromarray(np.clip(np.array(image) + noise, 0, 255).astype('uint8'))
    return noisy


def create_image_background(width, height, image_paths):
    path = random.choice(image_paths)
    bg = Image.open(path).convert('RGB')
    bg = bg.resize((width, height))
    return bg


def sine_distortion(img, amplitude=5, frequency=40):
    arr = np.array(img)
    height, width = arr.shape[:2]
    new_arr = np.zeros_like(arr)
    for y in range(height):
        shift = int(amplitude * np.sin(2 * np.pi * y / frequency))
        if shift > 0:
            new_arr[y, shift:] = arr[y, :-shift]
        elif shift < 0:
            new_arr[y, :shift] = arr[y, -shift:]
        else:
            new_arr[y] = arr[y]
    return Image.fromarray(new_arr)


def slant_distortion(img, factor=0.3):
    width, height = img.size
    m = (1, factor, 0, 0, 1, 0)
    return img.transform((width + int(height * abs(factor)), height), Image.AFFINE, m)


def generate_image(text, font, background_type, bg_images, distort_prob):
    width, height = 700, 50
    if background_type == 'plain':
        bg = create_plain_background(width, height)
    elif background_type == 'noise':
        bg = create_noisy_background(width, height)
    else:
        bg = create_image_background(width, height, bg_images)

    draw = ImageDraw.Draw(bg)
    w, h = draw.textsize(text, font=font)
    text_x = max((width - w) // 2, 0)
    text_y = max((height - h) // 2, 0)
    draw.text((text_x, text_y), text, font=font, fill='black')

    distort_type = 'none'
    rnd = random.random()
    if rnd < distort_prob:
        distortion = random.choice(['slant', 'sine'])
        if distortion == 'slant':
            bg = slant_distortion(bg)
        else:
            bg = sine_distortion(bg)
        distort_type = distortion
    if rnd < distort_prob / 2:
        bg = bg.filter(ImageFilter.GaussianBlur(radius=1))
        if distort_type == 'none':
            distort_type = 'blur'
        else:
            distort_type += '_blur'
    return bg, distort_type


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    fonts = load_fonts(args.font_dir, args.sizes)
    lines = load_text_lines(args.text_file)
    bg_images = list(Path(args.bg_dir).glob('*.jpg')) + list(Path(args.bg_dir).glob('*.png'))

    csv_path = Path(args.output_dir) / 'labels.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['filename', 'text', 'font', 'size', 'background', 'effect'])
        idx = 0
        for line in lines:
            for font_path, size, font in fonts:
                idx += 1
                bg_type = random.choices(['plain', 'noise', 'image'], weights=[0.5, 0.4, 0.1])[0]
                img, effect = generate_image(line, font, bg_type, bg_images, args.distort_prob)
                name = f"{idx:05d}.tif"
                img.save(Path(args.output_dir) / name)
                writer.writerow([name, line, font_path.name, size, bg_type, effect])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic Farsi text line images.')
    parser.add_argument('--font-dir', required=True, help='Directory with TTF font files')
    parser.add_argument('--bg-dir', required=True, help='Directory with background images')
    parser.add_argument('--text-file', required=True, help='File with lines of Farsi text')
    parser.add_argument('--output-dir', default='dataset', help='Where to save generated images')
    parser.add_argument('--sizes', nargs='+', type=int, default=[20, 22, 24, 26, 28, 30, 32], help='Font sizes to use')
    parser.add_argument('--distort-prob', type=float, default=0.1, help='Probability of applying distortion or blur')
    args = parser.parse_args()
    main(args)
