import signal
import sys
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        """
        Инициализация приложения рисования.

        :param root: Корневое окно приложения.
        """
        self.brush_size_var = None
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.previous_color = 'black'  # Инициализация previous_color
        self.brush_size = 1  # Начальный размер кисти

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса, включая кнопки управления.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10]
        self.brush_size_var = tk.StringVar(value=str(sizes[0]))
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *map(str, sizes),
                                        command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        back_color_button = tk.Button(control_frame, text="Назад к цвету", command=self.back_to_previous_color)
        back_color_button.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

    def update_brush_size(self, size):
        self.brush_size = int(size)

    def use_eraser(self):
        self.previous_color = self.pen_color
        self.pen_color = 'white'

    def back_to_previous_color(self):
        self.pen_color = self.previous_color

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.brush_size,
                                    fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, _event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        new_color = colorchooser.askcolor(color=self.pen_color)[1]
        if new_color:
            self.previous_color = self.pen_color
            self.pen_color = new_color

    def save_image(self):
        """
        Сохранение текущего изображения в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def signal_handler(_signum, _frame):
    print("Работа прервана, рисунок не сохранён.")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    root = tk.Tk()
    DrawingApp(root)
    try:
        root.mainloop()
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
