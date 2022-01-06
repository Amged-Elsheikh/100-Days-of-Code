import turtle as t
import random


def move(turtle: t, speed=list(range(0, 11))):
    turtle.forward(random.choice(speed))


if __name__ == '__main__':
    race = True
    screen = t.Screen()
    width = 500
    height = 400
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    y_positions = list(range(-height//2+25, height//2, height//len(colors)))
    screen.setup(width=width, height=height)
    user_bet = screen.textinput(
        "Make your bet", "Which turtle will win the race? enter a color:").lower()
    TURTLES = {}
    for i, color in enumerate(colors):
        tim = t.Turtle(shape="turtle")
        tim.color(color)
        tim.penup()
        tim.goto(x=-width/2+20, y=y_positions[i])
        tim.speed("fastest")
        TURTLES[color] = tim

    while race:
        for color in TURTLES.keys():
            move(TURTLES[color])
            x_pos, _ = TURTLES[color].pos()
            if x_pos >= (width/2-40):
                race = False
                winner = color
    if user_bet == winner:
        print(f"You bet on the winner turtle, {winner}")
    else:
        print(f"You bet on {user_bet}, winner is {winner}")
    screen.exitonclick()
