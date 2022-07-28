import pytest as pytest
from click.testing import CliRunner
from src.cocktail_cli.cli import cli


@pytest.fixture
def cli_runner():
    runner = CliRunner()
    return runner


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['whiskey'])
    assert result.exit_code == 0
