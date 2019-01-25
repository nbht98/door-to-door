from sys import maxsize
from Node import Node
from abc import abstractmethod
from random import choice


class Graph:
    def __init__(self, lst=None):
        if lst is None:
            self.lst = []
        else:
            self.lst = lst

    def __len__(self):
        return len(self.lst)

    def set_lst(self, lst):
        self.lst = lst

    def get_lst(self):
        return self.lst

    #  get min distance from 1 city to all of the city
    #  input: node of 1 city
    #  output: node of the city whose's distance is minimum to input
    def get_min_distance(self, node):
        min = maxsize
        tmpnode = node
        lst = self.lst
        for i in lst:
            tmp = node.get_Euclidean_distance(i)
            if tmp < min:
                min = tmp
                tmpnode = i
        return tmpnode

    #  get sum distance of all city in graph
    def get_sum_distance(self):
        sum = 0
        lst = self.lst
        for i in range(len(lst) - 1):
            sum += lst[i].get_Euclidean_distance(lst[i+1])
        return sum

    # print result: sum distance and number of cities
    def print_result(self):
        for i, j in enumerate(self.get_lst()):
            if i != len(self) - 1:
                print(j.get_cityname(), end=' -> ')
            else:
                print(j.get_cityname())
        print('Sum distance: ', self.get_sum_distance())
        print('Number of cities: ', len(self))

    @abstractmethod
    def find_shortest_path(self):
        pass


class Nearest(Graph):

    def __init__(self, lst=None):
        super().__init__(self)

    #  find the shortest part by nearest-neighbor
    #  from 1 city find the nearest city of it and append to res lst
    #  remove already appended city from main lst
    #  continue until main lst is empty
    def get_nearest_path(self):
        res = [self.lst[0]]
        next_city = self.lst[0]
        self.lst.remove(next_city)
        n = len(self)
        while n > 0:
            next_city = self.get_min_distance(next_city)
            res.append(next_city)
            self.lst.remove(next_city)
            n = n - 1
        return res

    def find_shortest_path(self):
        res = Graph(self.get_nearest_path())
        return res


class Nearest_Insert(Graph):

    def __init__(self, lst=None):
        super().__init__(self)

    def get_insertion_metric(self, node, first, second):
        a = node.get_Euclidean_distance(first)
        b = node.get_Euclidean_distance(second)
        c = first.get_Euclidean_distance(second)
        return a + b - c

    def get_nearest_insert(self):
        res = [self.lst[0]]
        next_city = self.lst[0]
        self.lst.remove(next_city)
        next_city = self.get_min_distance(next_city)
        res.append(next_city)
        self.lst.remove(next_city)
        n = len(self)
        insert_index = 1
        while n > 0:
            next_city = self.get_min_distance(next_city)
            tmp1 = self.get_insertion_metric(next_city, res[0], res[1])
            tmp2 = self.get_insertion_metric(res[len(res) - 1],
                                             res[len(res) - 2], next_city)
            if tmp1 < tmp2:
                insert_index = 1
                minimized_metric = tmp1
            else:
                insert_index = len(res)
                minimized_metric = tmp2
            for i in range(len(res) - 1):
                metric = self.get_insertion_metric(next_city, res[i], res[i+1])
                if metric <= minimized_metric:
                    insert_index = i + 1
                    minimized_metric = metric
            res.insert(insert_index, next_city)
            self.lst.remove(next_city)
            n = n - 1
        return res

    def find_shortest_path(self):
        res = Graph(self.get_nearest_insert())
        return res


class Two_Opt(Graph):

    def __init__(self, lst=None):
        super().__init__(self)

    def two_opt(self):
        #  Using nearest neighbor
        res = [self.lst[0]]
        next_city = self.lst[0]
        self.lst.remove(next_city)
        n = len(self)
        while n > 0:
            next_city = self.get_min_distance(next_city)
            res.append(next_city)
            self.lst.remove(next_city)
            n = n - 1
        #  Optimize by two-opt
        route = res
        best = route
        improved = True
        while improved:
            improved = False
            for i in range(len(best)):
                for j in range(i+1, len(best)):
                    if j - i == 1:
                        continue
                    tmp1 = Graph(route[i-1:j+1])
                    tmp2 = Graph([route[i-1]] + route[j-1:i-1:-1] + [route[j]])
                    if tmp1.get_sum_distance() > tmp2.get_sum_distance():
                        new_route = route[:]
                        # this is the 2woptSwap
                        new_route[i:j] = route[j-1:i-1:-1]
                        if Graph(new_route).get_sum_distance() <\
                           Graph(best).get_sum_distance():
                            best = new_route
                            improved = True
                if improved:
                    break
            route = best
        return best

    def find_shortest_path(self):
        res = Graph(self.two_opt())
        return res
