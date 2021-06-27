from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: float = 0
    y: float = 0

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise NotImplementedError(f"Addition not implemented between type Point and {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise NotImplementedError(f"Subtraction not implemented between type Point and {type(other)}")
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return round(self.x) == round(other.x) and round(self.y) == round(other.y)
        else:
            raise NotImplementedError(f"Equality not implemented between type Point and {type(other)}")

    def __neq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Polygon:

    def __init__(self, points: List[Point]):
        self.points = points


class Rectangle(Polygon):

    def __init__(self, 
        bottom_left_corner: Point,
        top_right_corner: Point):
        self.points = [
            bottom_left_corner,
            Point(bottom_left_corner.x, top_right_corner.y),
            top_right_corner,
            Point(top_right_corner.x, bottom_left_corner.y)
        ]

    def get_corners(self) -> List[Point]:
        return self.points
    
    def get_center(self) -> Point:
        return Point(
            self.bl().x + (self.tr().x - self.bl().x)/2,
            self.bl().y + (self.tr().y - self.bl().y)/2
        )
    def bl(self):
        return self.points[0]
    def tl(self):
        return self.points[1]
    def tr(self):
        return self.points[2]
    def br(self):
        return self.points[3]



class Object:

    def __init__(self, bottom_left_corner: Point, height: float, width: float):

        self.hitbox: Rectangle = Rectangle(
            bottom_left_corner, 
            bottom_left_corner + Point(width, height)
        )
        self.x, self.y = self.hitbox.get_center().x, self.hitbox.get_center().y
        self.width, self.height = width, height

    
    def update_hitbox(self):
        if (center := Point(self.x, self.y)) != self.hitbox.get_center():
            diff = center - self.hitbox.get_center()
            for i in range(len(self.hitbox.points)):
                self.hitbox.points[i] += diff