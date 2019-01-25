from math import hypot


class Node:
    def __init__(self, city_name, latitude, longitude):
        self.city_name = city_name
        self.pos = (float(latitude), float(longitude))

    def get_cityname(self):
        return self.city_name

    def get_pos(self):
        return self.pos

    #  calculate Euclidean distance of 2 cities
    def get_Euclidean_distance(self, node_s):
        a = node_s.pos[0] - self.pos[0]
        b = node_s.pos[1] - self.pos[1]
        return hypot(a, b)
