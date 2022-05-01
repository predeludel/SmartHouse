from flask import render_template, request, jsonify
from model import *

house = House()


@app.route('/api/<room_name>', methods=["GET"])
def api_room(room_name):
    room = get_room(room_name)
    return jsonify(room.as_dict())


@app.route('/api/security', methods=["GET"])
def api_security():
    return jsonify(house.security.as_dict())


@app.route('/api/robot', methods=["GET"])
def api_robot():
    return jsonify(house.robot.as_dict())


@app.route('/api/farm', methods=["GET"])
def api_farm():
    return jsonify(house.farm.as_dict())


@app.route('/api/<room_name>/light', methods=["GET", "POST"])
def api_light(room_name):
    room = get_room(room_name)
    if request.method == 'POST':
        room.light = request.json.get("light")
        house.save()
    return jsonify(room.as_dict())


@app.route('/api/<room_name>/temperature', methods=["GET", "POST"])
def api_temperature(room_name):
    room = get_room(room_name)
    if request.method == 'POST':
        room.temperature = float(request.json.get("temperature"))
        house.save()
    return jsonify(room.as_dict())


@app.route('/api/security/<room_name>', methods=["GET", "POST"])
def api_security_sensor(room_name):
    if request.method == 'POST':
        house.security.set_sensor(room_name, request.json.get("sensor"))
        house.save()
    return jsonify(house.security.as_dict())


@app.route('/api/security/door', methods=["GET", "POST"])
def api_security_door():
    if request.method == 'POST':
        house.security.door = request.json.get("door")
        house.save()
    return jsonify(house.security.as_dict())


@app.route('/api/robot/energy', methods=["GET", "POST"])
def api_robot_energy():
    if request.method == 'POST':
        house.robot.energy = int(request.json.get("energy"))
        house.save()
    return jsonify(house.robot.as_dict())


@app.route('/api/robot/place', methods=["GET", "POST"])
def api_robot_place():
    if request.method == 'POST':
        house.robot.place = request.json.get("place")
        house.save()
    return jsonify(house.robot.as_dict())


@app.route('/api/robot/status', methods=["GET", "POST"])
def api_robot_status():
    if request.method == 'POST':
        house.robot.status = request.json.get("status")
        house.save()
    return jsonify(house.robot.as_dict())


@app.route('/api/farm/temperature', methods=["GET", "POST"])
def api_farm_temperature():
    if request.method == 'POST':
        house.farm.temperature = float(request.json.get("temperature"))
        house.save()
    return jsonify(house.farm.as_dict())


@app.route('/api/farm/light', methods=["GET", "POST"])
def api_farm_light():
    if request.method == 'POST':
        house.farm.light = request.json.get("light")
        house.save()
    return jsonify(house.farm.as_dict())


@app.route('/api/farm/status', methods=["GET", "POST"])
def api_farm_status():
    if request.method == 'POST':
        house.farm.status = request.json.get("status")
        house.save()
    return jsonify(house.farm.as_dict())


@app.route('/api/farm/stage', methods=["GET", "POST"])
def api_farm_stage():
    if request.method == 'POST':
        house.farm.stage = request.json.get("stage")
        house.save()
    return jsonify(house.farm.as_dict())


def get_room(room_name):
    if room_name == BEDROOM:
        return house.bedroom
    elif room_name == LIVING_ROOM:
        return house.living_room
    elif room_name == KITCHEN:
        return house.kitchen
    elif room_name == BATHROOM:
        return house.bathroom


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
    room = get_room(room_name)
    room.light = not room.light
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
            room = get_room(room_name)
            room.temperature = new_temperature
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
