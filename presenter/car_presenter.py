class CarPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        self.sort_by_year()

    def sort_by_year(self):
        self.model.sort_by_year()
        self.view.show_cars(self._format_cars('Year (descending)'))

    def sort_by_brand(self):
        self.model.sort_by_brand()
        self.view.show_cars(self._format_cars('Brand (ascending)'))

    def sort_by_type(self):
        self.model.sort_by_type()
        self.view.show_cars(self._format_cars('Type (ascending)'))

    def _format_cars(self, sort_name):
        lines = [f'Sorted by {sort_name}:', '']
        lines.append(f'{"Type":<14}{"Brand":<18}{"Model":<18}{"Year":<6}')
        lines.append('-' * 56)
        for car in self.model.get_cars():
            car_type = car.__class__.__name__.replace('_', ' ').title()
            lines.append(
                f'{car_type:<14}{car.get_parameters("brand"):<18}'
                f'{car.get_parameters("model"):<18}{car.get_parameters("year"):<6}'
            )
        return '\n'.join(lines)
