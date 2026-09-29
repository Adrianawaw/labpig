from model.off_road import off_road
from model.sedan import Sedan
from model.sport_car import sport_car


class CarCatalog:
    def __init__(self):
        self.cars = [
            Sedan('Toyota', 'Camry', 2020, 4, 'independent', 5),
            Sedan('Honda', 'Accord', 2021, 4, 'independent', 5),
            Sedan('Ford', 'Fusion', 2019, 4, 'independent', 5),
            Sedan('Chevrolet', 'Malibu', 2020, 4, 'independent', 5),
            Sedan('Nissan', 'Altima', 2021, 4, 'independent', 5),
            Sedan('Hyundai', 'Sonata', 2020, 4, 'independent', 5),
            Sedan('Kia', 'Optima', 2021, 4, 'independent', 5),
            Sedan('Mazda', '6', 2019, 4, 'independent', 5),
            Sedan('Volkswagen', 'Passat', 2020, 4, 'independent', 5),
            Sedan('Subaru', 'Legacy', 2021, 4, 'independent', 5),
            off_road('Jeep', 'Wrangler', 2020, 250, 'manual', True),
            off_road('Land Rover', 'Defender', 2021, 300, 'automatic', True),
            off_road('Toyota', 'Land Cruiser', 2019, 280, 'automatic', True),
            off_road('Ford', 'Bronco', 2020, 270, 'manual', True),
            off_road('Chevrolet', 'Blazer', 2021, 260, 'automatic', True),
            off_road('Nissan', 'Xterra', 2020, 250, 'manual', True),
            off_road('Jeep', 'Cherokee', 2021, 240, 'automatic', True),
            off_road('Toyota', '4Runner', 2020, 230, 'manual', True),
            off_road('Land Rover', 'Discovery', 2020, 220, 'automatic', True),
            off_road('Ford', 'Ranger', 2020, 210, 'manual', True),
            sport_car('Porsche', '911', 2020, 330, 3.5, 'disc'),
            sport_car('Ferrari', '488', 2021, 330, 3.0, 'disc'),
            sport_car('Lamborghini', 'Huracan', 2019, 325, 3.2, 'disc'),
            sport_car('McLaren', '720S', 2020, 341, 2.9, 'disc'),
            sport_car('Aston Martin', 'Vantage', 2021, 314, 3.6, 'disc'),
            sport_car('Chevrolet', 'Corvette', 2020, 312, 3.7, 'disc'),
            sport_car('Nissan', 'GT-R', 2021, 315, 3.8, 'disc'),
            sport_car('BMW', 'M4', 2020, 290, 4.0, 'disc'),
            sport_car('Audi', 'R8', 2021, 330, 3.9, 'disc'),
            sport_car('Mercedes-Benz', 'AMG GT', 2020, 310, 4.1, 'disc'),
            Sedan('Volvo', 'S90', 2022, 4, 'independent', 5),
            Sedan('Tesla', 'Model 3', 2022, 4, 'independent', 5),
            Sedan('Lexus', 'ES', 2022, 4, 'independent', 5),
            Sedan('Renault', 'Talisman', 2018, 4, 'independent', 5),
            Sedan('Peugeot', '508', 2022, 4, 'independent', 5),
            Sedan('Skoda', 'Superb', 2018, 4, 'independent', 5),
            off_road('Suzuki', 'Jimny', 2018, 205, 'manual', True),
            off_road('Mitsubishi', 'Pajero', 2017, 235, 'automatic', True),
            off_road('Hummer', 'EV', 2022, 300, 'automatic', True),
            off_road('GMC', 'Terrain', 2019, 210, 'automatic', True),
            off_road('Dacia', 'Duster', 2022, 210, 'manual', True),
            sport_car('Toyota', 'Supra', 2022, 250, 4.1, 'disc'),
            sport_car('Ford', 'Mustang', 2021, 290, 4.4, 'disc'),
            sport_car('Jaguar', 'F-Type', 2020, 300, 4.0, 'disc'),
            sport_car('Lotus', 'Emira', 2022, 290, 4.3, 'disc'),
            sport_car('Koenigsegg', 'Jesko', 2021, 480, 2.8, 'disc'),
        ]

    def sort_by_year(self, reverse=False):
        self.cars.sort(key=lambda car: car.get_parameters('year'), reverse=reverse)

    def sort_by_brand(self, reverse=False):
        self.cars.sort(key=lambda car: car.get_parameters('brand'), reverse=reverse)

    def sort_by_type(self, reverse=False):
        self.cars.sort(key=lambda car: car.__class__.__name__, reverse=reverse)

    def get_cars(self):
        return self.cars
