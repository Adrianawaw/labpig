from interface.interface import Interface

class BaseCar(Interface):
    def __init__(self, brand, model, year):
        self.parameters = {}
        self.parameters['brand'] = brand
        self.parameters['model'] = model
        self.parameters['year'] = year


    def set_parameters(self, params, values):
        self.parameters[params] = values


    def get_parameters(self, params):
        return self.parameters.get(params)
    