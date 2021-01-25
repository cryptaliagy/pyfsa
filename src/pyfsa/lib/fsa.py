# -*- coding: utf-8 -*-
import pygraphviz as gv  # type: ignore
import itertools as it

from typing import (
    List,
    Optional,
)

from pyfsa.lib.types import TransitionsTable


def get_state_graph(
    transitions: TransitionsTable,
    start: Optional[str] = None,
    end: Optional[str] = None,
    nodes: Optional[List[str]] = None,
    name: str = 'output.png',
    draw: bool = True,
    engine: str = 'circo',
) -> gv.AGraph:
    '''
    From a transition dictionary, creates a pygraphviz graph
    of all the possible states and how to reach the given state.

    Returns the resulting graph.
    '''
    graph = gv.AGraph(directed=True, strict=False, ranksep='1')
    key_num = it.count()
    if nodes is not None:
        graph.add_nodes_from(nodes)
    else:
        graph.add_nodes_from(transitions.keys())

    for node, transition_row in transitions.items():
        for label, targets in transition_row.items():
            for target in targets:
                graph.add_edge(
                    node,
                    target,
                    key=f'{next(key_num)}',
                    label=label,
                    weight=1,
                )

    if start:
        n: gv.Node = graph.get_node(start)
        n.attr['color'] = '#0000FF'
        n.attr['style'] = 'filled'

    if end:
        n = graph.get_node(end)
        n.attr['color'] = '#00FF00'
        n.attr['style'] = 'filled'

    if draw:
        graph.layout(prog=engine)
        graph.draw(name)

    return graph


def verify_string(
    string: str,
    starting_state: str,
    final_state: str,
    transitions: TransitionsTable,
) -> bool:
    '''
    Given a transitions table, a start and end state, and
    some string, verifies that executing the finite state machine
    on the given string produces the desired final state.
    '''
    current_state = starting_state
    for letter in string:
        transition = transitions[current_state]
        current_state = transition[letter][0]

    return current_state == final_state


def render_string_graph(
    string: str,
    start: str,
    end: str,
    transitions: TransitionsTable,
    name: str = 'output.png',
    draw: bool = True,
    engine: str = 'circo'
):
    '''
    Given a string, a start state, an end state, end a
    transitions table, produces the graph resulting in
    the traversal of the string through the states defined
    in the transitions table. By default, it will
    output a png file of the result, but that can be
    suppressed.
    '''
    graph = gv.AGraph(directed=True)

    graph.graph_attr['label'] = f'Evaluating {string}'

    node_names = it.count()
    current_state = start
    node_name = next(node_names)
    graph.add_node(node_name)
    current_node = gv.Node(graph, node_name)
    current_node.attr['label'] = current_state
    current_node.attr['fillcolor'] = '#0000FF'
    current_node.attr['style'] = 'filled'

    for letter in string:
        node_name = next(node_names)
        graph.add_node(node_name)
        next_node = gv.Node(graph, node_name)
        # TODO: The algorithm prioritizes just the first
        # found state, which may not produce a correct
        # answer. Needs to fix this
        next_state = transitions[current_state][letter][0]
        next_node.attr['label'] = next_state
        graph.add_edge(current_node, next_node, label=letter)
        current_node = next_node
        current_state = next_state

    if current_state == end:
        current_node.attr['style'] = 'filled'
        current_node.attr['fillcolor'] = '#00FF00'

    if draw:
        graph.layout(prog=engine)
        graph.draw(name)

    return graph
