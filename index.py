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
    elif room_name == KITCHEN:
        house.kitchen.light = not house.kitchen.light
        print("wef")
    elif room_name == BATHROOM:
        house.bathroom.light = not house.bathroom.light
        print("ты норм")
    house.save()
    return show_main()


@app.route('/<room_name>/temperature')
def temperature(room_name):
    if room_name == BEDROOM:
        temperature = "123"
    elif room_name == LIVING_ROOM:
        temperature = house.living_room.temperature
    elif room_name == KITCHEN:
        temperature = house.kitchen.temperature
    elif room_name == BATHROOM:
        temperature = house.bathroom.temperature
    house.save()
    return show_main(temperature=temperature)


if __name__ == '__main__':
    app.run()
