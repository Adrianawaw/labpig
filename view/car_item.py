import customtkinter
from PIL import Image
from pathlib import Path


class CarItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, car, on_delete, on_edit):
        super().__init__(master, fg_color='#292929', corner_radius=7)
        self.car = car
        self.image = None

        image_path = car.get_parameters('image_path')
        if image_path and not Path(image_path).is_absolute():
            image_path = Path(__file__).resolve().parent.parent / image_path
        if image_path:
            try:
                self.image = customtkinter.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(105, 75),
                )
            except (FileNotFoundError, OSError):
                self.image = None

        if self.image is not None:
            customtkinter.CTkLabel(self, text='', image=self.image).grid(
                row=0, column=0, padx=(10, 8), pady=9, rowspan=2
            )
            text_column = 1
        else:
            text_column = 0

        car_type = car.__class__.__name__.replace('_', ' ').title()
        title_label = customtkinter.CTkLabel(
            self,
            text=f'{car.get_parameters("brand")} {car.get_parameters("model")}',
            anchor='w',
            font=('Arial', 15, 'bold'),
        )
        title_label.grid(
            row=0, column=text_column, padx=(5, 10), pady=(12, 2), sticky='sw'
        )

        description_frame = customtkinter.CTkFrame(
            self,
            fg_color='#202020',
            corner_radius=7,
        )
        description_frame.grid(
            row=1, column=text_column, padx=(5, 10), pady=(0, 10), sticky='nw'
        )

        customtkinter.CTkLabel(
            description_frame,
            text=f'{car_type}  |  Year: {car.get_parameters("year")}',
            anchor='w',
            text_color='#c8c8c8',
        ).grid(
            row=0, column=0, padx=10, pady=7, sticky='w'
        )

        actions = customtkinter.CTkFrame(self, fg_color='transparent')
        actions.grid(
            row=0, column=text_column + 1, rowspan=2,
            padx=(5, 10), pady=8, sticky='ns'
        )

        customtkinter.CTkButton(
            actions,
            text='✎',
            width=42,
            height=34,
            fg_color='#49316b',
            hover_color='#5b3d82',
            command=lambda: on_edit(self.car),
        ).grid(row=0, column=0, padx=2, pady=(0, 4))

        customtkinter.CTkButton(
            actions,
            text='✖',
            width=42,
            height=34,
            fg_color='#8f3030',
            hover_color='#b83c3c',
            command=lambda: on_delete(self.car),
        ).grid(row=1, column=0, padx=2, pady=(4, 0))
        self.grid_columnconfigure(text_column, weight=1)
