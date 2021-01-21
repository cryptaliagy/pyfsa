import csv
import pathlib as plb

from collections import defaultdict
from typing import (
    Dict,
    List,
)

from pyfsa.lib.types import TransitionsTable


def convert_csv_file(file_name: str) -> TransitionsTable:
    '''
    Reads a CSV file in the form of 'trigger,source,target' and
    produces a TransitionsTable. This object will be workable
    with the methods provided in the 'fsa' module.
    '''
    file_path = plb.Path(file_name)
    if not file_path.exists():
        return {}

    output: TransitionsTable = defaultdict(lambda: {})

    with file_path.open() as f:
        reader = csv.DictReader(f)

        for row in reader:
            source = row['source']
            trigger = row['trigger']
            target = row['target']

            src_dict = output[source]
            src_dict[trigger] = target

    return output


def convert_transitions(
    transitions: TransitionsTable
) -> List[Dict[str, str]]:
    '''
    Converts a TransitionsTable dictionary into a
    list of dictionaries that describe the role of each
    element. Used to dump a given transitions table
    in the internal representation into something a little
    friendlier to write in csv
    '''
    output = []

    for source in transitions.keys():
        for trigger, target in transitions[source].items():
            output.append({
                'trigger': trigger,
                'source': source,
                'target': target
            })

    return output


def transitions_to_csv(
    transitions: TransitionsTable,
    file_name: str
):
    '''
    Given a TransitionsTable, outputs a file with the
    components converted into a CSV format.
    '''
    field_names = ['trigger', 'source', 'target']
    with open(file_name) as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows(
            convert_transitions(transitions)
        )
