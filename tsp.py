#!/usr/bin/env python3
import argparse
from sys import stderr
from csv import reader
from resource import getrusage, RUSAGE_SELF
from Node import Node
from Graph import Nearest, Two_Opt, Nearest_Insert


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument("--algo", default='Nearest')
    return parser.parse_args()


def read_csv(filename):
    try:
        with open(filename, 'r') as f:
            return [Node(city, lat, long) for city, lat, long in reader(f)]
    except Exception:
        stderr.write("Invalid file\n")


def create_graph(algo):
    if algo == 'Two_Opt':
        return Two_Opt()
    elif algo == 'Nearest_Insert':
        return Nearest_Insert()
    elif algo == 'Nearest':
        return Nearest()
    else:
        return


def main():
    arg = parser()
    graph = create_graph(arg.algo)
    if graph is not None:
        graph.set_lst(read_csv(arg.filename))
        res = graph.find_shortest_path()
        res.print_result()
        print('Time cost: ', getrusage(RUSAGE_SELF)[0])


if __name__ == '__main__':
    main()
