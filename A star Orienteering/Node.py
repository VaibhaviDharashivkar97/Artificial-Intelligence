from filecmp import cmp
import sys


class Node:
    def __init__(self, x, y, rgba, elevation):
        self.x = x
        self.y = y
        self.rgba = rgba
        self.elevation = elevation
        self.f = 0
        self.g = 0
        self.h = 0
        self.m = 0
        self.parent = None

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " pixel: " + ",".join(
            map(str, self.rgba)) + " elevation: " + self.elevation

    def __lt__(self, obj):
        """self < obj."""
        return self.f < obj.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # def __le__(self, obj):
    #     """self <= obj."""
    #     return (self.f) <= (obj.f)
    #
    # def __eq__(self, obj):
    #     """self == obj."""
    #     return (self.f) == (obj.f)
    #
    # def __ne__(self, obj):
    #     """self != obj."""
    #     return (self.f) != (obj.f)
    #
    # def __gt__(self, obj):
    #     """self > obj."""
    #     return (self.f) > (obj.f)
    #
    # def __ge__(self, obj):
    #     """self >= obj."""
    #     return (self.f) >= (obj.f)

    def __hash__(self):
        return hash((self.x, self.y))

# n1 = Node(1,2,Node (-1,0,None))
# print(n1.x)
