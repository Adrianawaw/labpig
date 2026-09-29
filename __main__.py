from model.car_catalog import CarCatalog
from presenter.car_presenter import CarPresenter
from view.car_view import CarView


class CarApplication:
    def __init__(self):
        model = CarCatalog()
        view = CarView(None)
        self.presenter = CarPresenter(model, view)
        view.presenter = self.presenter
        self.view = view

    def run(self):
        self.presenter.start()
        self.view.run()


if __name__ == '__main__':
    CarApplication().run()
