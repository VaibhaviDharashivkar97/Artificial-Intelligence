import math
import sys
from warnings import warn
from PIL import Image
from Node import Node
import heapq

imgpath = sys.argv[1]
elevationPath = sys.argv[2]
destinationPath = sys.argv[3]
season = sys.argv[4]
output_img_name = sys.argv[5]

image = Image.open(imgpath, 'r')
x, y = image.size
pix = image.load()

Dictionary = {(248, 148, 18, 255): 15, (255, 192, 0, 255): 5, (255, 255, 255, 255): 10, (2, 208, 60, 255): 8,
              (2, 136, 40, 255): 4, (5, 73, 24, 255): 2,
              (0, 0, 255, 255): 1, (71, 51, 3, 255): 20, (0, 0, 0, 255): 22, (82, 219, 255, 255): 3}
Dictionary_fall = {(248, 148, 18, 255): 10, (255, 192, 0, 255): 4, (255, 255, 255, 255): 3, (2, 208, 60, 255): 5,
                   (2, 136, 40, 255): 4, (5, 73, 24, 255): 2,
                   (0, 0, 255, 255): 1, (71, 51, 3, 255): 16, (0, 0, 0, 255): 15}
path = []


def elevation_path():
    ele_file = open(elevationPath, 'r')
    elevation = []
    for line in ele_file:
        temp = line.strip().split()
        temp1 = []
        for i in range(len(temp) - 5):
            temp1.append(temp[i])
        elevation.append(temp1)
    return [[row[i] for row in elevation] for i in range(len(elevation[0]))]


def goal_points_file():
    path_file = open(destinationPath, 'r')
    goal_points = []
    for line in path_file:
        goal_points.extend(line.strip().split())
    for i in range(len(goal_points)):
        goal_points[i] = int(goal_points[i])
    return goal_points


def node_declaration(elevation_transpose):
    node_list = []
    for row in range(x):
        t = []
        for col in range(y):
            t.append(Node(row, col, pix[row, col], elevation_transpose[row][col]))
        node_list.append(t)
    return node_list


def node_declaration_winter(node):
    queue = []

    for i in range(7):
        for row in range(1,x - 1):
            for col in range(1, y - 1):
                if pix[row,col]==(0, 0, 255, 255):
                    if pix[row,col+1] != (0,0,255,255) :
                        queue.append(node[row][col])
                    elif pix[row+1, col] != (0,0,255,255) :
                        queue.append(node[row][col])
                    elif pix[row-1, col] != (0,0,255,255) :
                        queue.append(node[row][col])
                    elif pix[row, col-1] != (0,0,255,255):
                        queue.append(node[row][ col])
                    elif pix[row, col+1] != (0,0,255,255):
                        queue.append(node[row][ col])
                    elif pix[row+1, col+1] != (0,0,255,255) :
                        queue.append(node[row][ col])
                    elif pix[row-1,col-1] != (0,0,255,255):
                        queue.append(node[row][col])


                    else:
                        pix[row,col] = pix[row,col]
                else:
                    pix[row,col] = pix[row,col]

        for n in queue:
            pix[n.x,n.y] = (82, 219, 255, 255)
            n.rgba = (82, 219, 255, 255)


def traverse(goal_points, node_list):
    for i in range(3, len(goal_points), 2):
        start_x = goal_points[i - 3]
        start_y = goal_points[i - 2]
        goal_x = goal_points[i - 1]
        goal_y = goal_points[i]
        start = node_list[start_x][start_y]
        goal = node_list[goal_x][goal_y]
        start.f = 0
        start.g = 0
        start.h = 0
        start.parent = None
        if start.rgba == (205, 0, 101, 255) or goal.rgba == (205, 0, 101, 255):
            continue
        current = searching(start, goal, node_list)
        print(current.parent.m)
        while current is not None:
            path.append(current)
            current = current.parent

    new_img = Image.new("RGBA", (x, y))
    new_pix = new_img.load()
    for ro in range(x):
        for column in range(y):
            if node_list[ro][column] in path:
                new_pix[ro, column] = (255, 0, 0, 255)
                for ink in range(1, len(goal_points), 2):
                    if ro == goal_points[ink - 1] and column == goal_points[ink]:
                        new_pix[ro, column] = (0, 0, 0, 255)
            else:
                new_pix[ro, column] = pix[ro, column]
    new_img = new_img.save(output_img_name)


def searching(start, goal, node_list):
    queue = []
    visited = []

    heapq.heapify(queue)
    heapq.heappush(queue, start)

    while len(queue) > 0:
        current_node = heapq.heappop(queue)
        visited.append(current_node)

        if current_node == goal:
            return current_node

        neighbours = []

        xEast = current_node.x + 1
        xWest = current_node.x - 1
        ySouth = current_node.y + 1
        yNorth = current_node.y - 1

        if xEast <= x and pix[xEast, current_node.y] != (205, 0, 101, 255):
            # if node_list[xEast][current_node.y].parent is None:
            #     node_list[xEast][current_node.y].parent = current_node
            neighbours.append(node_list[xEast][current_node.y])
        if xWest >= 0 and pix[xWest, current_node.y] != (205, 0, 101, 255):
            # if node_list[xWest][current_node.y].parent is None:
            #     node_list[xWest][current_node.y].parent = current_node
            neighbours.append(node_list[xWest][current_node.y])
        if ySouth <= y and pix[current_node.x, ySouth] != (205, 0, 101, 255):
            # if node_list[current_node.x][ySouth].parent is None:
            #     node_list[current_node.x][ySouth].parent = current_node
            neighbours.append(node_list[current_node.x][ySouth])
        if yNorth >= 0 and pix[current_node.x, yNorth] != (205, 0, 101, 255):
            # if node_list[current_node.x][yNorth].parent is None:
            #     node_list[current_node.x][yNorth].parent = current_node
            neighbours.append(node_list[current_node.x][yNorth])
        if xEast <= x and ySouth <= y and pix[xEast, ySouth] != (205, 0, 101, 255):
            # if node_list[xEast][ySouth].parent is None:
            #     node_list[xEast][ySouth].parent = current_node
            neighbours.append(node_list[xEast][ySouth])
        if xWest >= 0 and ySouth <= y and pix[xWest, ySouth] != (205, 0, 101, 255):
            # if node_list[xWest][ySouth].parent is None:
            #     node_list[xWest][ySouth].parent = current_node
            neighbours.append(node_list[xWest][ySouth])
        if xWest >= 0 and yNorth >= 0 and pix[xWest, yNorth] != (205, 0, 101, 255):
            # if node_list[xWest][yNorth] is None:
            #     node_list[xWest][yNorth].parent = current_node
            neighbours.append(node_list[xWest][yNorth])
        if xEast <= x and yNorth >= 0 and pix[xEast, yNorth] != (205, 0, 101, 255):
            # if node_list[xEast][yNorth].parent is None:
            #     node_list[xEast][yNorth].parent = current_node
            neighbours.append(node_list[xEast][yNorth])

        for neighbour in neighbours:
            if current_node.parent is not None:
                if neighbour not in queue and neighbour not in visited and current_node.parent is not neighbour:
                    neighbour.parent = current_node
            if current_node.parent is None:
                neighbour.parent = current_node
            if len([visited_neighbour for visited_neighbour in visited if
                    visited_neighbour.x == neighbour.x and visited_neighbour.y == neighbour.y]) > 0:
                continue
            # if neighbour not in queue and neighbour not in visited:
            #     neighbour.parent=current_node
            if neighbour.x == goal.x and neighbour.y == goal.y:
                neighbour.g = 0
                neighbour.h = 0
                neighbour.f = 0
            else:
                neighbour.g, neighbour.m = g_function(neighbour, current_node)
                neighbour.h = h_function(neighbour, goal)
                neighbour.f = neighbour.g + neighbour.h

            if len([queued_node for queued_node in queue if
                    neighbour.x == queued_node.x and neighbour.y == queued_node.y and neighbour.g > queued_node.g]) > 0:
                # neighbour.parent = current_node
                continue
            # neighbour.parent = current_node
            heapq.heappush(queue, neighbour)
    warn("Couldn't get a path to destination")
    return None


def g_function(this_node, parent_node):
    elevation_angle = abs(float(this_node.elevation) - float(parent_node.elevation))
    distance = 0
    if this_node.y == parent_node.y and this_node.x != parent_node.x:
        distance = 10.29
    elif this_node.x == parent_node.x and this_node.y != parent_node.y:
        distance = 7.55
    else:
        distance = 12.76
    total_distance = parent_node.g + distance
    travelling_miles = parent_node.m + distance
    if elevation_angle == 0:
        if season == 'fall':
            return total_distance / ((Dictionary_fall.get(this_node.rgba) + Dictionary_fall.get(
                parent_node.rgba)) / 2), travelling_miles
        else:
            return total_distance / (
                    (Dictionary.get(this_node.rgba) + Dictionary.get(parent_node.rgba)) / 2), travelling_miles
    else:
        if season == 'fall':
            try:
                speed = total_distance / (
                        (Dictionary_fall.get(this_node.rgba) + Dictionary_fall.get(
                            parent_node.rgba)) / 2) - 2, travelling_miles
                return speed
            except ZeroDivisionError:
                return total_distance / (Dictionary_fall.get(this_node.rgba) / 2) - elevation_angle, travelling_miles
        else:
            try:
                speed = total_distance / (
                        (Dictionary.get(this_node.rgba) + Dictionary.get(parent_node.rgba)) / 2) - 2, travelling_miles
                return speed
            except ZeroDivisionError:
                return total_distance / (Dictionary.get(this_node.rgba) / 2) - elevation_angle, travelling_miles


def h_function(this_node, end_node):
    total_distance = math.sqrt(
        (10.29 ** 2 * (this_node.x - end_node.x) ** 2) + (7.55 ** 2 * (this_node.y - end_node.y) ** 2))
    return total_distance / 10


if __name__ == '__main__':
    elevation_transpose = elevation_path()
    goal_points = goal_points_file()
    node = node_declaration(elevation_transpose)
    if season == "winter":
        node_declaration_winter(node)
    traverse(goal_points, node)
