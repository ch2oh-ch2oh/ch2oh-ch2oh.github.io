# from flask import Flask, request, jsonify, send_from_directory
# from PIL import Image
# import numpy as np
# from heapq import heappop, heappush
#
#
# def rasterize_png(file_path):
#     img = Image.open(file_path)
#     img_gray = img.convert("L")
#     img_data = np.array(img_gray)
#     return img_data
#
#
# def build_grid(image_data):
#     threshold = 200
#     grid = np.empty(image_data.shape, dtype=bool)
#     np.less(image_data, threshold, out=grid)  # change to np.less
#     return grid.tolist()
#
#
# def dijkstra(grid, start, end):
#     height = len(grid)
#     width = len(grid[0])
#     queue = [(0, start)]
#     paths = {start: []}
#     costs = {start: 0}
#
#     while queue:
#         cost, (x, y) = heappop(queue)
#         if (x, y) == end:
#             return paths[(x, y)]
#         for dx in [-1, 0, 1]:
#             for dy in [-1, 0, 1]:
#                 if dx == dy == 0:
#                     continue  # Skip the current cell
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < height and 0 <= ny < width and not grid[nx][ny]:
#                     new_cost = cost + 1
#                     if new_cost < costs.get((nx, ny), float('inf')):
#                         heappush(queue, (new_cost, (nx, ny)))
#                         paths[(nx, ny)] = paths[(x, y)] + [(nx, ny)]
#                         costs[(nx, ny)] = new_cost
#     return []
#
#
# app = Flask(__name__, static_url_path='', static_folder='static')
#
# file_path = "static/level1.png"
# image_data = rasterize_png(file_path)
# grid_data = build_grid(image_data)
#
#
# @app.route('/')
# def home():
#     return app.send_static_file('index.html')
#
#
# PNG_CANVAS_WIDTH = 550
# PNG_CANVAS_HEIGHT = 527
#
#
# @app.route('/find_path', methods=['POST'])
# def find_path_endpoint():
#     start = tuple(map(int, request.json['start']))
#     end = tuple(map(int, request.json['end']))
#
#     if not (0 <= start[0] < PNG_CANVAS_WIDTH and 0 <= start[1] < PNG_CANVAS_HEIGHT):
#         return jsonify({'error': 'Point is out of range'}), 400
#
#     path = dijkstra(grid_data, start, end)
#     path = [[float(coord) for coord in point] for point in path]
#
#     return jsonify({'path': path}), 200
#
#
# @app.route('/path/<path:filename>')
# def serve_path(filename):
#     return send_from_directory('static', filename)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
from heapq import heappop, heappush

def rasterize_png(file_path):
    img = Image.open(file_path)
    img_gray = img.convert("L")
    img_data = np.array(img_gray)
    return img_data


def build_grid(image_data):
    threshold = 200
    grid = np.empty(image_data.shape, dtype=bool)
    np.less(image_data, threshold, out=grid)
    return grid.tolist()


def dijkstra(grid, start, end):
    height = len(grid)
    width = len(grid[0])
    queue = [(0, start)]
    paths = {start: []}
    costs = {start: 0}

    while queue:
        cost, (x, y) = heappop(queue)
        if (x, y) == end:
            return paths[(x, y)]
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue  # Skip the current cell
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width and not grid[nx][ny]:
                    new_cost = cost + 1
                    if new_cost < costs.get((nx, ny), float('inf')):
                        heappush(queue, (new_cost, (nx, ny)))
                        paths[(nx, ny)] = paths[(x, y)] + [(nx, ny)]
                        costs[(nx, ny)] = new_cost
    return []


app = Flask(__name__, static_url_path='', static_folder='static')

file_path = "static/level1.png"
image_data = rasterize_png(file_path)
grid_data = build_grid(image_data)

# Hardcoded store entry and exit points
store_entry = (100, 100)  # Replace with actual coordinates
store_exit = (200, 200)  # Replace with actual coordinates

# Hardcoded parking spots identified by QR codes
spots = {
    'qr1': (0, 0),  # Replace 'qr1', 'qr2', etc. with actual QR code identifiers
    'qr2': (400, 400),  # Replace (x1, y1), (x2, y2), etc. with actual coordinates
    # Add more spots as needed
}

start = None
end = None


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/set_start', methods=['POST'])
def set_start_endpoint():
    global start
    qr_code = request.json['qr_code']
    if qr_code in spots:
        start = spots[qr_code]
        return jsonify({'message': 'Start point set'}), 200
    else:
        return jsonify({'error': 'Invalid QR code'}), 400


@app.route('/find_path', methods=['POST'])
def find_path_endpoint():
    global start, end
    from_store = request.json.get('from_store', False)
    if from_store:
        start = store_exit
        qr_code = request.json['qr_code']
        if qr_code in spots:
            end = spots[qr_code]
        else:
            return jsonify({'error': 'Invalid QR code'}), 400
    else:
        end = store_entry

    if not start or not end:
        return jsonify({'error': 'Start or end point not set'}), 400

    path = dijkstra(grid_data, start, end)
    path = [[float(coord) for coord in point] for point in path]

    start = None
    end = None

    return jsonify({'path': path}), 200

@app.route('/path/<path:filename>')
def serve_path(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)

