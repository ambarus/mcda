#!/usr/bin/env python
# encoding: utf-8

from __future__ import division


def average_latency(g_path_len, ci_dict):
    """Average latency for a graph and a specific Ci controller placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci_dict : particular placement of controllers. Dictionary is keyed by node
              and has value int(1) if controller identifies with keyed node.

    Returns
    ------
    Average latency for a graph and a specific Ci controller placement
    """
    avg = 0
    for src, dst_dict in g_path_len.iteritems():
        # list of costs from source to Ci domain
        src_ci_cost = []
        for dst, cost in dst_dict.iteritems():
            if dst in ci_dict:
                if ci_dict[dst]:
                    src_ci_cost.append(cost)
        avg = avg + min(src_ci_cost)

    return avg / len(g_path_len)

def worst_latency(g_path_len, ci):
    """Source to controller worst case latency for a graph and a specific
    Ci controller placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci : particular placement of controllers. Dictionary is keyed by node and
         has value int(1) if controller identifies with keyed node.

    Returns
    ------
    Source to controller worst case latency for a graph and a specific
    Ci controller placement
    """
    # list of minimum lengths from sources to Ci domain
    s_ci_min_len = []
    for source, s_value in g_path_len.iteritems():
        # list of lengths from source to Ci domain
        s_ci_len = []
        for target, t_value in s_value.iteritems():
            if target in ci:
                if ci[target]:
                    s_ci_len.append(t_value)
        s_ci_min_len.append(min(s_ci_len))

    return max(s_ci_min_len)

def inter_controller_latency(g_path_len, ci):
    """Inter controller latency for a graph and a specific Ci controller
    placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci : particular placement of controllers. Dictionary is keyed by node and
         has value int(1) if controller identifies with keyed node.

    Returns
    -------
    Inter controller latency for a graph and a specific Ci controller placement
    """
    icl_path_len = []
    for source, s_value in g_path_len.iteritems():
        if source in ci:
                if ci[source]:
                    for target, t_value in s_value.iteritems():
                        if target in ci:
                            if ci[target]:
                                icl_path_len.append(g_path_len[source][target])
                    # compute only 1:N controller-to-controllers distances
                    break

    return max(icl_path_len)

def normalize_dparam(dparam, weight, r, a):
    """Normalize decision parameter

    Parameters
    ----------
    dparam : decision parameter
    weght : weight of decision parameter
    r : reservation level
    a : aspiration level

    Returns
    -------
    Normalized decision variable.
    """
    return weight * (r - dparam) / (r - a)
