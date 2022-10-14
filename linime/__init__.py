from gi import require_version

require_version("Gtk", "3.0")
from gi.repository import Gtk as gui, GLib as fns
import cairo, math
from time import sleep


class DrawingArea(gui.Frame):

    def __init__(self, w=10, h=10, border_width=0):
        super().__init__()
        self.set_border_width(border_width)
        self.set_size_request(w, h)
        self.width = w
        self.height = h
        self.vexpand = True
        self.hexpand = True
        self.surface = None

        self.area = gui.DrawingArea()
        self.area.set_size_request(self.width, self.height)
        self.add(self.area)

    def init_surface(self, area):
        if self.surface is not None:
            self.surface.finish()
            self.surface = None

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          area.get_allocated_width(),
                                          area.get_allocated_height())

    def redraw(self):
        self.init_surface(self.area)
        context = cairo.Context(self.surface)
        context.scale(self.surface.get_width(), self.surface.get_height())
        self.__draw__(self.area, context)
        self.surface.flush()


class Root(gui.Window):

    def __init__(self, h, w) -> None:
        super().__init__()
        gui.init()

    def __show__(self) -> None:
        self.show_all()
        self.connect("destroy", gui.main_quit)
        gui.main()


class Scene(DrawingArea):

    def __init__(self) -> None:
        self.height = 400
        self.width = 400
        super().__init__(h=self.height, w=self.width)
        self.window = Root(self.height, self.width)
        self.window.add(self)
        self.draw_list = []

    def __start__(self):
        self.area.connect("draw", self.__draw__)
        fns.timeout_add(30, self.__update__)
        self.window.__show__()

    def __update__(self) -> bool:
        rect = self.get_allocation()
        self.get_window().invalidate_rect(rect, True)
        return True

    def __show__(self, context):
        for obj in self.draw_list:
            obj.__draw__(context)

    def __draw__(self, area, context):
        if any(self.queue): self.__queue__(context)
        else: self.__show__(context)

    def __queue__(self, context):
        transition = self.queue[0]
        if transition[0] == "pause":
            sleep(transition[1])
            self.queue.pop(0)
            self.__show__(context)
            return

        elif len(transition) != 4:
            for i in transition:
                obj, prop, start, end = i
                if (obj.__transition__(prop, start, end) != 1):
                    if obj not in self.draw_list: self.draw_list.append(obj)
                    self.__show__(context)
                    continue
                else:
                    self.queue.pop(0)
                    self.__show__(context)
                    continue
            return
        
        obj, prop, start, end = transition
        if (obj.__transition__(prop, start, end) != 1):
            if obj not in self.draw_list: self.draw_list.append(obj)
            self.__show__(context)
            return
        else:
            self.queue.pop(0)
            self.__show__(context)
            return


class Item:

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.opacity: float = 1
        self.background_color = (224, 57, 45)

        self.border_width = 5
        self.border_color = (242, 75, 63)

        self.transition_dur = 4

    def __properties__(self, *args):
        for i in range(len(args), __step=2):
            self.__setattr__(args[i], args[i] + 1)

    def __transition__(self, property, start, end) -> int:
        if end > start and end - getattr(
                self, property) > (self.transition_dur * (end - start) /
                                   (end + start) / 100) * end:
            setattr(
                self, property,
                getattr(self, property) +
                (self.transition_dur * (end - start) /
                 (end + start) / 100) * end)
        elif start > end and end - getattr(
                self, property) < (self.transition_dur * (start - end) /
                                   (end + start) / 100) * start:
            setattr(
                self, property,
                getattr(self, property) -
                (self.transition_dur * (start - end) /
                 (end + start) / 100) * start)
        else:
            return 1


class Rectangle(Item):

    def __init__(self) -> None:
        super().__init__()
        self.height = 100
        self.width = 100

    def __draw__(self, context) -> None:
        context.rectangle(self.x, self.y, self.width, self.height)
        context.set_source_rgba(self.background_color[0] / 255,
                                self.background_color[1] / 255,
                                self.background_color[2] / 255, self.opacity)
        context.fill()
        context.rectangle(self.x + self.border_width / 2,
                          self.y + self.border_width / 2, self.width,
                          self.height)
        context.set_source_rgba(self.border_color[0] / 255,
                                self.border_color[1] / 255,
                                self.border_color[2] / 255, self.opacity)
        context.set_line_width(self.border_width)
        context.stroke()


class RoundedRectangle(Item):

    def __init__(self) -> None:
        super().__init__()
        self.height = 100
        self.width = 100
        self.radius = 10

    def __draw__(self, context) -> None:
        context.arc(self.x + self.radius, self.y + self.radius, self.radius,
                    math.pi, 3 * math.pi / 2)

        context.arc(self.x + self.width - self.radius, self.y + self.radius,
                    self.radius, 3 * math.pi / 2, 0)

        context.arc(self.x + self.width - self.radius,
                    self.y + self.height - self.radius, self.radius, 0,
                    math.pi / 2)

        context.arc(self.x + self.radius, self.y + self.height - self.radius,
                    self.radius, math.pi / 2, math.pi)

        context.close_path()
        context.set_source_rgba(self.background_color[0] / 255,
                                self.background_color[1] / 255,
                                self.background_color[2] / 255, self.opacity)
        context.fill()
        context.arc(self.x + self.radius, self.y + self.radius, self.radius,
                    math.pi, 3 * math.pi / 2)

        context.arc(self.x + self.width - self.radius, self.y + self.radius,
                    self.radius, 3 * math.pi / 2, 0)

        context.arc(self.x + self.width - self.radius,
                    self.y + self.height - self.radius, self.radius, 0,
                    math.pi / 2)

        context.arc(self.x + self.radius, self.y + self.height - self.radius,
                    self.radius, math.pi / 2, math.pi)

        context.close_path()
        context.set_source_rgba(self.border_color[0] / 255,
                                self.border_color[1] / 255,
                                self.border_color[2] / 255, self.opacity)
        context.set_line_width(self.border_width)
        context.stroke()


class Text(Item):

    def __init__(self) -> None:
        super().__init__()
        self.text = ""
        self.font_size = 25
        self.font_weight = 3
        self.height = 40

    def __draw__(self, context) -> None:
        context.set_font_size(self.font_size)
        context.set_source_rgba(self.background_color[0] / 255,
                                self.background_color[1] / 255,
                                self.background_color[2] / 255, self.opacity)
        context.move_to(self.x, self.y + self.height / 2)
        context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
        context.show_text(self.text)
        context.set_line_width(self.font_weight)
        context.stroke()


class Circle(Item):

    def __init__(self) -> None:
        super().__init__()
        self.radius = 20

    def __draw__(self, context) -> None:
        context.set_source_rgba(self.background_color[0] / 255,
                                self.background_color[1] / 255,
                                self.background_color[2] / 255, self.opacity)
        context.arc(self.x + self.radius, self.y+self.radius, self.radius, 0, 2 * math.pi)
        context.fill()
        context.set_source_rgba(self.border_color[0] / 255,
                                self.border_color[1] / 255,
                                self.border_color[2] / 255, self.opacity)
        context.arc(self.x + self.radius, self.y+self.radius, self.radius, 0, 2 * math.pi)
        context.set_line_width(self.border_width)
        context.stroke()