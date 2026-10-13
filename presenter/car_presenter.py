class CarPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.sort_directions = {
            'year': False,
            'brand': False,
            'type': False,
        }

    def start(self):
        self.model.sort_by_year()
        self.view.show_cars(self._format_cars('Year (ascending)'))

    def sort_by_year(self):
        reverse = self.sort_directions['year']
        self.model.sort_by_year(reverse)
        self.view.show_cars(self._format_cars(self._sort_name('Year', reverse)))
        self.sort_directions['year'] = not reverse

    def sort_by_brand(self):
        reverse = self.sort_directions['brand']
        self.model.sort_by_brand(reverse)
        self.view.show_cars(self._format_cars(self._sort_name('Brand', reverse)))
        self.sort_directions['brand'] = not reverse

    def sort_by_type(self):
        reverse = self.sort_directions['type']
        self.model.sort_by_type(reverse)
        self.view.show_cars(self._format_cars(self._sort_name('Type', reverse)))
        self.sort_directions['type'] = not reverse

    def add_car(self, car):
        self.model.add_car(car)
        self.view.show_cars(self._format_cars('Current order'))

    def remove_car(self, car):
        self.model.remove_car(car)
        self.view.show_cars(self._format_cars('Current order'))

    def update_car(self, car):
        self.model.save_cars()
        self.view.show_cars(self._format_cars('Current order'))

    def _sort_name(self, field_name, reverse):
        direction = 'descending' if reverse else 'ascending'
        return f'{field_name} ({direction})'

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
