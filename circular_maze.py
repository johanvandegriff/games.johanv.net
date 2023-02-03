#!/usr/bin/env python3
import math, random
from PIL import Image, ImageDraw

def generate_maze(
    num_levels = 16, #number of concentric circles in the maze
    big_level_every = 4, #big levels will have fewer gaps and be drawn with a thicker line
    img_size = 2000, #number of pixels for the image's width and height
    max_arc_length = .8, #max arc length of a segment before it needs to split into 2
    max_gaps_ratio = .25, #the max proportion of gaps compared to total segments
    narrow_line_width = .002, #how thick to make a normal level's lines
    wide_line_width = .007, #how thick to make a big level's lines
    foreground_color = 'black', #color of the maze's lines
    background_color = '#FFF0', #color of the image background
    debug = False, #should it show the missing gridlines in light blue
):
    img = Image.new('RGBA', (img_size, img_size), background_color)
    draw = ImageDraw.Draw(img)

    def draw_arc(draw, img_size, radius, start_degrees, end_degrees, line_width=narrow_line_width, color=foreground_color):
        dist_from_edge = round(img_size/2 - radius)
        start_degrees, end_degrees = 360-end_degrees, 360-start_degrees
        draw.arc([(dist_from_edge, dist_from_edge), (img_size-dist_from_edge, img_size-dist_from_edge)], start=start_degrees, end=end_degrees, fill=color, width=round(line_width*img_size))

    def polar_to_xy(img_size, radius, angle_degrees):
        return img_size/2+radius*math.cos(-angle_degrees*math.pi/180), img_size/2+radius*math.sin(-angle_degrees*math.pi/180)

    def draw_ray(draw, img_size, radius1, radius2, angle_degrees, line_width=narrow_line_width, color=foreground_color):
        push_inward = .001*img_size #tweak the radii slightly inward to make them be centered in the arc
        prev_x, prev_y = polar_to_xy(img_size, radius1-push_inward, angle_degrees)
        x, y = polar_to_xy(img_size, radius2-push_inward, angle_degrees)
        draw.line((prev_x,prev_y, x,y), fill=color, width=round(line_width*img_size))

    def get_level_radius(img_size, num_levels, level_idx):
        return round(img_size/2/num_levels*(.5+level_idx))



    MAZE_RAYS = 0
    MAZE_ARCS = 1
    maze = []

    prev_radius = 0
    num_segments = 4
    for level_idx in range(num_levels):
        radius = get_level_radius(img_size, num_levels, level_idx)

        #old method of automatically determining number of segments, works except they don't line up with the previous
        # segment_degrees = img_size*2/radius
        # if level_idx == 0:
        #     segment_degrees = img_size/radius
        # num_segments = round(360/segment_degrees)

        segment_length = 2*math.pi*radius/num_segments
        # if level_idx % 4 == 0:
        if segment_length > img_size*max_arc_length/num_levels:
            num_segments *= 2

        maze.append([[],[]])

        for cell_idx in range(num_segments):
            maze[level_idx][MAZE_RAYS].append(0)
            maze[level_idx][MAZE_ARCS].append(1)


    # maze = [
    #     # r,t,l,b
    #     [[0,0,0,0], #rays
    #   #tr,tl,bl,br
    #     [0,1,1,1]], #arcs
    #     [[1,1,1,1,1,1,1,1], #rays
    #     [1,1,1,1,1,1,1,1]], #arcs
    #     [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    #     [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    #     [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    #     [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    #     [[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    #     [[0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #rays
    #     [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], #arcs
    # ]

    def get_neighbors(maze, node):
        neighbors = []
        if node == 'END': #special case, mostly node is a tuple
            prev_level_idx = len(maze)-1
            for cell_idx in range(len(maze[prev_level_idx][MAZE_ARCS])):
                if not maze[prev_level_idx][MAZE_ARCS][cell_idx]:
                    neighbors.append((prev_level_idx, cell_idx))
            return neighbors
        level_idx, cell_idx = node

        level_num_cells = len(maze[level_idx][MAZE_RAYS])
        prev_level_idx = level_idx-1
        next_level_idx = level_idx+1
        prev_cell_idx = (cell_idx-1) % level_num_cells
        next_cell_idx = (cell_idx+1) % level_num_cells

        if not maze[level_idx][MAZE_RAYS][cell_idx]:
            neighbors.append((level_idx, prev_cell_idx))
        if not maze[level_idx][MAZE_RAYS][next_cell_idx]:
            neighbors.append((level_idx, next_cell_idx))
        if not maze[level_idx][MAZE_ARCS][cell_idx]:
            if next_level_idx == len(maze):
                neighbors.append('END')
            else:
                next_level_num_cells = len(maze[next_level_idx][MAZE_RAYS])
                if next_level_num_cells == level_num_cells:
                    neighbors.append((next_level_idx, cell_idx))
                elif next_level_num_cells == level_num_cells * 2:
                    neighbors.append((next_level_idx, cell_idx*2))
                    neighbors.append((next_level_idx, cell_idx*2+1))
                else:
                    raise Exception(f'expected {level_num_cells * 2} cells on level {next_level_idx} but got {next_level_num_cells}')
        if prev_level_idx >= 0:
            prev_level_num_cells = len(maze[prev_level_idx][MAZE_RAYS])
            if prev_level_num_cells == level_num_cells:
                if not maze[prev_level_idx][MAZE_ARCS][cell_idx]:
                    neighbors.append((prev_level_idx, cell_idx))
            elif prev_level_num_cells == int(level_num_cells / 2):
                if not maze[prev_level_idx][MAZE_ARCS][int(cell_idx/2)]:
                    neighbors.append((prev_level_idx, int(cell_idx/2)))
            else:
                raise Exception(f'expected {int(level_num_cells / 2)} cells on level {next_level_idx} but got {next_level_num_cells}')
        
        return neighbors


    for level_idx, level in enumerate(maze):
        rays = level[MAZE_RAYS]
        arcs = level[MAZE_ARCS]

        is_big_level = (level_idx+1)/big_level_every == int((level_idx+1)/big_level_every)
        if is_big_level:
            max_gaps = round(len(arcs)*max_gaps_ratio)
            num_gaps = random.randint(1, max(1, max_gaps))
        else:
            max_gaps = round(len(arcs)*max_gaps_ratio)
            num_gaps = random.randint(3, max(3, max_gaps))

        # num_gaps = num_gaps * 2 - 1 #always odd number

        for i in range(len(rays)):
            rays[i] = 0 #start with no sub-divisions on the level
            arcs[i] = 1 #start with no gaps on the level
        if level_idx == 0: #level 0 always has 4 arcs
            num_gaps = 1
            num_gaps = random.randint(-1,2)
            if num_gaps < 1:
                num_gaps = 1

        # if level_idx == len(maze)-1:
        #     num_gaps = 1

        # print(max_gaps, num_gaps)

        indexes = [i for i in range(len(arcs))]
        while num_gaps > 0:
            if len(indexes) == 0:
                break #abort if there are no places left to put gaps
                # raise Exception("not enough options for gaps left")
            gap_idx = random.choice(indexes)
            indexes.remove(gap_idx)

            if is_big_level:
                dist = max(2, round(len(arcs) / 5)) #make sure the gaps on big levels are further away
            else:
                dist = 1

            for i in range(-dist, dist+1):
                #make sure there are no adjacent gaps:
                try:
                    indexes.remove((gap_idx-i) % len(arcs))
                except:
                    pass
            arcs[gap_idx] = 0
            num_gaps -= 1


    def validate_maze(maze):
        connected_nodes = [(0,0)] #0,0 is the top-right corner of the center circle
        #the 1st coord is the level, the 2nd coord is the cell, starting from the cell sitting on the right flat line

        connected_node_idx = 0
        while True:
            curr_node = connected_nodes[connected_node_idx]
            for node in get_neighbors(maze, curr_node):
                if not node in connected_nodes:
                    connected_nodes.append(node)
            connected_node_idx += 1
            if connected_node_idx >= len(connected_nodes):
                break

        #make sure all nodes are reachable by comparing the total number of reachable nodes with the expected number
        return len(connected_nodes) == sum(map(lambda l: len(l[MAZE_RAYS]), maze))+1 #length of maze plus 1 for the 'END' node

    assert validate_maze(maze)

    rays_possible_to_add = []
    for level_idx in range(1, len(maze)):
        for ray_idx in range(0, len(maze[level_idx][MAZE_RAYS])):
            rays_possible_to_add.append((level_idx, ray_idx))

    #try each ray once but in a random order
    while len(rays_possible_to_add) > 0:
        ray = random.choice(rays_possible_to_add)
        rays_possible_to_add.remove(ray)
        level_idx, ray_idx = ray
        if not maze[level_idx][MAZE_RAYS][ray_idx]:
            maze[level_idx][MAZE_RAYS][ray_idx] = 1
            if not validate_maze(maze):
                maze[level_idx][MAZE_RAYS][ray_idx] = 0

    prev_radius = 0
    num_segments = 4
    for level_idx in range(num_levels):
        radius = get_level_radius(img_size, num_levels, level_idx)

        is_big_level = (level_idx+1)/big_level_every == int((level_idx+1)/big_level_every)
        if is_big_level:
            arc_line_width = wide_line_width
        else:
            arc_line_width = narrow_line_width

        num_segments = len(maze[level_idx][MAZE_ARCS])
        segment_degrees = 360/num_segments

        for segment_idx in range(num_segments):
            # print(level_idx, segment_idx, end=' ')
            # print(maze[level_idx][MAZE_RAYS][segment_idx], maze[level_idx][MAZE_ARCS][segment_idx])
            # if (segment_idx+level_idx+3)/5 != int((segment_idx+level_idx+3)/5):
            if maze[level_idx][MAZE_RAYS][segment_idx]:
                draw_ray(draw, img_size, prev_radius, radius, segment_degrees * segment_idx)
            elif debug:
                draw_ray(draw, img_size, prev_radius, radius, segment_degrees * segment_idx, color='lightblue') #tmp
            # if (segment_idx+level_idx)/8 != int((segment_idx+level_idx)/8):
            if maze[level_idx][MAZE_ARCS][segment_idx]:
                draw_arc(draw, img_size, radius, segment_degrees*segment_idx, segment_degrees*(segment_idx+1), arc_line_width)
            elif debug:
                draw_arc(draw, img_size, radius, segment_degrees*segment_idx, segment_degrees*(segment_idx+1), arc_line_width, color='lightblue') #tmp
        
        prev_radius = radius

    # img.show()
    # img.save('test.png')
    return img
