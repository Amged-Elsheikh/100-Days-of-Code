import random
import turtle as t
import random
import colorgram

def random_color(object: t.Turtle):
    object.color(random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255))


def draw_square(object: t.Turtle, lenght: float):
    for _ in range(4):
        object.forward(lenght)
        object.right(90)


def draw_dashline(object: t.Turtle, lenght: float, number_og_gaps: float):
    for _ in range(number_og_gaps//2):
        object.pendown()
        object.forward(lenght/number_og_gaps)
        object.penup()
        object.forward(lenght/number_og_gaps)


def draw_shapes(object: t.Turtle, lenght: float, number_edges: int):
    angle = 360
    random_color(object)
    if angle % number_edges == 0:
        while angle != 0:
            object.forward(lenght)
            object.right(360//number_edges)
            angle -= 360//number_edges


def random_walk(object: t.Turtle, number_of_steps: int, lenght=50.0):
    object.pensize(10)
    for _ in range(number_of_steps):
        random_color(object)
        direction = random.choice([0, 90, 180, 270])
        object.setheading(direction)
        object.forward(lenght)


def draw_spirograpgh(object: t.Turtle, radius=50, size_of_gap=5):
    for _ in range(360//size_of_gap):
        random_color(object)
        object.circle(radius)
        object.setheading(object.heading() + size_of_gap)

# t.colormode(255)
# joe = t.Turtle()  # Define a turtel
# joe.shape("turtle")
# joe.speed("fastest")

# # draw_square(joe, 100)
# # draw_dashline(joe, 100, 30)
# # for i in range(3, 30):
# #     draw_shapes(joe, 100, i)
# # random_walk(joe, 1000)
# # draw_spirograpgh(joe,  radius=100, size_of_gap=2)
# screen = t.Screen()  # define the screen object
# screen.exitonclick()
