import linime, numpy as np, math

class scene(linime.Scene):

    def  __init__(self):
        super().__init__()
        
        self.rect = linime.RoundedRectangle() 
        self.rect.height = 100 
        self.rect.width = 200 
        self.rect.x = 10 
        self.rect.y = 10 
        self.rect.opacity = 1 
 
        self.text = linime.Circle() 
        self.text.x = 150 
        self.text.y = 10 
        self.text.radius = 40 
        self.text.opacity = 0.01 
 
        self.queue = [((self.rect, 'x', 10, 100), (self.rect, 'y', 10, 150), ),('pause', 2),(self.text, 'opacity', 0.01, 1), ]

        self.__start__()

    def __draw__(self, area, context):
        
        if any(self.queue): self.__queue__(context)
        else: self.__show__(context)

        self.text.__draw__(context)

scene()