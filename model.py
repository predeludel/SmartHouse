from flask import Flask

app = Flask(__name__, static_folder="static", static_url_path='/static')

app.debug = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

DATABASE_FOLDER = "database"
BEDROOM = "bedroom"
LIVING_ROOM = "living_room"
KITCHEN = "kitchen"
BATHROOM = "bathroom"
TRUE = "True"
ROBOT_FILE = "robot.txt"
FARM_FILE = "farm.txt"
SECURITY_FILE = "security.txt"


class Config:
    INIT_LIGHT = True
    INIT_TEMPERATURE = 0.0
    INIT_NOISE = True
    INIT_STATUS = False
    INIT_ENERGY = 100
    INIT_PLACE = "На зарядке"
    INIT_STAGE = "Не активна"
    INIT_DOOR = True
    INIT_SENSOR = False


class Robot:
    def __init__(self, status, energy, place):
        self.status = status
        self.energy = energy
        self.place = place

    def save(self):
        with open(f'{DATABASE_FOLDER}/{ROBOT_FILE}', 'w', encoding='utf-8') as file:
            file.write(f"status={self.status}\n")
            file.write(f"energy={self.energy}\n")
            file.write(f"place={self.place}")

    def load(self):
        try:
            with open(f'{DATABASE_FOLDER}/{ROBOT_FILE}', 'r', encoding='utf-8') as file:
                data = file.read().split("\n")
                self.status = data[0].split("=")[1] == TRUE
                self.energy = int(data[1].split("=")[1])
                self.place = data[2].split("=")[1]
        except FileNotFoundError:
            self.save()
        except ValueError:
            self.save()

    def as_dict(self):
        return {
            "status": self.status,
            "energy": self.energy,
            "place": self.place
        }


class Farm:
    def __init__(self, temperature, light, status, stage):
        self.temperature = temperature
        self.light = light
        self.status = status
        self.stage = stage

    def save(self):
        with open(f'{DATABASE_FOLDER}/{FARM_FILE}', 'w', encoding='utf-8') as file:
            file.write(f"temperature={self.temperature}\n")
            file.write(f"light={self.light}\n")
            file.write(f"status={self.status}\n")
            file.write(f"stage={self.stage}")

    def load(self):
        try:
            with open(f'{DATABASE_FOLDER}/{FARM_FILE}', 'r', encoding='utf-8') as file:
                data = file.read().split("\n")
                self.temperature = float(data[0].split("=")[1])
                self.light = (data[1].split("=")[1]) == TRUE
                self.status = (data[2].split("=")[1]) == TRUE
                self.stage = (data[3].split("=")[1])

        except FileNotFoundError:
            self.save()
        except ValueError:
            self.save()

    def as_dict(self):
        return {
            "temperature": self.temperature,
            "light": self.light,
            "status": self.status,
            "stage": self.stage
        }


class Room:
    def __init__(self, name, light, temperature):
        self.name = name
        self.light = light
        self.temperature = temperature

    def save(self):
        with open(f'{DATABASE_FOLDER}/{self.name}.txt', 'w', encoding='utf-8') as file:
            file.write(f"light={self.light}\n")
            file.write(f"temperature={self.temperature}\n")

    def load(self):
        try:
            with open(f'{DATABASE_FOLDER}/{self.name}.txt', 'r', encoding='utf-8') as file:
                data = file.read().split("\n")
                self.light = data[0].split("=")[1] == TRUE
                self.temperature = float(data[1].split("=")[1])
        except FileNotFoundError:
            self.save()
        except ValueError:
            self.save()

    def as_dict(self):
        return {
            "light": self.light,
            "temperature": self.temperature,
        }


class Security:
    def __init__(self, door, sensor_bedroom, sensor_living_room, sensor_kitchen, sensor_bathroom):
        self.door = door
        self.sensor_bedroom = sensor_bedroom
        self.sensor_living_room = sensor_living_room
        self.sensor_kitchen = sensor_kitchen
        self.sensor_bathroom = sensor_bathroom

    def save(self):
        with open(f'{DATABASE_FOLDER}/{SECURITY_FILE}', 'w', encoding='utf-8') as file:
            file.write(f"door={self.door}\n")
            file.write(f"sensor_bedroom={self.sensor_bedroom}\n")
            file.write(f"sensor_living_room={self.sensor_living_room}\n")
            file.write(f"sensor_kitchen={self.sensor_kitchen}\n")
            file.write(f"sensor_bathroom ={self.sensor_bathroom}")

    def load(self):
        try:
            with open(f'{DATABASE_FOLDER}/{SECURITY_FILE}', 'r', encoding='utf-8') as file:
                data = file.read().split("\n")
                self.door = data[0].split("=")[1] == TRUE
                self.sensor_bedroom = data[1].split("=")[1] == TRUE
                self.sensor_living_room = data[2].split("=")[1] == TRUE
                self.sensor_kitchen = data[3].split("=")[1] == TRUE
                self.sensor_bathroom = data[4].split("=")[1] == TRUE

        except FileNotFoundError:
            self.save()
        except ValueError:
            self.save()

    def as_dict(self):
        return {
            "door": self.door,
            "sensor_bedroom": self.sensor_bedroom,
            "sensor_living_room ": self.sensor_living_room,
            "sensor_kitchen": self.sensor_kitchen,
            "sensor_bathroom": self.sensor_bathroom,
        }

    def set_sensor(self, room_name, value):
        if room_name == BEDROOM:
            self.sensor_bedroom = value
        elif room_name == BATHROOM:
            self.sensor_bathroom = value
        elif room_name == KITCHEN:
            self.sensor_kitchen = value
        elif room_name == LIVING_ROOM:
            self.sensor_living_room = value


class House:
    def __init__(self):
        self.bedroom = Room(BEDROOM, Config.INIT_LIGHT, Config.INIT_TEMPERATURE)
        self.living_room = Room(LIVING_ROOM, Config.INIT_LIGHT, Config.INIT_TEMPERATURE)
        self.kitchen = Room(KITCHEN, Config.INIT_LIGHT, Config.INIT_TEMPERATURE)
        self.bathroom = Room(BATHROOM, Config.INIT_LIGHT, Config.INIT_TEMPERATURE)
        self.robot = Robot(Config.INIT_STATUS, Config.INIT_ENERGY, Config.INIT_PLACE)
        self.farm = Farm(Config.INIT_TEMPERATURE, Config.INIT_LIGHT, Config.INIT_STATUS, Config.INIT_STAGE)
        self.security = Security(Config.INIT_DOOR, Config.INIT_SENSOR, Config.INIT_SENSOR, Config.INIT_SENSOR,
                                 Config.INIT_SENSOR)

    def load(self):
        self.bedroom.load()
        self.living_room.load()
        self.kitchen.load()
        self.bathroom.load()
        self.robot.load()
        self.farm.load()
        self.security.load()

    def save(self):
        self.bedroom.save()
        self.living_room.save()
        self.kitchen.save()
        self.bathroom.save()
        self.robot.save()
        self.farm.save()
        self.security.save()
