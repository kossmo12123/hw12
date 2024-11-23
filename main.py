import random
import logging


logging.basicConfig(filename='simulation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Human:
    def __init__(self, name="Human", job=None, home=None, car=None, pet=None):
        self.name = name
        self.money = 100
        self.gladness = 50
        self.satiety = 50
        self.job = job
        self.car = car
        self.home = home
        self.pet = pet

    def get_home(self):
        self.home = House()
        logging.info(f"{self.name} settled in a house.")

    def get_car(self):
        self.car = Auto(brands_of_car)
        logging.info(f"{self.name} bought a car {self.car.brand}.")

    def get_job(self):
        if self.car.drive():
            pass
        else:
            self.to_repair()
        self.job = Job(job_list)
        logging.info(f"{self.name} got a job as {self.job.job} with salary {self.job.salary}.")

    def get_pet(self):
        self.pet = Pet("Buddy")
        logging.info(f"{self.name} got a pet named {self.pet.name}.")

    def feed_pet(self):
        if self.pet:
            logging.info(f"Feeding {self.pet.name}")
            self.pet.feed()

    def play_with_pet(self):
        if self.pet:
            logging.info(f"Playing with {self.pet.name}")
            self.pet.play()
            self.gladness += 5

    def eat(self):
        if self.home.food <= 0:
            self.shopping("food")
        else:
            if self.satiety >= 100:
                self.satiety = 100
                return
            self.satiety += 5
            self.home.food -= 5
            logging.info(f"{self.name} ate some food. Satiety is now {self.satiety}.")

    def work(self):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                self.shopping("fuel")
                return
            else:
                self.to_repair()
                return
        self.money += self.job.salary
        self.gladness -= self.job.gladness_less
        self.satiety -= 4
        logging.info(f"{self.name} went to work. Money: {self.money}, Gladness: {self.gladness}, Satiety: {self.satiety}.")

    def shopping(self, manage):
        if self.car.drive():
            pass
        else:
            if self.car.fuel < 20:
                manage = "fuel"
            else:
                self.to_repair()
                return
        if manage == "fuel":
            logging.info("Bought fuel")
            self.money -= 100
            self.car.fuel += 100
        elif manage == "food":
            logging.info("Bought food")
            self.money -= 50
            self.home.food += 50
        elif manage == "delicacies":
            logging.info("Bought delicacies")
            self.gladness += 10
            self.satiety += 2
            self.money -= 15

    def chill(self):
        self.gladness += 10
        self.home.mess += 5
        logging.info(f"{self.name} chilled. Gladness: {self.gladness}, Mess: {self.home.mess}.")

    def clean_home(self):
        self.gladness -= 5
        self.home.mess = 0
        logging.info(f"{self.name} cleaned the home. Gladness: {self.gladness}, Mess: {self.home.mess}.")

    def to_repair(self):
        self.car.strength += 100
        self.money -= 50
        logging.info(f"{self.name} repaired the car. Strength: {self.car.strength}, Money: {self.money}.")

    def days_indexes(self, day):
        day = f" Today the {day} of {self.name}'s life "
        logging.info(day)
        logging.info(f"Money – {self.money}")
        logging.info(f"Satiety – {self.satiety}")
        logging.info(f"Gladness – {self.gladness}")
        logging.info(f"Food – {self.home.food}")
        logging.info(f"Mess – {self.home.mess}")
        logging.info(f"Fuel – {self.car.fuel}")
        logging.info(f"Strength – {self.car.strength}")
        if self.pet:
            logging.info(f"Happiness – {self.pet.happiness}")
            logging.info(f"Hunger – {self.pet.hunger}")

    def is_alive(self):
        if self.gladness < 0:
            logging.warning("Depression…")
            return False
        if self.satiety < 0:
            logging.warning("Dead…")
            return False
        if self.money < -500:
            logging.warning("Bankrupt…")
            return False
        return True

    def live(self, day):
        if not self.is_alive():
            return False
        if self.home is None:
            logging.info("Settled in the house")
            self.get_home()
        if self.car is None:
            self.get_car()
            logging.info(f"I bought a car {self.car.brand}")
        if self.job is None:
            self.get_job()
            logging.info(f"I don't have a job, going to get a job {self.job.job} with salary {self.job.salary}")
        if self.pet is None:
            self.get_pet()
            logging.info(f"Got a pet named {self.pet.name}")
        self.days_indexes(day)
        dice = random.randint(1, 5)
        if self.satiety < 20:
            logging.info("I'll go eat")
            self.eat()
        elif self.gladness < 20:
            if self.home.mess > 15:
                logging.info("I want to chill, but there is so much mess… So I will clean the house")
                self.clean_home()
            else:
                logging.info("Let`s chill!")
                self.chill()
        elif self.money < 0:
            logging.info("Start working")
            self.work()
        elif self.car.strength < 15:
            logging.info("I need to repair my car")
            self.to_repair()
        elif dice == 1:
            logging.info("Let`s chill!")
            self.chill()
        elif dice == 2:
            logging.info("Start working")
            self.work()
        elif dice == 3:
            logging.info("Cleaning time!")
            self.clean_home()
        elif dice == 4:
            logging.info("Time for treats!")
            self.shopping(manage="delicacies")
        elif dice == 5:
            logging.info("Time to play with the pet!")
            self.play_with_pet()

class Auto:
    def __init__(self, brand_list):
        self.brand = random.choice(list(brand_list))
        self.fuel = brand_list[self.brand]["fuel"]
        self.strength = brand_list[self.brand]["strength"]
        self.consumption = brand_list[self.brand]["consumption"]

    def drive(self):
        if self.strength > 0 and self.fuel >= self.consumption:
            self.fuel -= self.consumption
            self.strength -= 1
            return True
        else:
            logging.info("The car cannot move")
            return False

class House:
    def __init__(self):
        self.mess = 0
        self.food = 0

class Pet:
    def __init__(self, name):
        self.name = name
        self.happiness = 50
        self.hunger = 50

    def feed(self):
        if self.hunger >= 100:
            self.hunger = 100
            return
        self.hunger += 5

    def play(self):
        if self.happiness >= 100:
            self.happiness = 100
            return
        self.happiness += 10

job_list = {
    "Java developer": {"salary": 50, "gladness_less": 10},
    "Python developer": {"salary": 40, "gladness_less": 3},
    "C++ developer": {"salary": 45, "gladness_less": 25},
    "Rust developer": {"salary": 70, "gladness_less": 1},
}

brands_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14},
}

class Job:
    def __init__(self, job_list):
        self.job = random.choice(list(job_list))
        self.salary = job_list[self.job]["salary"]
        self.gladness_less = job_list[self.job]["gladness_less"]

nick = Human(name="Nick")
for day in range(1, 8):
    if not nick.live(day):
        break
