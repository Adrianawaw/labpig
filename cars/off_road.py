
from base_class.base_class import BaseCar

class off_road(BaseCar):
    def __init__(self, brand , model , year, clearance_mm , transmision_type, differential_lock):
        super().__init__(brand, model, year)
        self.parameters['clearance_mm'] = clearance_mm
        self.parameters['transmision_type'] = transmision_type
        self.parameters['differential_lock'] = differential_lock

    def get_parameters(self, params):
        try:
            return super().get_parameters(params)
        except KeyError:
            return None
