import customtkinter

from cars.off_road import off_road
from cars.sedan import Sedan
from cars.sport_car import sport_car


class CarCatalog:
    def __init__(self):
        self.cars = [
            Sedan('Toyota', 'Camry', 2020, 4, 'independent', 5),
            Sedan('Honda', 'Accord', 2021, 4, 'independent', 5),
            Sedan('Ford', 'Fusion', 2019, 4, 'independent', 5),
            Sedan('Chevrolet', 'Malibu', 2020, 4, 'independent', 5),
            Sedan('Nissan', 'Altima', 2021, 4, 'independent', 5),
            Sedan('Hyundai', 'Sonata', 2020, 4, 'independent', 5),
            Sedan('Kia', 'Optima', 2021, 4, 'independent', 5),
            Sedan('Mazda', '6', 2019, 4, 'independent', 5),
            Sedan('Volkswagen', 'Passat', 2020, 4, 'independent', 5),
            Sedan('Subaru', 'Legacy', 2021, 4, 'independent', 5),
            off_road('Jeep', 'Wrangler', 2020, 250, 'manual', True),
            off_road('Land Rover', 'Defender', 2021, 300, 'automatic', True),
            off_road('Toyota', 'Land Cruiser', 2019, 280, 'automatic', True),
            off_road('Ford', 'Bronco', 2020, 270, 'manual', True),
            off_road('Chevrolet', 'Blazer', 2021, 260, 'automatic', True),
            off_road('Nissan', 'Xterra', 2020, 250, 'manual', True),
            off_road('Jeep', 'Cherokee', 2021, 240, 'automatic', True),
            off_road('Toyota', '4Runner', 2020, 230, 'manual', True),
            off_road('Land Rover', 'Discovery', 2021, 220, 'automatic', True),
            off_road('Ford', 'Ranger', 2020, 210, 'manual', True),
            sport_car('Porsche', '911', 2020, 330, 3.5, 'disc'),
            sport_car('Ferrari', '488', 2021, 330, 3.0, 'disc'),
            sport_car('Lamborghini', 'Huracan', 2019, 325, 3.2, 'disc'),
            sport_car('McLaren', '720S', 2020, 341, 2.9, 'disc'),
            sport_car('Aston Martin', 'Vantage', 2021, 314, 3.6, 'disc'),
            sport_car('Chevrolet', 'Corvette', 2020, 312, 3.7, 'disc'),
            sport_car('Nissan', 'GT-R', 2021, 315, 3.8, 'disc'),
            sport_car('BMW', 'M4', 2020, 290, 4.0, 'disc'),
            sport_car('Audi', 'R8', 2021, 330, 3.9, 'disc'),
            sport_car('Mercedes-Benz', 'AMG GT', 2020, 310, 4.1, 'disc'),
            Sedan('Volvo', 'S90', 2022, 4, 'independent', 5),
            Sedan('Tesla', 'Model 3', 2022, 4, 'independent', 5),
            Sedan('Lexus', 'ES', 2022, 4, 'independent', 5),
            Sedan('Renault', 'Talisman', 2018, 4, 'independent', 5),
            Sedan('Peugeot', '508', 2022, 4, 'independent', 5),
            Sedan('Skoda', 'Superb', 2018, 4, 'independent', 5),
            off_road('Suzuki', 'Jimny', 2018, 205, 'manual', True),
            off_road('Mitsubishi', 'Pajero', 2017, 235, 'automatic', True),
            off_road('Hummer', 'EV', 2022, 300, 'automatic', True),
            off_road('GMC', 'Terrain', 2019, 210, 'automatic', True),
            off_road('Dacia', 'Duster', 2022, 210, 'manual', True),
            sport_car('Toyota', 'Supra', 2022, 250, 4.1, 'disc'),
            sport_car('Ford', 'Mustang', 2021, 290, 4.4, 'disc'),
            sport_car('Jaguar', 'F-Type', 2020, 300, 4.0, 'disc'),
            sport_car('Lotus', 'Emira', 2022, 290, 4.3, 'disc'),
            sport_car('Koenigsegg', 'Jesko', 2021, 480, 2.8, 'disc'),
        ]

    def sort_by_year(self):
        self.cars.sort(key=lambda car: car.get_parameters('year'), reverse=True)

    def sort_by_brand(self):
        self.cars.sort(key=lambda car: car.get_parameters('brand'))

    def sort_by_type(self):
        self.cars.sort(key=lambda car: car.__class__.__name__)

    def as_text(self, sort_name):
        lines = [f'Sorted by {sort_name}:', '']
        lines.append(f'{"Type":<14}{"Brand":<18}{"Model":<18}{"Year":<6}')
        lines.append('-' * 56)
        for car in self.cars:
            car_type = car.__class__.__name__.replace('_', ' ').title()
            lines.append(
                f'{car_type:<14}{car.get_parameters("brand"):<18}'
                f'{car.get_parameters("model"):<18}{car.get_parameters("year"):<6}'
            )
        return '\n'.join(lines)


class CarApplication:
    def __init__(self):
        self.catalog = CarCatalog()
        self.current_sort = 'Year (descending)'
        self.window = customtkinter.CTk()
        self.window.title('Lab 2 GUI')
        self.window.geometry('760x620')
        self.window.minsize(600, 420)
        self.window.configure(fg_color='#260b35')

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(
            self.window,
            wrap='none',
            font=('Consolas', 14),
            fg_color='#1f1f1f',
            text_color='#f2eaff',
            border_width=0,
        )
        self.textbox.grid(row=0, column=0, padx=10, pady=(10, 8), sticky='nsew')

        self.buttons_frame = customtkinter.CTkFrame(
            self.window, fg_color='#1f1f1f', corner_radius=7
        )
        self.buttons_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        customtkinter.CTkButton(
            self.buttons_frame,
            text='Sort by Year',
            command=self.sort_by_year,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=0, padx=(9, 5), pady=9, sticky='ew')
        customtkinter.CTkButton(
            self.buttons_frame,
            text='Sort by Brand',
            command=self.sort_by_brand,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=1, padx=5, pady=9, sticky='ew')
        customtkinter.CTkButton(
            self.buttons_frame,
            text='Sort by Type',
            command=self.sort_by_type,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=2, padx=(5, 9), pady=9, sticky='ew')

        self.catalog.sort_by_year()
        self.refresh_textbox()

    def refresh_textbox(self):
        self.textbox.configure(state='normal')
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', self.catalog.as_text(self.current_sort))
        self.textbox.configure(state='disabled')

    def sort_by_year(self):
        self.catalog.sort_by_year()
        self.current_sort = 'Year (descending)'
        self.refresh_textbox()

    def sort_by_brand(self):
        self.catalog.sort_by_brand()
        self.current_sort = 'Brand (ascending)'
        self.refresh_textbox()

    def sort_by_type(self):
        self.catalog.sort_by_type()
        self.current_sort = 'Type (ascending)'
        self.refresh_textbox()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    CarApplication().run()
