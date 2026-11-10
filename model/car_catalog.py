import json
from pathlib import Path

from model.database import Database
from model.off_road import off_road
from model.sedan import Sedan
from model.sport_car import sport_car


class CarCatalog:
    def __init__(self):
        self.database = Database()
        if self.database.is_empty():
            self._seed_database()
        self.cars = []
        self._load_cars()

    def sort_by_year(self, reverse=False):
        self._load_cars('year', reverse)

    def sort_by_brand(self, reverse=False):
        self._load_cars('brand', reverse)

    def sort_by_model(self, reverse=False):
        self._load_cars('model', reverse)

    def sort_by_type(self, reverse=False):
        self._load_cars('type', reverse)

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
        return self.database.fetch_performance()

    def get_statistics(self):
        statistics, fastest = self.database.fetch_statistics()
        fastest_text = '-'
        if fastest:
            fastest_text = (
                f"{fastest['brand']} {fastest['model']} "
                f"({fastest['speed']} km/h)"
            )
        return {
            'total': statistics['total'],
            'first_year': statistics['first_year'] or '-',
            'last_year': statistics['last_year'] or '-',
            'fastest': fastest_text,
        }

    def get_type_distribution(self):
        return self.database.fetch_distribution('type')

    def get_year_distribution(self):
        return self.database.fetch_distribution('year')

    def get_model_distribution(self):
        return self.database.fetch_distribution('model')

    def add_car(self, car):
        car.database_id = self.database.insert_car(
            car.__class__.__name__,
            car.parameters,
        )
        self._load_cars()

    def remove_car(self, car):
        if car.database_id is not None:
            self.database.delete_car(car.database_id)
        self._load_cars()

    def save_cars(self):
        for car in self.cars:
            if car.database_id is not None:
                self.database.update_car(
                    car.database_id,
                    car.__class__.__name__,
                    car.parameters,
                )
        self._load_cars()

    def _load_cars(self, order_by='year', descending=False):
        self.cars = [
            self._create_car(row)
            for row in self.database.fetch_cars(order_by, descending)
        ]

    def _create_car(self, row):
        parameters = row['parameters']
        common = (
            parameters['brand'],
            parameters['model'],
            parameters['year'],
        )
        if row['car_type'] == 'Sedan':
            car = Sedan(
                *common,
                parameters['doors'],
                parameters['type_suspension'],
                parameters['passenger_capacity'],
            )
        elif row['car_type'] == 'off_road':
            car = off_road(
                *common,
                parameters['clearance_mm'],
                parameters['transmision_type'],
                parameters['differential_lock'],
            )
        elif row['car_type'] == 'sport_car':
            car = sport_car(
                *common,
                parameters['max_speed'],
                parameters['acceleration'],
                parameters['brake_type'],
            )
        else:
            raise ValueError(f"Unknown car type in database: {row['car_type']}")
        car.database_id = row['id']
        car.set_parameters('image_path', parameters.get('image_path', ''))
        return car

    def _seed_database(self):
        storage_path = Path(__file__).resolve().parent / 'data' / 'cars.json'
        if not storage_path.exists():
            return
        data = json.loads(storage_path.read_text(encoding='utf-8-sig'))
        for item in data:
            self.database.insert_car(item['type'], item['parameters'])
