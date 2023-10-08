from PIL import Image
import numpy as np

# Definiere die Farben
colors = {
    'rot': [255, 0, 0],
    'gelb': [255, 255, 0],
    'schwarz': [0, 0, 0],
    'grün': [0, 128, 0],
    'lila': [128, 0, 128],
    'rosa': [255, 192, 203],
    'orange': [255, 165, 0],
    'blau': [0, 0, 255]
}

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in colors:
        cr, cg, cb = colors[color]
        color_diff = abs(r - cr) + abs(g - cg) + abs(b - cb)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def analyze_image(image_path):
    # Lade das Bild
    img = Image.open(image_path)
    data = np.array(img)

    # Analysiere das Bild
    color_counts = {color: 0 for color in colors}
    for row in data:
        for pixel in row:
            color_counts[closest_color(pixel[:3])] += 1

    # Zeige die Ergebnisse an
    total = sum(color_counts.values())
    for color in color_counts:
        percentage = (color_counts[color] / total) * 100
        print(f'{color}: {percentage:.2f}%')

# Verwende die Funktion
analyze_image('path_to_your_image.png')
