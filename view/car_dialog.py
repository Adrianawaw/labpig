import customtkinter
import os
from tkinter import filedialog

from model.off_road import off_road
from model.sedan import Sedan
from model.sport_car import sport_car


class CarDialog(customtkinter.CTkToplevel):
    def __init__(self, master, on_save, car=None):
        super().__init__(master)
        self.on_save = on_save
        self.car = car
        self.edit_mode = car is not None
        self.title('Edit car' if self.edit_mode else 'Add car')
        self.geometry('390x570')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.entries = {}
        self.image_path = ''
        self.type_menu = customtkinter.CTkOptionMenu(
            self,
            values=['Sedan', 'Off-road', 'Sport car'],
            command=self._show_specific_fields,
        )
        self.type_menu.pack(fill='x', padx=20, pady=(20, 10))

        self.fields_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.fields_frame.pack(fill='both', expand=True, padx=20)
        car_type = self._car_type() if self.edit_mode else 'Sedan'
        self.type_menu.set(car_type)
        self._show_specific_fields(car_type)
        if self.edit_mode:
            self._populate_fields()
            self.type_menu.configure(state='disabled')
            self.image_path = car.get_parameters('image_path') or ''

        image_name = os.path.basename(self.image_path) if self.image_path else 'No image selected'
        self.image_label = customtkinter.CTkLabel(self, text=image_name)
        self.image_label.pack(pady=(0, 5))
        customtkinter.CTkButton(
            self,
            text='Choose image',
            command=self._choose_image,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).pack(fill='x', padx=20, pady=(0, 10))

        customtkinter.CTkButton(
            self,
            text='Save changes' if self.edit_mode else 'Add car',
            command=self._save,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).pack(fill='x', padx=20, pady=(10, 20))

    def _show_specific_fields(self, car_type):
        for child in self.fields_frame.winfo_children():
            child.destroy()
        self.entries = {}

        fields = [
            ('brand', 'Brand'),
            ('model', 'Model'),
            ('year', 'Year'),
        ]
        if car_type == 'Sedan':
            fields.extend([
                ('doors', 'Doors'),
                ('type_suspension', 'Suspension type'),
                ('passenger_capacity', 'Passenger capacity'),
            ])
        elif car_type == 'Off-road':
            fields.extend([
                ('clearance_mm', 'Clearance (mm)'),
                ('transmision_type', 'Transmission type'),
            ])
        else:
            fields.extend([
                ('max_speed', 'Maximum speed'),
                ('acceleration', 'Acceleration'),
                ('brake_type', 'Brake type'),
            ])

        for row, (name, label) in enumerate(fields):
            customtkinter.CTkLabel(
                self.fields_frame, text=label, anchor='w'
            ).grid(row=row, column=0, padx=5, pady=5, sticky='w')
            entry = customtkinter.CTkEntry(self.fields_frame)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
            self.entries[name] = entry

        if car_type == 'Off-road':
            self.lock_var = customtkinter.BooleanVar(value=True)
            customtkinter.CTkCheckBox(
                self.fields_frame,
                text='Differential lock',
                variable=self.lock_var,
            ).grid(row=len(fields), column=0, columnspan=2, padx=5, pady=8, sticky='w')
        self.fields_frame.grid_columnconfigure(1, weight=1)

    def _save(self):
        try:
            values = {name: entry.get().strip() for name, entry in self.entries.items()}
            if not values['brand'] or not values['model']:
                raise ValueError('Brand and model are required.')
            values['year'] = int(values['year'])
            car_type = self.type_menu.get()

            if self.edit_mode:
                self.car.set_parameters('brand', values['brand'])
                self.car.set_parameters('model', values['model'])
                self.car.set_parameters('year', values['year'])
                self.car.set_parameters('image_path', self.image_path)
                self.on_save(self.car)
                self.destroy()
                return
            if car_type == 'Sedan':
                car = Sedan(
                    values['brand'], values['model'], values['year'],
                    int(values['doors']), values['type_suspension'],
                    int(values['passenger_capacity']),
                )
            elif car_type == 'Off-road':
                car = off_road(
                    values['brand'], values['model'], values['year'],
                    int(values['clearance_mm']), values['transmision_type'],
                    self.lock_var.get(),
                )
            else:
                car = sport_car(
                    values['brand'], values['model'], values['year'],
                    int(values['max_speed']), float(values['acceleration']),
                    values['brake_type'],
                )
            car.set_parameters('image_path', self.image_path)
        except (KeyError, TypeError, ValueError):
            self._show_error('Enter valid values for all fields.')
            return

        self.on_save(car)
        self.destroy()

    def _car_type(self):
        class_name = self.car.__class__.__name__
        return {
            'Sedan': 'Sedan',
            'off_road': 'Off-road',
            'sport_car': 'Sport car',
        }[class_name]

    def _populate_fields(self):
        for name, entry in self.entries.items():
            value = self.car.get_parameters(name)
            if value is not None:
                entry.insert(0, str(value))

    def _choose_image(self):
        path = filedialog.askopenfilename(
            title='Choose car image',
            filetypes=[
                ('Image files', '*.png *.jpg *.jpeg *.webp'),
                ('All files', '*.*'),
            ],
        )
        if path:
            self.image_path = path
            self.image_label.configure(text=os.path.basename(path))

    def _show_error(self, message):
        customtkinter.CTkLabel(
            self,
            text=message,
            text_color='#ff7777',
        ).pack(pady=(0, 10))
