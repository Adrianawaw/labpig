class CarPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.sort_directions = {
            'year': False,
            'brand': False,
            'model': False,
            'type': False,
        }
        self.selected_type = 'All'

    def start(self):
        self.model.sort_by_year()
        self._refresh_view('Year (ascending)')

    def filter_by_type(self, car_type):
        self.selected_type = car_type
        self._refresh_view(f'Filter: {car_type}')

    def sort_by_year(self):
        reverse = self.sort_directions['year']
        self.model.sort_by_year(reverse)
        self._refresh_view(self._sort_name('Year', reverse))
        self.sort_directions['year'] = not reverse

    def sort_by_brand(self):
        reverse = self.sort_directions['brand']
        self.model.sort_by_brand(reverse)
        self._refresh_view(self._sort_name('Brand', reverse))
        self.sort_directions['brand'] = not reverse

    def sort_by_model(self):
        reverse = self.sort_directions['model']
        self.model.sort_by_model(reverse)
        self._refresh_view(self._sort_name('Model', reverse))
        self.sort_directions['model'] = not reverse

    def sort_by_type(self):
        reverse = self.sort_directions['type']
        self.model.sort_by_type(reverse)
        self._refresh_view(self._sort_name('Type', reverse))
        self.sort_directions['type'] = not reverse

    def add_car(self, car):
        self.model.add_car(car)
        self._refresh_view('Current order')

    def remove_car(self, car):
        self.model.remove_car(car)
        self._refresh_view('Current order')

    def update_car(self, car):
        self.model.save_cars()
        self._refresh_view('Current order')

    def get_chart_data(self, chart_kind='Type'):
        chart_methods = {
            'Type': self.model.get_type_distribution,
            'Year': self.model.get_year_distribution,
            'Model': self.model.get_model_distribution,
            'Performance': self.model.get_performance_data,
        }
        return chart_methods[chart_kind]()

    def show_chart(self):
        self.view.show_chart(self.get_chart_data())

    def get_statistics(self):
        return self.model.get_statistics()

    def _refresh_view(self, sort_name):
        self.view.show_cars(
            self._format_cars(sort_name),
            self.model.get_cars_by_type(self.selected_type),
        )

    def _sort_name(self, field_name, reverse):
        direction = 'descending' if reverse else 'ascending'
        return f'{field_name} ({direction})'

    def _format_cars(self, sort_name, cars=None):
        lines = [f'Sorted by {sort_name}:', '']
        lines.append(f'{"Type":<14}{"Brand":<18}{"Model":<18}{"Year":<6}')
        lines.append('-' * 56)
        for car in cars if cars is not None else self.model.get_cars():
            car_type = car.__class__.__name__.replace('_', ' ').title()
            lines.append(
                f'{car_type:<14}{car.get_parameters("brand"):<18}'
                f'{car.get_parameters("model"):<18}{car.get_parameters("year"):<6}'
            )
        return '\n'.join(lines)
