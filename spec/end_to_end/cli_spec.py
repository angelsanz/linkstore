from expects import expect, equal, be_empty
from click.testing import CliRunner

from linkstore.cli import linkstore_cli as cli

with description('the command-line interface'):
    with context('when saving links'):
        with it('does not output anything'):
            cli_runner = CliRunner()
            an_url = 'https://www.example.com/'
            a_tag = 'favourites'

            execution_result = cli_runner.invoke(cli, [ 'save', an_url, a_tag ])

            expect(execution_result.exit_code).to(equal(0))
            expect(execution_result.output).to(be_empty)
