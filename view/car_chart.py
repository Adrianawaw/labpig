import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CarChart(customtkinter.CTkToplevel):
    def __init__(self, master, chart_data, data_provider, statistics_provider):
        super().__init__(master)
        self.title('Car catalog chart')
        self.geometry('620x520')
        self.minsize(520, 430)
        self.transient(master)
        self.protocol('WM_DELETE_WINDOW', self._close)
        self.data_provider = data_provider
        self.statistics_provider = statistics_provider
        self.chart_kind = 'Type'
        self.animation_job = None
        self.animation_frame = 0

        self.figure = Figure(figsize=(6, 4.5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.chart_data = chart_data
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(
            fill='both', expand=True, padx=12, pady=(12, 4)
        )
        self._draw_chart('Cars by type')

        controls = customtkinter.CTkFrame(self, fg_color='transparent')
        controls.pack(fill='x', padx=12, pady=(0, 4))
        customtkinter.CTkLabel(controls, text='Chart:').pack(
            side='left', padx=(0, 8)
        )
        self.chart_menu = customtkinter.CTkOptionMenu(
            controls,
            values=['Type', 'Year', 'Model', 'Performance'],
            command=self._change_chart,
        )
        self.chart_menu.pack(side='left', fill='x', expand=True)

        customtkinter.CTkButton(
            self,
            text='Animate again',
            command=self.animate,
            fg_color='#287db5',
            hover_color='#3696d1',
        ).pack(fill='x', padx=12, pady=(4, 4))

        customtkinter.CTkButton(
            self,
            text='Close',
            command=self._close,
            fg_color='#49316b',
            hover_color='#5b3d82',
        ).pack(fill='x', padx=12, pady=(4, 12))

        self.animate()

    def _draw_chart(self, title):
        self.axes.clear()
        if self.chart_kind == 'Performance':
            self._draw_performance_chart()
            return
        labels = list(self.chart_data)
        values = list(self.chart_data.values())
        self.values = values
        self.is_model_chart = self.chart_kind == 'Model'
        if self.is_model_chart:
            self.chart_x = list(range(len(labels)))
            (self.chart_line,) = self.axes.plot(
                [], [], color='#287db5', linewidth=2, marker='o',
                markersize=6, markerfacecolor='#55b5ed',
            )
            self.axes.set_xticks(self.chart_x)
            self.axes.set_xticklabels(labels)
        else:
            self.bars = self.axes.bar(
                labels, [0] * len(values), color='#287db5'
            )

        self.axes.set_title(title)
        self.axes.set_ylabel('Number of cars')
        self.axes.set_ylim(0, max(values, default=1) + 2)
        self.axes.grid(axis='y', alpha=0.25)
        self.axes.tick_params(axis='x', labelrotation=45)
        if self.is_model_chart:
            self.axes.tick_params(axis='x', labelsize=7)
        self.figure.tight_layout()
        self.canvas.draw()

    def _draw_performance_chart(self):
        items = sorted(
            self.chart_data,
            key=lambda item: item['acceleration'],
        )
        self.performance_items = items
        self.performance_x = [item['acceleration'] for item in items]
        self.performance_y = [item['speed'] for item in items]
        fastest_index = max(
            range(len(items)),
            key=lambda index: items[index]['speed'],
            default=None,
        )
        self.performance_colors = [
            '#f4b942' if index == fastest_index else '#e76f51'
            for index in range(len(items))
        ]
        (self.performance_line,) = self.axes.plot(
            [], [], color='#f4b942', linewidth=2, alpha=0.85,
        )
        self.performance_points = self.axes.scatter(
            self.performance_x,
            self.performance_y,
            s=90,
            edgecolors='#ffffff',
            linewidths=0.8,
        )
        self.performance_points.set_facecolors([
            [0, 0, 0, 0] for _ in items
        ])
        self.performance_annotations = []
        for item in items:
            annotation = self.axes.annotate(
                item['model'],
                (0, 0),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8,
            )
            annotation.set_visible(False)
            self.performance_annotations.append(annotation)
        self.axes.set_title('Performance: speed vs acceleration')
        self.axes.set_xlabel('Acceleration (0-100 km/h, seconds)')
        self.axes.set_ylabel('Maximum speed (km/h)')
        if items:
            self.axes.set_xlim(min(self.performance_x) - 0.3, max(self.performance_x) + 0.3)
            self.axes.set_ylim(min(self.performance_y) - 15, max(self.performance_y) + 20)
        self.axes.grid(alpha=0.25)
        self.figure.tight_layout()
        self.canvas.draw()

    def animate(self):
        self._stop_animation()
        if self.chart_kind == 'Performance':
            self.performance_line.set_data([], [])
            self.performance_points.set_facecolors([
                [0, 0, 0, 0] for _ in self.performance_items
            ])
            for annotation in self.performance_annotations:
                annotation.set_visible(False)
            self.animation_frame = 0
            self.canvas.draw()
            self.animation_job = self.after(45, self._animate_frame)
            return
        if self.is_model_chart:
            self.chart_line.set_data([], [])
        else:
            for bar in self.bars:
                bar.set_height(0)
        self.animation_frame = 0
        self.canvas.draw()
        self.animation_job = self.after(35, self._animate_frame)

    def _change_chart(self, chart_kind):
        self.chart_kind = chart_kind
        titles = {
            'Type': 'Cars by type',
            'Year': 'Cars by production year',
            'Model': 'Cars by model',
            'Performance': 'Performance: speed vs acceleration',
        }
        self.chart_data = self.data_provider(chart_kind)
        self._draw_chart(titles[chart_kind])
        self.animate()

    def _animate_frame(self):
        self.animation_frame += 1
        progress = self.animation_frame / 30
        if self.chart_kind == 'Performance':
            point_count = min(
                len(self.performance_items),
                max(0, int(progress * len(self.performance_items))),
            )
            self.performance_line.set_data(
                self.performance_x[:point_count],
                self.performance_y[:point_count],
            )
            self.performance_points.set_offsets([
                [x, y] for x, y in zip(
                    self.performance_x, self.performance_y
                )
            ])
            self.performance_points.set_facecolors(
                [
                    self.performance_colors[index]
                    if index < point_count else [0, 0, 0, 0]
                    for index in range(len(self.performance_items))
                ]
            )
            for index, annotation in enumerate(self.performance_annotations):
                if index < point_count:
                    annotation.xy = (
                        self.performance_x[index],
                        self.performance_y[index],
                    )
                    annotation.set_visible(True)
        elif self.is_model_chart:
            point_count = min(
                len(self.values),
                max(1, int(progress * len(self.values))),
            )
            self.chart_line.set_data(
                self.chart_x[:point_count],
                self.values[:point_count],
            )
        else:
            for bar, value in zip(self.bars, self.values):
                bar.set_height(value * progress)
        self.canvas.draw_idle()
        if self.animation_frame < 30 and self.winfo_exists():
            self.animation_job = self.after(35, self._animate_frame)
        else:
            self.animation_job = None

    def _close(self):
        self._stop_animation()
        self.destroy()

    def _stop_animation(self):
        if self.animation_job is not None:
            self.after_cancel(self.animation_job)
            self.animation_job = None
