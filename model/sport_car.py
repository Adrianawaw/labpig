from model.base_class import BaseCar


class sport_car(BaseCar):
    def __init__(self, brand, model, year, max_speed, acceleration, brake_type):
        super().__init__(brand, model, year)
        self.parameters['max_speed'] = max_speed
        self.parameters['acceleration'] = acceleration
        self.parameters['brake_type'] = brake_type

    def get_parameters(self, params):
        try:
            return super().get_parameters(params)
        except KeyError:
            return None
