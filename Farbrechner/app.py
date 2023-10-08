from flask import Flask, request, render_template
import cv2
import numpy as np
from scipy.spatial import distance

COLORS = {
    'rot': (255, 0, 0),
    'grün': (0, 255, 0),
    'blau': (0, 0, 255),
    'gelb': (255, 255, 0),
    'orange': (255, 165, 0),
    'lila': (128, 0, 128),
    'braun': (165, 42, 42),
    'rosa': (255, 192, 203),
}

app = Flask(name)

def parse_colors(colors_in_liters):
    result = {}
    for color_liters in colors_in_liters.split(';'):
        color_name, liters = color_liters.split(':')
        color = COLORS[color_name.lower()]
        result[color] = float(liters)
    return result

def find_nearest_color(color):
    colors = np.array(list(COLORS.values()))
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    index_of_nearest_color = np.argmin(distances)
    return list(COLORS.keys())[index_of_nearest_color]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        width = float(request.form.get('width'))
        height = float(request.form.get('height'))
        colors_in_liters = parse_colors(request.form.get('colors'))  # Format: "rot:2;blau:3"
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img_height, img_width, _ = img.shape
        total_area = width * height
        pixel_area = total_area / (img_height * img_width)
        colors, count = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True)
        color_areas = {}
        for color, cnt in zip(colors, count):
            if tuple(color) not in COLORS.values():
                color_name = find_nearest_color(color)
                color_areas[color_name] = color_areas.get(color_name, 0) + cnt*pixel_area
            else:
                color_areas[tuple(color)] = cnt*pixel_area
        missing_colors = {color: area - colors_in_liters.get(color, 0) for color, area in color_areas.items() if area > colors_in_liters.get(color, 0)}
        return render_template('upload.html', missing_colors=missing_colors)
    return render_template('upload.html')

if name == 'main':
    app.run(debug=True)