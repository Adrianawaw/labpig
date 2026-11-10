from model.interface import Interface


class BaseCar(Interface):
    def __init__(self, brand, model, year):
        self.database_id = None
        self.parameters = {}
        self.parameters['brand'] = brand
        self.parameters['model'] = model
        self.parameters['year'] = year
        self.parameters['image_path'] = ''

    def set_parameters(self, params, values):
        self.parameters[params] = values

    def get_parameters(self, params):
        return self.parameters.get(params)
