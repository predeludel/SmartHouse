from flask import render_template
from model import *

house = House()


@app.route('/')
def show_main():
    house.load()
    return render_template("main.html",
                           house=house,
                           temperature_bedroom=house.bedroom.temperature,
                           temperature_living_room=house.living_room.temperature,
                           temperature_kitchen=house.kitchen.temperature,
                           temperature_bathroom=house.bathroom.temperature,
                           status_robot=house.robot.status,
                           energy_robot=house.robot.energy, place_robot=house.robot.place)


@app.route('/<room_name>/light')
def light_room(room_name):
    if room_name == BEDROOM:
        house.bedroom.light = not house.bedroom.light
    elif room_name == LIVING_ROOM:
        house.living_room.light = not house.living_room.light
    elif room_name == KITCHEN:
        house.kitchen.light = not house.kitchen.light
    elif room_name == BATHROOM:
        house.bathroom.light = not house.bathroom.light
    house.save()
    return show_main()


@app.route('/robot/status')
def status_robot():
    house.robot.status = not house.robot.status
    house.save()
    return show_main()


@app.route('/farm/light')
def light_farm():
    if house.farm.status:
        house.farm.light = not house.farm.light
        house.save()
    return show_main()


@app.route('/farm/status')
def status_farm():
    house.farm.status = not house.farm.status
    house.farm.light = False
    house.farm.temperature = 0
    house.farm.stage = "Не активна"
    house.save()
    return show_main()


if __name__ == '__main__':
    app.run()
