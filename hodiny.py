import tkinter as tk
from datetime import datetime

root = tk.Tk()

canvas = tk.Canvas(root, height=500, width=1200, bg="black")
canvas.pack()


class Line:
    def __init__(self, point: tuple, dx: int, dy: int, color: str, canvas):
        self.coords = point
        self.dx = dx
        self.dy = dy
        self.color = color
        self.canvas = canvas
        if dx == dy:
            self.id = canvas.create_rectangle(point[0], point[1], point[0] + dx, point[1] + dy, fill = color, outline = "")
        elif dx < dy:
            self.id = canvas.create_polygon(point[0], point[1], point[0] + dx // 2, point[1] - dx // 2 , point[0] + dx, point[1], point[0] + dx, point[1] + dy, point[0] + dx // 2, point[1] + dy + dx // 2, point[0], point[1] + dy,fill=color, outline="black")
        if dx > dy:
            self.id = canvas.create_polygon(point[0], point[1], point[0] + dx, point[1], point[0] + dx + dy // 2, point[1] + dy // 2, point[0] + dx, point[1] + dy, point[0], point[1] + dy, point[0] - dy // 2, point[1] + dy // 2,fill=color, outline="black")

    def on(self):
        self.canvas.itemconfig(self.id, fill = self.color)

    def off(self):
        self.canvas.itemconfig(self.id, fill = "black")


class Segment:
    def __init__(self, point: tuple, small: int, big: int, color: str, canvas):
        self.parts = []
        self.canvas = canvas
        self.big = big
        self.small = small
        self.coords = point
        self.color = color
        sx = point[0]
        sy = point[1]
        self.parts.append(Line((sx + small, sy), big, small, color, canvas))
        self.parts.append(Line((sx + small + big, sy + small), small, big, color, canvas))
        self.parts.append(Line((sx + small, sy + big + small), big, small, color, canvas))
        self.parts.append(Line((sx, sy + small), small, big, color, canvas))
        self.parts.append(Line((sx + small + big, sy + 2*small + big), small, big, color, canvas))
        self.parts.append(Line((sx + small, sy + 2 * big + 2 * small), big, small, color, canvas))
        self.parts.append(Line((sx, sy + 2 * small + big), small, big, color, canvas))
    
    def reset(self):
        for i in self.parts:
            i.off()
    
    def error(self):
        for i in self.parts:
            i.on()
    
    def display(self, number: int):
        match str(number):
            case '0':
                self.error()
                self.parts[2].off()
            case '1':
                self.reset()
                self.parts[1].on()
                self.parts[4].on()
            case '2':
                self.reset()
                self.parts[0].on()
                self.parts[1].on()
                self.parts[2].on()
                self.parts[6].on()
                self.parts[5].on()
            case '3':
                self.error()
                self.parts[3].off()
                self.parts[6].off()
            case '4':
                self.error()
                self.parts[0].off()
                self.parts[6].off()
                self.parts[5].off()
            case '5':
                self.error()
                self.parts[1].off()
                self.parts[6].off()
            case '6':
                self.error()
                self.parts[1].off()
            case '7':
                self.reset()
                self.parts[0].on()
                self.parts[1].on()
                self.parts[4].on()
            case '8':
                self.error()
            case '9':
                self.error()
                self.parts[6].off()
            case _:
                pass


class Clock:
    def __init__(self, canvas):
        self.canvas = canvas
        self.segments = []
        space = 0.4
        self.dvojbodka = []
        for i in range(6):
            x = i * (140 + space * 140)
            y = 100
            segment = Segment((x+30, y), 20, 100, "magenta", canvas)
            self.segments.append(segment)
            if i == 3 or i == 1:
                col_1 = Line((x + 190,y + 140), 20, 20, "magenta", canvas)
                col_2 = Line((x + 190,y + 100), 20, 20, "magenta", canvas)
                col_1.on()
                col_2.on()
                self.dvojbodka.append(col_1)
                self.dvojbodka.append(col_2)

    def r(self):
        current_time = datetime.now().strftime("%H%M%S")
        for i in range(6):
            digit = int(current_time[i])
            self.segments[i].display(digit)
        if int(current_time[-1]) % 2 == 0:
            for i in self.dvojbodka:
                i.on()
        else:
            for i in self.dvojbodka:
                i.off()
        root.after(1000, self.r)


skuska = Clock(canvas)
skuska.r()

root.mainloop()
