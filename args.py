#!/usr/bin/env python
# encoding: utf-8

import argparse


def restricted_float(x):
    #Define a restricted float data type in interval (0, 1].
    x = float(x)
    if x <= 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range (0.0, 1.0]"%(x,))
    return x


def parse_args():
    """Parse user arguments

    Returns
    -------
    args : Namespace object with user arguments
    nargs : Number of user arguments
    """
    parser = argparse.ArgumentParser(description=
                                     "Multi-criteria optimization algorithm")
    parser.add_argument("-a", type=restricted_float,
                        help="Average latency - failure free scenario. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("-w", type=restricted_float,
                        help="Worst case latency - failure free scenario. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("-i", type=restricted_float,
                        help="Inter controller latency. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("--dynamic", help="Generate dynamic undirected graph",
                        action="store_true")
    parser.add_argument("-n", type=int, help="Number of graph nodes")
    parser.add_argument("-c", type=int, help="Number of controllers in graph. "
                        "Allowed values are between N/3 and N/7")
    #parser.add_argument("-c", "--controlers", dest="controlers", metavar="C",
                         #default=2, type=int, help="Number of controlers")
    args = parser.parse_args()
    if not (args.a or args.w or args.i):
        raise parser.error("No action requested, add -a or -w or -i option")
    # nr of args
    nargs = 0
    if args.a:
        nargs = nargs + 1
    if args.w:
        nargs = nargs + 1
    if args.i:
        nargs = nargs + 1

    return args, nargs
