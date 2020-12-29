
from operator import itemgetter
from typing import List


class Distance(object):
    def __init__(self):
        self.scale_factor = 2000

    def distance_square(self, x0: float, y0: float, x1: float, y1: float) -> float:
        """Return the squarded distance between two points"""
        dx: float = x1 - x0
        dy: float = y1 - y0
        dx *= dx
        dy *= dy
        return dx + dy
    
    def euclidean_distance(self, x0, y0, x1, y1) -> float:
        """return euclidean_distance between two points"""
        return (self.distance_square(x0, y0, x1, y1) * 0.5) * self.scale_factor
    
    def mahattan_distance(self, x0, y0, x1, y1) -> float:
        """return manhattan distance between two points"""
        dx: float = abs(x1 - x0)
        dy: float = abs(y1 - y0)
        return (dx + dy) * self.scale_factor

    def find_nearest_point(self, point_list: List[tuple], point_to_find: tuple, number: int):
        distances = []
        for point in point_list:
            distances.append([point, self.euclidean_distance(point[0], point[1], point_to_find[0], point_to_find[1])])
        distances = sorted(distances, key=itemgetter(1))
        distances = [i.pop(0) for i in distances]
        return distances[0:number]
