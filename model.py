from flask import Flask

app = Flask(__name__, static_folder="static", static_url_path='/static')

app.debug = True
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

DATABASE_FOLDER = "database"
BEDROOM = "bedroom"
LIVING_ROOM = "living_room"

TRUE = "True"


class Config:
    INIT_LIGHT = True
    INIT_TEMPERATURE = 0.0
    INIT_NOISE = True


class Robot:
    pass


class Room:
    def __init__(self, name, light, temperature, noise):
        self.name = name
        self.light = light
        self.temperature = temperature
        self.noise = noise

    def save(self):
        with open(f'{DATABASE_FOLDER}/{self.name}.txt', 'w', encoding='utf-8') as file:
            file.write(f"light={self.light}\n")
            file.write(f"temperature={self.temperature}\n")
            file.write(f"noise={self.noise}")

    def load(self):
        try:
            with open(f'{DATABASE_FOLDER}/{self.name}.txt', 'r', encoding='utf-8') as file:
                data = file.read().split("\n")
                self.light = data[0].split("=")[1] == TRUE
                self.temperature = float(data[1].split("=")[1])
                self.noise = data[2].split("=")[1] == TRUE
        except FileNotFoundError:
            self.save()
        except ValueError:
            self.save()


class House:
    def __init__(self):
        self.bedroom = Room(BEDROOM, Config.INIT_LIGHT, Config.INIT_TEMPERATURE, Config.INIT_NOISE)
        self.living_room = Room(LIVING_ROOM, Config.INIT_LIGHT, Config.INIT_TEMPERATURE, Config.INIT_NOISE)

    def load(self):
        self.bedroom.load()
        self.living_room.load()

    def save(self):
        self.bedroom.save()
        self.living_room.save()
