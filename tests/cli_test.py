import pytest
import unittest.mock as mock
import pathlib as plb

import pyfsa.main as main

from click.testing import CliRunner


@pytest.fixture
def mock_csv():
    with mock.patch('pyfsa.main.csv') as csv:
        csv.convert_csv_file = mock.Mock()
        csv.convert_csv_file.return_value = {
            'x': {'a': 'y', 'b': 'z'},
            'y': {'a': 'x', 'b': 'z'},
            'z': {'a': 'z', 'b': 'z'}
        }

        yield csv


@pytest.mark.cli
@pytest.mark.parametrize('cmd', [
    'state -f states.csv out.png'
])
def test_cli(
    cmd: str,
    mock_csv
):
    runner = CliRunner()

    with runner.isolated_filesystem() as fs:
        path = plb.Path(fs)
        (path / 'states.csv').touch()
        result = runner.invoke(main.main, [
            *cmd.split()
        ])
        assert not result.exception
        assert plb.Path('out.png').exists()
