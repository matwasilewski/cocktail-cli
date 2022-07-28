import pytest as pytest
from click.testing import CliRunner
from cocktail_cli.cli import cli


@pytest.fixture
def cli_runner():
    runner = CliRunner()
    return runner


def test_cli(cli_runner):
    result = cli_runner.invoke(cli, ["whiskey"])
    assert result.exit_code == 0


def test_with_pantry(cli_runner):
    result = cli_runner.invoke(cli, ["resources/test_pantry.csv"])
    assert result.exit_code == 0
