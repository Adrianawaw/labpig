import customtkinter


class CarView:
    def __init__(self, presenter):
        self.presenter = presenter
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
            text_color='#ffffff',
            border_width=0,
        )
        self.textbox.grid(row=0, column=0, padx=10, pady=(10, 8), sticky='nsew')

        buttons_frame = customtkinter.CTkFrame(
            self.window, fg_color='#1f1f1f', corner_radius=7
        )
        buttons_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        customtkinter.CTkButton(
            buttons_frame,
            text='Sort by Year',
            command=lambda: self.presenter.sort_by_year(),
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=0, padx=(9, 5), pady=9, sticky='ew')
        customtkinter.CTkButton(
            buttons_frame,
            text='Sort by Brand',
            command=lambda: self.presenter.sort_by_brand(),
            fg_color='#49316b',
            hover_color='#11FF31',
        ).grid(row=0, column=1, padx=5, pady=9, sticky='ew')
        customtkinter.CTkButton(
            buttons_frame,
            text='Sort by Type',
            command=lambda: self.presenter.sort_by_type(),
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).grid(row=0, column=2, padx=(5, 9), pady=9, sticky='ew')

    def show_cars(self, cars_text):
        self.textbox.configure(state='normal')
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('1.0', cars_text)
        self.textbox.configure(state='disabled')

    def run(self):
        self.window.mainloop()
