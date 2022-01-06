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
        new_path = path.join(cwd, "Day 18 Turtle")
        chdir(new_path)


def extract_colors(filename: str, number_of_colors: int):
    colors = colorgram.extract(filename, number_of_colors)
    rgb_colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
    return list(filter(lambda x: sum(x) <= 230*3, rgb_colors))


def draw_h_dots(rgb_colors, dot_size, gap, steps):
    for i in range(steps):
        t.dot(dot_size, random.choice(rgb_colors))
        # t.penup()
        if i != steps-1:
            t.forward(gap)


if __name__ == '__main__':
    dot_size = 40
    gap = 50
    # To get good plot make sure v_steps==h_steps
    h_steps = 20
    v_steps = 10
    width=h_steps*gap
    height=v_steps*gap

    t.colormode(255)
    t.penup()
    t.speed("fastest")
    # t.hideturtle()
    screen = t.Screen()  # define the screen object
    screen.setup(width+dot_size/2, height+dot_size/2)
    change_directory()
    rgb_colors = extract_colors('Economy-Mince.jpg', 40)
    t.goto(x=(-width+gap)/2, y=(-height+gap)/2)

    start_x, current_y = t.pos()
    for i in range(v_steps):
        draw_h_dots(rgb_colors, dot_size, gap, h_steps)
        current_y += gap
        if i != v_steps-1:
            t.goto(start_x, current_y)

    screen.exitonclick()
