import customtkinter

from view.car_dialog import CarDialog
from view.car_item import CarItemFrame


class CarView:
    def __init__(self, presenter):
        self.presenter = presenter
        self.window = customtkinter.CTk()
        self.window.title('Lab 2 GUI')
        self.window.geometry('560x700')
        self.window.minsize(480, 520)
        self.window.configure(fg_color='#260b35')
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.cars_frame = customtkinter.CTkScrollableFrame(
            self.window, fg_color='#1f1f1f', corner_radius=7,
            label_text='Cars',
            label_font=('Arial', 15, 'bold'),
        )
        self.cars_frame.grid(row=0, column=0, padx=10, pady=(10, 8), sticky='nsew')
        self.cars_frame.grid_columnconfigure(0, weight=1)

        controls = customtkinter.CTkFrame(
            self.window, fg_color='#1f1f1f', corner_radius=7
        )
        controls.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(2, weight=1)

        self.sort_menu = customtkinter.CTkOptionMenu(
            controls,
            values=['Year', 'Brand', 'Type'],
        )
        self.sort_menu.grid(row=0, column=0, padx=(9, 4), pady=9, sticky='ew')

        customtkinter.CTkButton(
            controls,
            text='Sort cars',
            command=self._sort_selected,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=1, padx=4, pady=9, sticky='ew')

        customtkinter.CTkButton(
            controls,
            text='Add car',
            command=self._open_add_dialog,
            fg_color='#2d7040',
            hover_color='#3d9355',
        ).grid(row=0, column=2, padx=(4, 9), pady=9, sticky='ew')

    def show_cars(self, cars_text):
        del cars_text
        for child in self.cars_frame.winfo_children():
            child.destroy()
        for row, car in enumerate(self.presenter.model.get_cars()):
            CarItemFrame(
                self.cars_frame,
                car,
                self.presenter.remove_car,
                self._open_edit_dialog,
            ).grid(row=row, column=0, padx=8, pady=4, sticky='ew')

    def _open_add_dialog(self):
        CarDialog(self.window, self.presenter.add_car)

    def _sort_selected(self):
        commands = {
            'Year': self.presenter.sort_by_year,
            'Brand': self.presenter.sort_by_brand,
            'Type': self.presenter.sort_by_type,
        }
        commands[self.sort_menu.get()]()

    def _open_edit_dialog(self, car):
        CarDialog(self.window, self.presenter.update_car, car)

    def run(self):
        self.window.mainloop()
