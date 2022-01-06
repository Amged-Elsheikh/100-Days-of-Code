"""Hirst Demien sample
"""
import random
import turtle as t
import random
import colorgram

def change_directory():
    from os import getcwd, path, chdir
    cwd = getcwd()
    if "day 18" not in cwd.lower():
        new_path = path.join(cwd,"Day 18 Turtle")
        chdir(new_path)

def extract_colors(filename: str, number_of_colors: int):
    colors = colorgram.extract(filename, number_of_colors)
    rgb_colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
    return list(filter(lambda x: sum(x)<=230*3, rgb_colors))

def draw_h_dots(rgb_colors, dot_size, gap, steps):
    for i in range(steps):
        t.dot(dot_size, random.choice(rgb_colors))
        # t.penup()
        if i!=steps-1:
            t.forward(gap)


if __name__ == '__main__':
    dot_size = 20
    gap = 50
    h_steps = 20
    v_steps = 20
    t.colormode(255)
    t.penup()
    t.speed("fastest")
    t.hideturtle()

    change_directory()
    rgb_colors = extract_colors('Economy-Mince.jpg', 40)
    
    ##### to check from where to start on your screen uncoment the next two line and comment rest of the code except the screen part. count the number of dots and update number_of_dots_to_start value.
    t.setheading(225)
    # draw_h_dots(rgb_colors,dot_size,gap,20)
    number_of_dots_to_start = 14
    t.forward(number_of_dots_to_start*gap)
    t.setheading(0)
    start_x, current_y = t.pos()
    for i in range(v_steps):
        draw_h_dots(rgb_colors, dot_size, gap, h_steps)
        current_y += gap
        if i!=v_steps-1:
            t.goto(start_x,current_y)
    
    screen = t.Screen()  # define the screen object
    screen.exitonclick()