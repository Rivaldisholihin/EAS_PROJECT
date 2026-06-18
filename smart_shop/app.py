from flask import Flask, render_template, request, jsonify, Response
from graph import supermarket_graph, categories, get_coordinates, coordinates
import itertools, heapq, math
import random
import time
import json
from datetime import datetime
import threading

app = Flask(__name__)

def heuristic(a, b):
    x1, y1 = get_coordinates(a)
    x2, y2 = get_coordinates(b)
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star(graph, start, goal):
    queue = [(heuristic(start, goal), 0, start, [start])]
    visited = set()

    while queue:
        _, cost, current, path = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, cost

        for neighbor, dist in graph.get(current, []):
            if neighbor not in visited:
                new_cost = cost + dist
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(queue, (priority, new_cost, neighbor, path + [neighbor]))

    return None, float('inf')

def dijkstra(graph, start, goal):
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        cost, current, path = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, cost

        for neighbor, dist in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + dist, neighbor, path + [neighbor]))

    return None, float('inf')

def bfs(graph, start, goal):
    queue = [(start, [start], 0)]
    visited = set()

    while queue:
        current, path, total_cost = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, total_cost

        for neighbor, dist in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], total_cost + dist))

    return None, float('inf')

def dfs(graph, start, goal):
    stack = [(start, [start], 0)]
    visited = set()

    while stack:
        current, path, total_cost = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path, total_cost

        for neighbor, dist in graph.get(current, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], total_cost + dist))
    return None, float('inf')

node_crowded = {node: random.randint(0, 8) for node in supermarket_graph.keys()}

def update_crowded_status():
    while True:
        for node in node_crowded:
            node_crowded[node] = random.randint(0, 8)
        time.sleep(30)

thread = threading.Thread(target=update_crowded_status)
thread.daemon = True
thread.start()


def wait_until_not_crowded(node, threshold=7):
    if node_crowded.get(node, 0) >= threshold:
        return {
            "waiting": True,
            "node": node,
            "crowded": node_crowded[node]
        }
    return {"waiting": False}


def find_optimal_route(selected, algorithm):

    def run_algo(start, goal):
        if algorithm == "a_star": return a_star(supermarket_graph, start, goal)
        if algorithm == "dijkstra": return dijkstra(supermarket_graph, start, goal)
        if algorithm == "bfs": return bfs(supermarket_graph, start, goal)
        if algorithm == "dfs": return dfs(supermarket_graph, start, goal)

    start, end = "Pintu Masuk", "Kasir"
    min_cost, best = float('inf'), None

    for perm in itertools.permutations(selected):
        total_cost = 0
        path = [start]

        wait_status = wait_until_not_crowded(perm[0])
        if wait_status["waiting"]:
            return wait_status

        seg, cost = run_algo(start, perm[0])
        if not seg: continue
        path.extend(seg[1:])
        total_cost += cost

        valid = True
        for i in range(len(perm) - 1):

            wait_status = wait_until_not_crowded(perm[i+1])
            if wait_status["waiting"]:
                return wait_status

            seg, cost = run_algo(perm[i], perm[i+1])
            if not seg:
                valid = False
                break
            path.extend(seg[1:])
            total_cost += cost

        if not valid:
            continue

        wait_status = wait_until_not_crowded(end)
        if wait_status["waiting"]:
            return wait_status

        seg, cost = run_algo(perm[-1], end)
        if not seg: continue
        path.extend(seg[1:])
        total_cost += cost

        if total_cost < min_cost:
            min_cost = total_cost
            best = path

    return {
        "waiting": False,
        "route": best,
        "distance": round(min_cost, 1),
        "steps": best
    }


@app.route("/")
def index():
    return render_template(
        "route_main.html",
        categories=categories,
        coords=coordinates,
        graph=supermarket_graph
    )

@app.route("/home") 
def home():
    return render_template("base.html")

@app.route("/compute", methods=["POST"])
def compute():
    selected = request.json.get("categories", [])
    algorithm = request.json.get("algorithm")
    result = find_optimal_route(selected, algorithm)
    return jsonify(result)

@app.route("/sse")
def sse():
    def event_stream():
        while True:
            yield f"data: {json.dumps(node_crowded)}\n\n"
            time.sleep(5)
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
