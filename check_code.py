class Shape:
    def __init__(self, color):
        self.color = color

    def display_shape(self):
        print("Type: Shape")
    @classmethod
    def create_shape(clsaaawwq, color, type):
        if type == "circle":
            return clsaaawwq(color)
            # return Circle(color)
        elif type == "rectangle":
            return Rectangle(color)

class Circle(Shape):
    def display_shape(self):
        print("Type: Circle")

class Rectangle(Shape):
    def display_shape(self):
        print("Type: Rectangle")

circle = Shape.create_shape("red", "circle")
circle.display_shape()  # Output: Type: Circle