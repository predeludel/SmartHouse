from flask import render_template
from model import *

house = House()


@app.route('/')
def show_main():
    house.load()
    return render_template("main.html", house=house)


@app.route('/<room_name>/light')
def light(room_name):
    if room_name == BEDROOM:
        house.bedroom.light = not house.bedroom.light
    elif room_name == LIVING_ROOM:
        house.living_room.light = not house.living_room.light
    house.save()
    return show_main()


if __name__ == '__main__':
    app.run()
