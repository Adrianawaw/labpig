
from base_class.base_class import BaseCar

class Sedan(BaseCar):
    def __init__(self, brand , model , year, doors , type_suspension , passenger_capacity):
        super().__init__(brand, model, year)

        self.parameters['doors'] = doors
        self.parameters['type_suspension'] = type_suspension
        self.parameters['passenger_capacity'] = passenger_capacity

    def get_parameters(self, params):
        try:
            return super().get_parameters(params)
        except KeyError:
            return None