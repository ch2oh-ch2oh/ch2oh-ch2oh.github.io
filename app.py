from flask import Flask, request, jsonify, send_from_directory
import heapq
from svgpathtools import svg2paths
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


# def reconstruct_path(came_from, start, goal):
#     path = [goal]
#     current = goal
#     while current != start:
#         current = came_from[current]
#         path.append(current)
#     path.reverse()
#     return path
#
#
from svgpathtools import Line


def point_inside_polygon(x, y, segments):
    point = complex(x, y)
    crossings = 0
    n = len(segments)

    for i in range(n):
        segment = segments[i]
        if isinstance(segment, Line):
            p1 = segment.start
            p2 = segment.end

            if y > min(p1.imag, p2.imag):
                if y <= max(p1.imag, p2.imag):
                    if x <= max(p1.real, p2.real):
                        if p1.imag != p2.imag:
                            xinters = (y - p1.imag) * (p2.real - p1.real) / (p2.imag - p1.imag) + p1.real
                        if p1.real == p2.real or x <= xinters:
                            crossings += 1

    return crossings % 2 == 1


# def get_svg_neighbors(point, polygons, step=1):
#     x, y = point
#     neighbors = [
#         (x + step, y),
#         (x - step, y),
#         (x, y + step),
#         (x, y - step),
#     ]
#
#     def is_valid_neighbor(neighbor):
#         return not any(point_inside_polygon(neighbor[0], neighbor[1], polygon) for polygon in polygons)
#
#     return [neighbor for neighbor in neighbors if is_valid_neighbor(neighbor)]
#
#
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

#
# def heuristic(a, b):
#     return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def build_grid(paths):
    """Builds a grid of the specified width and height.

    Each cell in the grid is set to True if it is inside a path, and False otherwise.
    """
    grid = [[False] * SVG_CANVAS_WIDTH for _ in range(SVG_CANVAS_HEIGHT)]
    for y in range(SVG_CANVAS_HEIGHT):
        for x in range(SVG_CANVAS_WIDTH):
            for path in paths:
                if point_inside_polygon(x, y, path):
                    grid[y][x] = True
                    break
    return grid


def find_path(start, end, paths):
    start = tuple(map(int, start))
    end = tuple(map(int, end))

    grid_data = build_grid(paths)

    grid = Grid(matrix=grid_data)

    start_node = grid.node(start[0], start[1])
    end_node = grid.node(end[0], end[1])

    finder = AStarFinder()
    path, _ = finder.find_path(start_node, end_node, grid)

    return path

def dijkstra(grid, start, end):
    queue = PriorityQueue()
    queue.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not queue.empty():
        current = queue.get()

        if current == end:
            break

        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                queue.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far



app = Flask(__name__, static_url_path='', static_folder='static')


# Импортируйте SVG файл при инициализации сервера
# Update the import_svg function to create polygons from paths
def import_svg(file_path):
    paths, attributes = svg2paths(file_path)
    return paths


file_path = "static/level1.svg"
paths = import_svg(file_path)


@app.route('/')
def home():
    return app.send_static_file('index.html')

SVG_CANVAS_WIDTH = 1920  # replace with actual width
SVG_CANVAS_HEIGHT = 1080  # replace with actual height


@app.route('/find_path', methods=['POST'])
def find_path_endpoint():
    start = request.json['start']
    end = request.json['end']

    print(f"Start: {start}")
    print(f"End: {end}")

    if not (0 <= start[0] < SVG_CANVAS_WIDTH and 0 <= start[1] < SVG_CANVAS_HEIGHT):
        return jsonify({'error': 'Point is out of range'}), 400

    # path = find_path(start, end, paths)
    start = tuple(map(int, start))
    end = tuple(map(int, end))
    path, _ = dijkstra(start, end, paths)

    path = [[float(coord) for coord in point] for point in path]

    return jsonify({'path': path}), 200



@app.route('/path/<path:filename>')
def serve_path(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)
