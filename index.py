from flask import render_template, request
from model import *

house = House()


@app.route('/')
def login():
    if request.args.get("key") == "00":
        return show_main()
    return render_template("login.html")


def show_main():
    house.load()
    return render_template("main.html", house=house)


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


@app.route('/security/door')
def door():
    house.security.door = not house.security.door
    house.save()
    return show_main()


@app.route('/<room_name>/temperature/set')
def temperature_room(room_name):
    new_temperature = request.args.get("new_temperature")
    try:
        new_temperature = float(new_temperature.replace("℃", ""))
        if 0 < new_temperature < 38:
            if room_name == BEDROOM:
                house.bedroom.temperature = new_temperature
            elif room_name == LIVING_ROOM:
                house.living_room.temperature = new_temperature
            elif room_name == KITCHEN:
                house.kitchen.temperature = new_temperature
            elif room_name == BATHROOM:
                house.bathroom.temperature = new_temperature
            house.save()
            return show_main()
        else:
            return show_main()

    except ValueError:
        return show_main()


@app.route('/farm/temperature/set')
def temperature_farm():
    new_temperature = request.args.get("new_temperature")
    try:
        new_temperature = float(new_temperature.replace("℃", ""))
        if 15 < new_temperature < 28:
            house.farm.temperature = new_temperature
            house.save()
            return show_main()
        else:
            return show_main()

    except ValueError:
        return show_main()


@app.route('/farm/status')
def status_farm():
    if house.farm.status:
        house.farm.status = not house.farm.status
        house.farm.light = True
        house.farm.temperature = 25
        house.farm.stage = "Зелень не растет"

    else:
        house.farm.status = not house.farm.status
        house.farm.light = not house.farm.light
        house.farm.temperature = 0.0
        house.farm.stage = "Зелень растет"
    house.save()
    return show_main()


if __name__ == '__main__':
    app.run()
