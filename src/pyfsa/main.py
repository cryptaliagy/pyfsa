import click

import pyfsa.lib.csv_convert as csv
import pyfsa.lib.fsa as fsa


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True),
    help='CSV file containing definition of state tables',
    required=True
)
@click.option(
    '-s',
    '--start',
    type=str,
    help='The starting state. Cannot be the same as end state.',
)
@click.option(
    '-e',
    '--end',
    type=str,
    help='The end state. Cannot be the same as start state.'
)
@click.argument(
    'output_file',
    type=str,
    required=False,
)
def state(
    file: str,
    start: str,
    end: str,
    output_file: str,
):
    '''
    Renders finite state automata graphs from csv files.

    The CSV files must be in the form 'trigger,source,target'.
    If you provide an optional filename argument, the file
    will render as that, but otherwise it will use
    'output.png' as default.
    '''
    transitions = csv.convert_csv_file(file)
    if output_file:
        name = output_file
    else:
        name = 'output.png'
    click.echo('Rendering state graph... ', nl=False)
    fsa.get_state_graph(
        transitions,
        start_state=start,
        final_state=end,
        name=name
    )
    click.secho('DONE', bg='green')


@main.command()
@click.option(
    '-f',
    '--file',
    type=click.Path(exists=True),
    help='CSV file containing definition of state tables',
    required=True
)
@click.option(
    '-s',
    '--start',
    type=str,
    help='The starting state. Cannot be the same as end state.',
    required=True,
)
@click.option(
    '-e',
    '--end',
    type=str,
    help='The end state. Cannot be the same as start state.',
    required=True,
)
@click.option(
    '-o',
    '--output',
    help='The output file to render the traversal graph, if desired',
    type=str,
    required=False,
)
@click.argument(
    'string',
    type=str,
    required=True
)
def string(
    file: str,
    start: str,
    end: str,
    output: str,
    string: str,
):
    '''
    Verifies that the provided string is valid given a
    finite state machine provided in csv format.

    The csv file should be in the format
    'trigger,source,target'.

    If an output file name is given, it will also render
    a traversal graph of the string in the machine.
    '''
    transitions = csv.convert_csv_file(file)

    if output:
        fsa.render_string_graph(
            string,
            start,
            end,
            transitions,
            output
        )

    if fsa.verify_string(
        string,
        start,
        end,
        transitions
    ):
        click.echo(
            f'The string {string} reaches the desired output '
            'based on the transitions defined in the file '
            f'{file}.'
        )
    else:
        click.echo(
            f'The string {string} does not reach the desired '
            'output based on the transitions defined in '
            f'the file {file}.'
        )


if __name__ == '__main__':  # pragma: no cover
    main()
