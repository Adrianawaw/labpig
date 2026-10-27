import json
from pathlib import Path

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
        self.storage_path = Path(__file__).resolve().parent / 'data' / 'cars.json'
        self._load_cars()

    def sort_by_year(self, reverse=False):
        self.cars.sort(key=lambda car: car.get_parameters('year'), reverse=reverse)

    def sort_by_brand(self, reverse=False):
        self.cars.sort(key=lambda car: car.get_parameters('brand'), reverse=reverse)

    def sort_by_model(self, reverse=False):
        self.cars.sort(key=lambda car: car.get_parameters('model'), reverse=reverse)

    def sort_by_type(self, reverse=False):
        self.cars.sort(key=lambda car: car.__class__.__name__, reverse=reverse)

    def get_cars(self):
        return self.cars

    def get_cars_by_type(self, car_type):
        if car_type == 'All':
            return self.cars
        return [
            car for car in self.cars
            if car.__class__.__name__.replace('_', ' ').title() == car_type
        ]

    def get_performance_data(self):
        return [
            {
                'model': car.get_parameters('model'),
                'brand': car.get_parameters('brand'),
                'speed': car.get_parameters('max_speed'),
                'acceleration': car.get_parameters('acceleration'),
                'type': car.__class__.__name__.replace('_', ' ').title(),
            }
            for car in self.cars
            if car.get_parameters('max_speed') is not None
        ]

    def get_statistics(self):
        years = [car.get_parameters('year') for car in self.cars]
        speeds = self.get_performance_data()
        fastest = max(speeds, key=lambda car: car['speed'], default=None)
        return {
            'total': len(self.cars),
            'first_year': min(years, default='-'),
            'last_year': max(years, default='-'),
            'fastest': (
                f"{fastest['brand']} {fastest['model']} "
                f"({fastest['speed']} km/h)"
                if fastest else '-'
            ),
        }

    def get_type_distribution(self):
        return self._get_distribution(
            lambda car: car.__class__.__name__.replace('_', ' ').title()
        )

    def get_year_distribution(self):
        return self._get_distribution(lambda car: str(car.get_parameters('year')))

    def get_model_distribution(self):
        return self._get_distribution(lambda car: car.get_parameters('model'))

    def _get_distribution(self, key_factory):
        distribution = {}
        for car in self.cars:
            key = key_factory(car)
            distribution[key] = distribution.get(key, 0) + 1
        return dict(sorted(distribution.items()))

    def add_car(self, car):
        self.cars.append(car)
        self.save_cars()

    def remove_car(self, car):
        if car in self.cars:
            self.cars.remove(car)
            self.save_cars()

    def save_cars(self):
        data = [
            {
                'type': car.__class__.__name__,
                'parameters': car.parameters,
            }
            for car in self.cars
        ]
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    def _load_cars(self):
        if not self.storage_path.exists():
            return

        data = json.loads(self.storage_path.read_text(encoding='utf-8-sig'))
        self.cars = [self._create_car(item) for item in data]

    def _create_car(self, item):
        parameters = item['parameters']
        car_type = item['type']
        common = (
            parameters['brand'],
            parameters['model'],
            parameters['year'],
        )
        if car_type == 'Sedan':
            car = Sedan(
                *common,
                parameters['doors'],
                parameters['type_suspension'],
                parameters['passenger_capacity'],
            )
        elif car_type == 'off_road':
            car = off_road(
                *common,
                parameters['clearance_mm'],
                parameters['transmision_type'],
                parameters['differential_lock'],
            )
        elif car_type == 'sport_car':
            car = sport_car(
                *common,
                parameters['max_speed'],
                parameters['acceleration'],
                parameters['brake_type'],
            )
        else:
            raise ValueError(f'Unknown car type in storage: {car_type}')

        car.set_parameters('image_path', parameters.get('image_path', ''))
        return car
