import turtle
import time
import random

WIDTH, HEIGHT = 700, 600
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'black', 'purple', 'pink', 'brown', 'cyan']


def get_number_of_racers():
    while True:
        racers = input('Enter the number of racers (2 - 10): ')
        if racers.isdigit():
            racers = int(racers)
            if 2 <= racers <= 10:
                return racers
        print('Invalid input. Enter a number between 2 and 10.')


def init_screen():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title('Turtle Racing!')
    screen.bgcolor('lightgray')
    return screen


def draw_finish_line():
    line = turtle.Turtle()
    line.speed(0)
    line.penup()
    line.goto(-WIDTH//2 + WIDTH - 50, -HEIGHT//2 + 20)
    line.pendown()
    line.pensize(5)
    line.color('black')
    line.left(90)
    for _ in range(20):
        line.forward(15)
        line.penup()
        line.forward(10)
        line.pendown()
    line.hideturtle()


def create_turtles(colors):
    turtles = []
    spacing_x = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.goto(-WIDTH//2 + (i + 1) * spacing_x, -HEIGHT//2 + 20)
        racer.pendown()
        turtles.append(racer)
    return turtles


def countdown():
    counter = turtle.Turtle()
    counter.hideturtle()
    counter.penup()
    counter.goto(0, 0)
    counter.color('black')
    counter.write('3', align='center', font=('Arial', 40, 'bold'))
    time.sleep(1)
    counter.clear()
    counter.write('2', align='center', font=('Arial', 40, 'bold'))
    time.sleep(1)
    counter.clear()
    counter.write('1', align='center', font=('Arial', 40, 'bold'))
    time.sleep(1)
    counter.clear()
    counter.write('GO!', align='center', font=('Arial', 40, 'bold'))
    time.sleep(0.5)
    counter.clear()


def race(turtles):
    while True:
        for racer in turtles:
            racer.forward(random.randint(1, 20))
            if racer.ycor() >= HEIGHT//2 - 30:
                return racer


def celebrate_winner(winner):
    winner.penup()
    winner.goto(0, HEIGHT//4)
    winner.write(f'The winner is {winner.color()[0]}!', align='center', font=('Arial', 30, 'bold'))
    winner.goto(0, HEIGHT//4 - 40)
    for _ in range(10):
        winner.forward(20)
        winner.backward(20)
    time.sleep(3)


def main():
    racers = get_number_of_racers()
    screen = init_screen()
    draw_finish_line()
    random.shuffle(COLORS)
    colors = COLORS[:racers]
    turtles = create_turtles(colors)
    countdown()
    winner = race(turtles)
    celebrate_winner(winner)
    screen.bye()


if __name__ == '__main__':
    main()
